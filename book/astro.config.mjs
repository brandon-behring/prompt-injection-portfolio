// @ts-check
/**
 * astro.config.mjs — book-scaffold-astro consumer config.
 * defineBookConfig threads BOOK_PROFILE and wires the Integration.
 */
import { defineBookConfig } from '@brandon_m_behring/book-scaffold-astro';

export default await defineBookConfig({
  // Portfolio book deploys to Cloudflare Pages per plan §3 (deploy target;
  // custom domain TBD at v0.5+). Until then, the *.pages.dev URL is the
  // canonical site. Update wrangler.toml `name` field together with this.
  site: 'https://prompt-injection-portfolio.pages.dev',
});
