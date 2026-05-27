/**
 * src/content.config.ts — Content collections.
 * defineBookSchemas returns chapters + tools-collateral; extend via
 * standard JS spread + Zod `.extend()` if you need book-specific fields.
 */
import { defineBookSchemas } from '@brandon_m_behring/book-scaffold-astro/schemas';

export const { collections } = defineBookSchemas({
  preset: 'research-portfolio',
  // Real chapters live in src/content/textbook/ (the 13 KF-decomposed chapters),
  // not the scaffold-default src/content/chapters/. chaptersBase redirects the
  // glob loader so they're wired into the `chapters` collection (ADR-051).
  chaptersBase: './src/content/textbook',
});
