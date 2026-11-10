# Git et livraison

## Commits

Format de la règle `common-git-workflow` :

```text
<type>: <description>

<corps optionnel>
```

Types : `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`.

Un commit n'est créé que sur demande. Le message passe par un HEREDOC pour garder les paragraphes. On ne commit pas `.env`, de keystore, ni de jeton. L'installation ECC désactive le trailer `Co-Authored-By` ; on ne le rajoute pas.

Avant de committer : `git status`, `git diff`, `git log` pour caler le ton sur l'historique du dépôt. Après un échec de hook, on corrige et on crée un nouveau commit. On n'amende pas un commit déjà poussé.

## Branches et pull requests

1. Regarder tout l'historique depuis la base, pas seulement le dernier commit.
2. `git diff <base>...HEAD` pour le contenu réel de la PR.
3. Pousser avec `-u` si la branche est nouvelle.
4. `gh pr create` avec un résumé court et un plan de test.

Pas de rebase interactif lancé par un agent. Pas de force-push sur `main`.

## Vérifier avant de dire que c'est fini

La commande exacte dépend du dépôt. Le socle habituel :

```bash
# Web TypeScript
npm test
npm run check
npm run build

# Flutter
flutter analyze
flutter test
```

Une interface se vérifie en plus dans le navigateur ou sur device. Voir [Session](session.md).

## Déploiement observé

| Cible | Commande habituelle | Où |
| --- | --- | --- |
| Vercel production | `npx vercel --prod --yes` | sites Astro / React déjà liés |
| Vercel preview | `npx vercel --yes` | seulement si la preview est demandée |
| Premier lien Vercel | `npx vercel link --yes` puis deploy | projet pas encore lié |
| Android / iOS store | fastlane, déjà installé via Homebrew | apps Flutter |
| Correctif mobile sans store | Shorebird | apps qui l'ont dans le `pubspec` (`fgm_lyrics_app`) |
| APK direct | dépôt public dédié | exemple : `fgm-hymnals-apk` |

Sur Bricks, la cible de production est `@astrojs/vercel`. On n'y revient pas à `@astrojs/node` sans demande explicite. Cette contrainte est dans le dépôt Bricks, pas dans tous les sites.

Le déploiement suit le dernier arbre de travail demandé. On ne pousse pas le Git distant sauf demande séparée : Vercel peut déployer le working tree.

## Récap hebdo

`weekly-features-recap` produit, à partir de l'historique Git et des transcripts Cursor, trois textes en langage courant : récap, standup, changelog. Public : PM et non-développeurs.
