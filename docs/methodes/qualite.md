# Qualité et sécurité

## Avant chaque commit

Liste de `common-security` :

- aucun secret en dur
- entrées validées
- requêtes paramétrées
- HTML sanitisé
- CSRF en place là où il y a une session web
- auth et rôles vérifiés
- limitation de débit sur les endpoints exposés
- messages d'erreur sans fuite

## Si un problème de sécurité apparaît

1. S'arrêter.
2. Passer par `security-reviewer`.
3. Corriger le critique avant de continuer.
4. Faire tourner les secrets exposés.
5. Chercher le même motif ailleurs.

Le skill `security-review` couvre auth, saisie, secrets, endpoints et paiement. Le skill `production-audit` sert aux questions « qu'est-ce qui casse en production ? » sans envoyer le dépôt à un service d'audit externe.

## Tests

Règle `common-testing` :

1. Écrire le test.
2. Le voir échouer.
3. Écrire le minimum pour le faire passer.
4. Refactorer.
5. Vérifier la couverture (cible 80 %).

Trois niveaux : unitaire, intégration, E2E du parcours critique. Si un test échoue, on corrige l'implémentation quand le test dit le comportement voulu. On ne plie pas le test pour faire taire un vrai écart.

Outils vus selon la stack :

| Stack | Outil |
| --- | --- |
| TypeScript / Astro | Vitest, `astro check` |
| Flutter | `flutter test`, `flutter analyze` |
| Parcours device | Maestro |
| Parcours web | navigateur Cursor, Playwright quand le dépôt l'a |
| Device réel ou simulateur | mobile-mcp, `adb`, simulateur Xcode |

## Revue

`common-code-review` : la revue a lieu avant de considérer le changement terminé. Ordre de gravité : critique, haut, puis moyen quand le coût est raisonnable.

Pour une UI, la revue visuelle ne remplace pas le parcours. États à regarder : vide, erreur, chargement, rôle sans droit, écran étroit.

## Web, rappels des règles `web-*`

- Organiser par surface, pas par type de fichier.
- CSP en production.
- Pas d'UI générique interchangeable : la page doit être reconnaissable comme ce produit.
- Performance : tenir les budgets du dépôt (les cibles chiffrées vivent dans `web-performance.mdc`).
- Captures de contrôle aux largeurs 320, 768, 1024 et 1440 quand la mise en page change.
- Hooks locaux au projet. Pas d'exécution distante ponctuelle branchée en hook.

## Paiement

Le skill `payment-gateway` pose un port indépendant du fournisseur. Le skill `payunit-integration` est l'adaptateur Payunit (Mobile Money, cartes, checkout hébergé, XAF). L'UI et les commandes parlent au port. Changer de PSP ne réécrit pas le checkout.

Aucun secret Payunit dans le client. Les appels signés passent par le backend du projet (Function, serveur), comme les autres mutations sensibles.
