# Continuité entre agents

Les chats et la mémoire de l'IDE disparaissent. Le dépôt reste. Le skill `ai-continuity-kit` (dépôt [paul-mbou/ai-continuity-kit](https://github.com/paul-mbou/ai-continuity-kit)) est le modèle posé sur chaque projet.

## Fichiers

```text
AGENTS.md                 # contrat unique, lu par tous les outils
CLAUDE.md                 # pointe vers AGENTS.md
HANDOFF.md                # état de la session, court
docs/PRODUCT.md           # ce que le produit est, et n'est pas
docs/decisions/           # ADR datés
docs/knowledge/           # onboarding profond
  INDEX.md
.cursor/rules/            # règles Cursor du projet, qui renvoient à AGENTS.md
.agents/skills/           # playbooks du domaine
```

## Ordre de lecture

Tout agent qui reprend le projet lit dans cet ordre, puis s'arrête :

1. `AGENTS.md`
2. `HANDOFF.md`
3. `docs/PRODUCT.md`
4. `docs/knowledge/INDEX.md`, puis seulement les pages indiquées
5. Les ADR si le sujet touche l'architecture
6. Le skill du domaine (`.agents/skills/` ou `.cursor/skills/`)

`PROJECT_SPEC.md` et `OPEN_QUESTIONS.md` viennent ensuite quand ils existent. On n'invente pas une règle produit qui contredit ces fichiers.

## Knowledge memory

Le skill `knowledge-memory-gen` remplit `docs/knowledge/` à partir du code réel, pas d'un modèle générique. Jeu de pages :

| Fichier | Contenu |
| --- | --- |
| `INDEX.md` | parcours de lecture |
| `PROJECT_OVERVIEW.md` | but, stack, arborescence |
| `ARCHITECTURE.md` | état, routing, données |
| `CODING_CONVENTIONS.md` | noms, fichiers, patterns |
| `DEVELOPMENT_RULES.md` | contraintes, sécurité, env |
| `PATTERNS.md` | recette pour ajouter une feature |
| `API_CONTRACT.md` | seulement s'il y a une API |
| `THEME_AND_UI.md` | seulement s'il y a une UI |
| `PROJECT_STATUS.md` | maturité, dettes, suite |

Une page qui ne s'applique pas se saute. Une page existante se met à jour là où le code a changé, sans réécriture cosmétique.

## Principes

1. `AGENTS.md` est la source. Les fichiers d'outil ne font que pointer dessus.
2. Une règle qui ne doit jamais casser vit dans un test, un lint ou une CI, pas seulement dans un paragraphe.
3. Une décision datée va dans un ADR. Un chat ne compte pas.
4. `HANDOFF.md` tient sur un écran.
5. Aucun secret dans ces fichiers.

## Exemple vécu : Bricks

`~/My_Projects/ReactJS/bricks` applique ce kit. Son `AGENTS.md` ajoute les règles du domaine : stock dérivé des mouvements, calculs dans `packages/domain`, mutations sensibles via une Appwrite Function (Zod, rôles, `AuditLog`), UI en français, jetons de marque `slate` / `clay` / `br-*`, déploiement Vercel avec `@astrojs/vercel`. Ces règles sont celles du produit, pas celles de tous les dépôts. Le handbook global ne les copie pas dans les autres projets.
