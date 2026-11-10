# Contexte et recherche de code

Règle globale `ai-context-compression`. Elle est toujours active. But : une recherche précise plutôt qu'un balayage de fichiers.

Il n'y a pas de proxy Cursor → Headroom pour les modèles d'abonnement. La compression passe par les MCP jCodeMunch et Headroom.

## Choisir un outil

| Situation | Outil |
| --- | --- |
| « Où est-ce géré ? », appelants, impact d'un changement, zone large inconnue | jCodeMunch (`route`, puis `order`) |
| Fichier déjà connu, petit dépôt, correction d'une ligne | Grep, Glob, Read |
| Gros résultat (logs, JSON, trace) encore utile | Headroom `headroom_compress` |
| Besoin de l'original après compression | Headroom `headroom_retrieve`, avec une requête étroite |
| Extrait déjà court | rien |

On ne chaîne pas jCodeMunch et Headroom sur le même payload, sauf si le résultat jCodeMunch reste énorme.

## jCodeMunch

Binaire observé : `~/.local/bin/jcodemunch-mcp`, lancé par `uvx jcodemunch-mcp`. Premier usage d'une session : résoudre ou indexer le dépôt si la tâche demande une recherche. Ensuite :

1. `route` avec la tâche en langage clair.
2. `order` sur l'action renvoyée (appelants, impact, source d'un symbole).
3. S'arrêter dès que la preuve suffit. Une absence citable se rapporte, sans relancer des synonymes.
4. Après édition, réindexer les chemins changés si le hook ne l'a pas fait.

Hooks Claude déjà branchés sur ce binaire : après Edit/Write, avant compactage, à la fin d'une tâche.

Ne pas utiliser jCodeMunch pour relire un fichier déjà ouvert, ni pour remplacer la lecture ciblée juste avant une édition.

## Headroom

Binaire : `~/.local/bin/headroom` (`headroom-ai` 0.42.0), servi en MCP avec `--proxy-url http://127.0.0.1:8787`.

Compresser une fois les sorties volumineuses. Travailler sur la forme compressée. `headroom_stats` sert à mesurer, pas à chaque tour.

## Documentation de bibliothèque

Pour une API, un framework ou un CLI, interroger Context7 (`resolve-library-id`, puis `query-docs`) plutôt que la mémoire du modèle. Le serveur est `https://mcp.context7.com/mcp`.

## Design et appareils

| Besoin | MCP |
| --- | --- |
| Fichier Figma | Framelink Figma MCP (`figma-developer-mcp`) |
| Écran généré | Google Stitch |
| App Flutter en cours d'exécution | Dart MCP |
| Device ou simulateur | mobile-mcp |
| Parcours déclaratif | Maestro (`maestro mcp`) |
| Collections HTTP | Postman MCP |
| Projet Firebase | `firebase-tools mcp` |

Les jetons de Figma, Postman et Stitch restent dans `~/.cursor/mcp.json`.
