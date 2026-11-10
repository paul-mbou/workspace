# Web

Stack observée sur les projets React du dossier `~/My_Projects/ReactJS`.

## Socle actuel

| Couche | Choix vu dans les dépôts |
| --- | --- |
| Site | Astro, rendu serveur, îlots React |
| UI | React, Tailwind 4 (`@tailwindcss/vite`) |
| Langage | TypeScript strict |
| Tests / types | Vitest, `@astrojs/check` |
| Hébergement | Vercel, adaptateur `@astrojs/vercel` |
| Alternative légère | Vite + React (ex. `todo-react`) |
| Cas Nuxt | `empire-audition` (déposé sous `Flutter/Apps`, stack Nuxt) |

Projets qui portent ce socle Astro + React + Tailwind : `bricks`, `briquo`, `proxima_immigration_website`. `goldstock` est le dépôt public de la landing GOLDSTOCK, ancêtre visuel du kit d'interface.

## Façon de construire une feature

1. Lire `AGENTS.md` du dépôt.
2. Poser le calcul pur dans un package de domaine testé, quand le dépôt en a un (`packages/domain` sur Bricks).
3. Garder les seuils, taux et rendements dans les réglages ou la base. Pas de constante magique.
4. UI en français si le produit est local. Composants dans le kit du dépôt, pas une deuxième librairie visuelle.
5. Formulaire long en sheet.
6. `npm test`, `npm run check`, `npm run build`.
7. Vérifier le flux dans le navigateur.
8. Déployer avec `npx vercel --prod --yes` quand le dépôt le demande.

## Appwrite côté web

Sur Bricks, Appwrite Cloud porte Auth, base, storage, functions, messaging et realtime. Le client ne reçoit pas de clé secrète d'API. Une mutation sensible (stock, argent, rôle) passe par une Function : schéma Zod, contrôle de rôle, écriture d'`AuditLog`. Le stock n'est pas saisi : il est dérivé des mouvements.

Les notifications push partent d'une alerte, puis d'une Function. Jamais depuis le navigateur.

## Fichiers de config habituels

- `package.json`, `astro.config`, `tsconfig.json`
- `src/styles` pour les jetons Tailwind
- `src/components` pour les îlots React
- `src/pages` pour les routes Astro
- `src/lib` pour le client, le store, la file offline

La forme exacte est celle du dépôt. Le knowledge du dépôt (`docs/knowledge/INDEX.md`) prime sur cette page.
