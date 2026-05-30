"""Detector rungs for the attack-type-LODO harness (spec §4).

Four rungs behind a common :class:`Detector` protocol:

* ``tfidf``  — TF-IDF + LogisticRegression classical floor (CPU).
* ``frozen`` — frozen ModernBERT-base mean-pooled embeddings → LogisticRegression head.
* ``lora``   — LoRA fine-tune of ModernBERT-base (rank swept on val).
* ``full_ft``— full fine-tune of ModernBERT-base (LR swept on val).

Each rung's ``fit`` selects its recipe on a **train-internal validation split**
(spec §3) using the same metric stack as the reported metrics (``eval_toolkit``
``pr_auc``) — never on the held-out test attack-types. Transformer rungs use
**device-adaptive precision** (**native** bf16 on Ampere+, else fp16) with an fp32 softmax
cast; the RTX 2070 SUPER is Turing — torch reports *emulated* bf16 there, so we gate on native
support and use fp16 (the native-fast Turing path). ``torch`` / ``transformers``
/ ``peft`` are imported lazily so importing this module (and the TF-IDF rung) stays light.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

import numpy as np
from eval_toolkit import metric_specs, scorecard
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

__all__ = ["Detector", "TfidfLogReg", "FrozenProbe", "LoRADetector", "FullFT", "make_detector", "RUNG_NAMES"]

_DEFAULT_MODEL = "answerdotai/ModernBERT-base"
RUNG_NAMES: tuple[str, ...] = ("tfidf", "frozen", "lora", "full_ft")


@runtime_checkable
class Detector(Protocol):
    """A trainable injection detector that emits P(positive) per text."""

    name: str

    def fit(
        self,
        train_texts: Sequence[str],
        train_labels: Sequence[int],
        val_texts: Sequence[str],
        val_labels: Sequence[int],
    ) -> dict[str, object]:
        """Train + select the recipe on (train, val); return the selected recipe."""

    def predict_proba(self, texts: Sequence[str]) -> np.ndarray:
        """Return P(positive) as a float array aligned with ``texts``."""


def _val_pr_auc(labels: Sequence[int], scores: Sequence[float]) -> float:
    """AUPRC on a split via ``eval_toolkit.scorecard`` (selection metric = reported metric).

    Val splits are 2-class by construction (``carve_val_from_train`` rejects single-class
    splits), so a ``None`` point estimate means a degenerate fit — fail loud, never silent.
    """
    cell = scorecard(
        np.asarray(labels), np.asarray(scores), metrics=[metric_specs.pr_auc], bootstrap=False
    )["pr_auc"]
    if cell.value is None:
        raise ValueError(f"val pr_auc undefined (status={cell.status}: {cell.reason})")
    return float(cell.value)


def _select_device_dtype() -> tuple[object, object]:
    """Return ``(device, dtype)``: cuda+bf16 on Ampere+, cuda+fp16 on Turing, else cpu+fp32.

    bf16 is gated on **native** support (``including_emulation=False``): torch 2.12 reports
    ``is_bf16_supported()`` True on Turing (e.g. the RTX 2070 SUPER) via *emulation*, but
    emulated bf16 carries overhead with no Turing tensor-core benefit — Turing has native fast
    fp16. So we pick fp16 on Turing and reserve bf16 for Ampere+ where it is native (the cloud
    target). Verified: ``is_bf16_supported(including_emulation=False)`` is False on capability 7.5.
    """
    import torch

    if torch.cuda.is_available():
        native_bf16 = torch.cuda.is_bf16_supported(including_emulation=False)
        dtype = torch.bfloat16 if native_bf16 else torch.float16
        return torch.device("cuda"), dtype
    return torch.device("cpu"), torch.float32


# --------------------------------------------------------------------------- #
# Classical floor
# --------------------------------------------------------------------------- #
class TfidfLogReg:
    """TF-IDF + LogisticRegression floor; ``C`` selected on val AUPRC."""

    name = "tfidf"

    def __init__(
        self,
        *,
        c_grid: Sequence[float] = (0.1, 1.0, 10.0),
        max_features: int = 50_000,
        ngram_range: tuple[int, int] = (1, 2),
        seed: int = 0,
    ) -> None:
        self.c_grid = tuple(c_grid)
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.seed = seed
        self._vec: TfidfVectorizer | None = None
        self._clf: LogisticRegression | None = None
        self.recipe: dict[str, object] = {}

    def fit(self, train_texts, train_labels, val_texts, val_labels):  # type: ignore[no-untyped-def]
        vec = TfidfVectorizer(max_features=self.max_features, ngram_range=self.ngram_range)
        x_tr = vec.fit_transform(list(train_texts))
        x_val = vec.transform(list(val_texts))
        best: tuple[float, float, LogisticRegression] | None = None
        for c in self.c_grid:
            clf = LogisticRegression(C=c, class_weight="balanced", max_iter=1000, random_state=self.seed)
            clf.fit(x_tr, list(train_labels))
            score = _val_pr_auc(val_labels, clf.predict_proba(x_val)[:, 1])
            if best is None or score > best[0]:
                best = (score, c, clf)
        assert best is not None
        self._vec, self._clf = vec, best[2]
        self.recipe = {"C": best[1], "val_pr_auc": best[0]}
        return self.recipe

    def predict_proba(self, texts):  # type: ignore[no-untyped-def]
        if self._vec is None or self._clf is None:
            raise RuntimeError("TfidfLogReg.predict_proba called before fit")
        return self._clf.predict_proba(self._vec.transform(list(texts)))[:, 1]


# --------------------------------------------------------------------------- #
# Frozen-probe
# --------------------------------------------------------------------------- #
class FrozenProbe:
    """Frozen ModernBERT mean-pooled embeddings → LogisticRegression head."""

    name = "frozen"

    def __init__(
        self,
        *,
        model_name: str = _DEFAULT_MODEL,
        max_length: int = 512,
        batch_size: int = 32,
        c_grid: Sequence[float] = (0.1, 1.0, 10.0),
        seed: int = 0,
    ) -> None:
        self.model_name = model_name
        self.max_length = max_length
        self.batch_size = batch_size
        self.c_grid = tuple(c_grid)
        self.seed = seed
        self._tok = None
        self._model = None
        self._device = None
        self._clf: LogisticRegression | None = None
        self.recipe: dict[str, object] = {}

    def _ensure_model(self) -> None:
        if self._model is None:
            from transformers import AutoModel, AutoTokenizer

            self._device, _ = _select_device_dtype()
            self._tok = AutoTokenizer.from_pretrained(self.model_name)
            self._model = AutoModel.from_pretrained(self.model_name).to(self._device).eval()

    def _embed(self, texts: Sequence[str]) -> np.ndarray:
        import torch

        self._ensure_model()
        assert self._tok is not None and self._model is not None
        chunks: list[np.ndarray] = []
        texts = list(texts)
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            enc = self._tok(
                batch, truncation=True, max_length=self.max_length, padding=True, return_tensors="pt"
            ).to(self._device)
            with torch.no_grad():
                hidden = self._model(**enc).last_hidden_state
                mask = enc["attention_mask"].unsqueeze(-1)
                summed = (hidden * mask).sum(dim=1)
                counts = mask.sum(dim=1).clamp(min=1)
                chunks.append((summed / counts).float().cpu().numpy())
        return np.vstack(chunks)

    def fit(self, train_texts, train_labels, val_texts, val_labels):  # type: ignore[no-untyped-def]
        x_tr = self._embed(train_texts)
        x_val = self._embed(val_texts)
        best: tuple[float, float, LogisticRegression] | None = None
        for c in self.c_grid:
            clf = LogisticRegression(C=c, class_weight="balanced", max_iter=2000, random_state=self.seed)
            clf.fit(x_tr, list(train_labels))
            score = _val_pr_auc(val_labels, clf.predict_proba(x_val)[:, 1])
            if best is None or score > best[0]:
                best = (score, c, clf)
        assert best is not None
        self._clf = best[2]
        self.recipe = {"C": best[1], "val_pr_auc": best[0]}
        return self.recipe

    def predict_proba(self, texts):  # type: ignore[no-untyped-def]
        if self._clf is None:
            raise RuntimeError("FrozenProbe.predict_proba called before fit")
        return self._clf.predict_proba(self._embed(texts))[:, 1]


# --------------------------------------------------------------------------- #
# Transformer fine-tuning helpers (shared by LoRA + full-FT)
# --------------------------------------------------------------------------- #
def _class_weights(labels: Sequence[int], device: object):  # type: ignore[no-untyped-def]
    import torch

    arr = np.asarray(labels)
    weight = torch.ones(2, dtype=torch.float32)
    classes, counts = np.unique(arr, return_counts=True)
    for c, ct in zip(classes, counts, strict=False):
        weight[int(c)] = float(arr.size) / (len(classes) * float(ct))
    return weight.to(device)


def _train_seq_classifier(  # type: ignore[no-untyped-def]
    model, tok, texts, labels, *, device, dtype, epochs, batch_size, lr, max_length, seed
):
    """Minimal real training loop: AdamW + class-weighted CE, fp16/bf16 autocast, fp32 loss."""
    import torch

    torch.manual_seed(seed)
    labels_t = torch.tensor(np.asarray(labels), dtype=torch.long)
    loss_fn = torch.nn.CrossEntropyLoss(weight=_class_weights(labels, device))
    opt = torch.optim.AdamW(model.parameters(), lr=lr)
    model.to(device).train()
    use_amp = getattr(device, "type", "cpu") == "cuda"
    rng = np.random.default_rng(seed)
    idx = np.arange(len(texts))
    texts = list(texts)
    for _ in range(epochs):
        rng.shuffle(idx)
        for i in range(0, len(idx), batch_size):
            b = idx[i : i + batch_size]
            enc = tok(
                [texts[j] for j in b], truncation=True, max_length=max_length, padding=True, return_tensors="pt"
            ).to(device)
            y = labels_t[b].to(device)
            opt.zero_grad()
            with torch.autocast(device_type=getattr(device, "type", "cpu"), dtype=dtype, enabled=use_amp):
                logits = model(**enc).logits
            loss = loss_fn(logits.float(), y)
            loss.backward()
            opt.step()
    return model


def _predict_seq_classifier(model, tok, texts, *, device, max_length, batch_size):  # type: ignore[no-untyped-def]
    import torch

    model.to(device).eval()
    texts = list(texts)
    out: list[np.ndarray] = []
    for i in range(0, len(texts), batch_size):
        enc = tok(
            texts[i : i + batch_size], truncation=True, max_length=max_length, padding=True, return_tensors="pt"
        ).to(device)
        with torch.no_grad():
            probs = torch.softmax(model(**enc).logits.float(), dim=-1)[:, 1].cpu().numpy()
        out.append(probs)
    return np.concatenate(out)


# --------------------------------------------------------------------------- #
# LoRA + full fine-tune
# --------------------------------------------------------------------------- #
class LoRADetector:
    """LoRA fine-tune of ModernBERT-base; rank ``r`` selected on val AUPRC."""

    name = "lora"

    def __init__(
        self,
        *,
        model_name: str = _DEFAULT_MODEL,
        r_grid: Sequence[int] = (8, 16),
        epochs: int = 3,
        batch_size: int = 16,
        lr: float = 1e-4,
        max_length: int = 512,
        seed: int = 0,
    ) -> None:
        self.model_name = model_name
        self.r_grid = tuple(r_grid)
        self.epochs = epochs
        self.batch_size = batch_size
        self.lr = lr
        self.max_length = max_length
        self.seed = seed
        self._tok = None
        self._model = None
        self._device = None
        self.recipe: dict[str, object] = {}

    def _build(self, r: int):  # type: ignore[no-untyped-def]
        from peft import LoraConfig, TaskType, get_peft_model
        from transformers import AutoModelForSequenceClassification

        base = AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=2)
        cfg = LoraConfig(
            task_type=TaskType.SEQ_CLS,
            r=r,
            lora_alpha=2 * r,
            lora_dropout=0.05,
            target_modules="all-linear",
            modules_to_save=["classifier"],
        )
        return get_peft_model(base, cfg)

    def fit(self, train_texts, train_labels, val_texts, val_labels):  # type: ignore[no-untyped-def]
        from transformers import AutoTokenizer

        self._device, dtype = _select_device_dtype()
        self._tok = AutoTokenizer.from_pretrained(self.model_name)
        best: tuple[float, int, object] | None = None
        for r in self.r_grid:
            model = self._build(r)
            _train_seq_classifier(
                model, self._tok, train_texts, train_labels, device=self._device, dtype=dtype,
                epochs=self.epochs, batch_size=self.batch_size, lr=self.lr, max_length=self.max_length, seed=self.seed,
            )
            scores = _predict_seq_classifier(
                model, self._tok, val_texts, device=self._device, max_length=self.max_length, batch_size=self.batch_size
            )
            v = _val_pr_auc(val_labels, scores)
            if best is None or v > best[0]:
                best = (v, r, model)
        assert best is not None
        self._model = best[2]
        self.recipe = {"r": best[1], "lr": self.lr, "epochs": self.epochs, "val_pr_auc": best[0]}
        return self.recipe

    def predict_proba(self, texts):  # type: ignore[no-untyped-def]
        if self._model is None:
            raise RuntimeError("LoRADetector.predict_proba called before fit")
        return _predict_seq_classifier(
            self._model, self._tok, texts, device=self._device, max_length=self.max_length, batch_size=self.batch_size
        )


class FullFT:
    """Full fine-tune of ModernBERT-base; learning rate selected on val AUPRC."""

    name = "full_ft"

    def __init__(
        self,
        *,
        model_name: str = _DEFAULT_MODEL,
        lr_grid: Sequence[float] = (2e-5, 5e-5),
        epochs: int = 3,
        batch_size: int = 16,
        max_length: int = 512,
        seed: int = 0,
    ) -> None:
        self.model_name = model_name
        self.lr_grid = tuple(lr_grid)
        self.epochs = epochs
        self.batch_size = batch_size
        self.max_length = max_length
        self.seed = seed
        self._tok = None
        self._model = None
        self._device = None
        self.recipe: dict[str, object] = {}

    def _build(self):  # type: ignore[no-untyped-def]
        from transformers import AutoModelForSequenceClassification

        return AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=2)

    def fit(self, train_texts, train_labels, val_texts, val_labels):  # type: ignore[no-untyped-def]
        from transformers import AutoTokenizer

        self._device, dtype = _select_device_dtype()
        self._tok = AutoTokenizer.from_pretrained(self.model_name)
        best: tuple[float, float, object] | None = None
        for lr in self.lr_grid:
            model = self._build()
            _train_seq_classifier(
                model, self._tok, train_texts, train_labels, device=self._device, dtype=dtype,
                epochs=self.epochs, batch_size=self.batch_size, lr=lr, max_length=self.max_length, seed=self.seed,
            )
            scores = _predict_seq_classifier(
                model, self._tok, val_texts, device=self._device, max_length=self.max_length, batch_size=self.batch_size
            )
            v = _val_pr_auc(val_labels, scores)
            if best is None or v > best[0]:
                best = (v, lr, model)
        assert best is not None
        self._model = best[2]
        self.recipe = {"lr": best[1], "epochs": self.epochs, "val_pr_auc": best[0]}
        return self.recipe

    def predict_proba(self, texts):  # type: ignore[no-untyped-def]
        if self._model is None:
            raise RuntimeError("FullFT.predict_proba called before fit")
        return _predict_seq_classifier(
            self._model, self._tok, texts, device=self._device, max_length=self.max_length, batch_size=self.batch_size
        )


def make_detector(name: str, *, seed: int = 0, **overrides: object) -> Detector:
    """Construct a rung by name (one of :data:`RUNG_NAMES`) with optional overrides."""
    factories: dict[str, type] = {
        "tfidf": TfidfLogReg,
        "frozen": FrozenProbe,
        "lora": LoRADetector,
        "full_ft": FullFT,
    }
    if name not in factories:
        raise KeyError(f"unknown rung {name!r}; expected one of {RUNG_NAMES}")
    return factories[name](seed=seed, **overrides)  # type: ignore[return-value, arg-type]
