# prompt-injection-portfolio-book — AI authoring guide

This book is built with `@brandon_m_behring/book-scaffold-astro` (academic profile, v3.1.0).

**Where things live:**

- Chapters: `src/content/chapters/*.mdx` — frontmatter follows the academic schema
- Components, layouts, default routes: `@brandon_m_behring/book-scaffold-astro/components/...`
- Style customizations: `src/styles/` (overrides package styles)
- Bibliography: `bibliography.bib` (academic) → `src/data/references.json` via `npm run build:bib`
- Cross-references: ids on `<Theorem>` / `<Figure>` → `src/data/labels.json` via `npm run build:labels`

**Toolkit reference:** [PACKAGE_DESIGN.md](https://github.com/brandon-behring/book-scaffold-astro/blob/v3.0/PACKAGE_DESIGN.md) — single source of truth for the API. File issues at https://github.com/brandon-behring/book-scaffold-astro/issues with label `consumer:prompt-injection-portfolio-book`.
