# Services

Services rencontrés dans les dossiers et les dépôts. Chaque projet n'en utilise qu'une partie. Le choix réel est dans son `AGENTS.md`.

## Backend et données

| Service | Rôle observé | Dossier ou trace |
| --- | --- | --- |
| Appwrite Cloud | auth, base, storage, functions, messaging, realtime | `~/My_Projects/Appwrite`, client `appwrite` / `node-appwrite` |
| Firebase | auth et données mobile, projet MCP | `firebase_core` dans plusieurs apps, CLI `firebase` |
| Directus | dossier de travail présent | `~/My_Projects/Directus` |
| Serverpod | dossier de travail présent | `~/My_Projects/Serverpod` |

Côté Appwrite, les permissions de collection se relisent à chaque collection nouvelle. Les secrets de fonction restent dans Appwrite, pas dans le client.

## Paiement

Port : skill et dépôt `payment-gateway`.  
Adaptateur Cameroun / XAF : skill et dépôt `payunit-integration` (Mobile Money, cartes, checkout hébergé).

L'écran de paiement dépend du port. L'adaptateur se remplace sans réécrire l'UI.

## Hébergement et livraison

| Besoin | Outil |
| --- | --- |
| Site web | Vercel CLI |
| Build mobile | Xcode, Android Studio, fastlane, CocoaPods |
| Patch OTA | Shorebird |
| APK public sans ouvrir les sources | dépôt `fgm-hymnals-apk` |

## Recherche, design, API

| Besoin | Outil |
| --- | --- |
| Docs à jour d'une lib | Context7 |
| Code et impact | jCodeMunch |
| Gros logs | Headroom |
| Figma | Framelink Figma MCP |
| Maquettes générées | Google Stitch |
| Requêtes HTTP | Postman MCP |
| Device | mobile-mcp, Maestro, adb |

Le détail des commandes MCP, sans jetons, est dans [MCP](../generated/mcp.md).

## Éditeur

| Outil | Rôle |
| --- | --- |
| Cursor | IDE principal, skills, règles, MCP |
| Claude Code | mêmes skills utiles, hooks jCodeMunch, plugin floorplan |
| Antigravity / Antigravity IDE | présents sur le PATH |
| Android Studio | SDK Android et JDK |
| Xcode | iOS |

Les skills Cursor intégrés (`~/.cursor/skills-cursor`) suivent la mise à jour de Cursor : automate, canvas, hooks, rules, bugbot, security review, loop, origin. On ne les clone pas.
