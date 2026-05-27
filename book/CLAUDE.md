# prompt-injection-portfolio-book — AI authoring guide

This book is built with `@brandon_m_behring/book-scaffold-astro` (**research-portfolio** profile, **v4.x**; see ADR-051).

**Where things live:**

- Chapters: `src/content/textbook/*.mdx` — frontmatter follows the **research-portfolio** schema
  (wired via `defineBookSchemas({ preset, chaptersBase: './src/content/textbook' })`). Required
  fields include `last_verified` (a date) + `freshness` (experimental-result | literature-survey |
  theoretical | reference). Use MDX comments `{/* */}`, never HTML `<!-- -->`.
- Components, layouts, default routes: `@brandon_m_behring/book-scaffold-astro/components/...`
- Style customizations: `src/styles/` (overrides package styles)
- Bibliography: `bibliography.bib` → `src/data/references.json` via `npm run build:bib`
- Cross-references: ids on `<Theorem>` / `<Figure>` → `src/data/labels.json` via `npm run build:labels`

**Toolkit reference:** [book-scaffold-astro v4.4.0](https://github.com/brandon-behring/book-scaffold-astro/tree/v4.4.0) (see `recipes/` + `MIGRATION-v3-to-v4.md`) — single source of truth for the API. File issues at https://github.com/brandon-behring/book-scaffold-astro/issues with label `consumer:prompt-injection-portfolio-book`.
