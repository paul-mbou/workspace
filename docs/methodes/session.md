# Session de travail

Paul est ingénieur logiciel. Le travail se fait dans le code : lire, modifier, lancer, vérifier. Le handbook et les agents servent cette boucle, ils ne la remplacent pas.

## Avant d'écrire

1. Lire le contrat du dépôt, dans l'ordre de [Continuité](continuite.md).
2. Si la zone est large ou inconnue, passer par jCodeMunch (voir [Contexte](contexte.md)).
3. Si la demande est ambiguë et chère à inverser, écrire le plan ou l'ADR avant le code. Un design logiciel passe par le plugin [Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model) : `/egm-brainstorm`, puis `/egm-draft`, puis `/egm-review`. L'elephant garde le contexte du projet ; les reviewers goldfish relisent le document sans l'historique de la conversation. L'approbation reste humaine avant d'implémenter.
4. Repérer la règle de calcul ou le design system déjà présent. Ne pas en inventer un autre.

## Pendant

Pipeline décrit par la règle `common-development-workflow` :

1. **Plan.** Découper, nommer les dépendances et les risques. L'agent `planner` sert aux features larges.
2. **TDD.** Test rouge, implémentation minimale, refactor. Cible de couverture : 80 %. L'agent `tdd-guide` porte cette boucle. Types attendus : unitaires, intégration, parcours E2E du langage en cours.
3. **Revue.** Juste après l'écriture, revue du diff. Corriger d'abord le critique et le haut. Agents : `code-reviewer` pour le code, et le reviewer du langage (`react-reviewer`, `typescript-reviewer`, etc.) quand les fichiers correspondent.
4. **Vérification visible.** Pour une UI, ouvrir le flux dans le navigateur ou sur device et le parcourir comme un utilisateur : cliquer, saisir, envoyer, changer de page. Une capture seule ne compte pas. Vérifier les écrans qui partagent le même état, les états vides et d'erreur, et le mobile si la mise en page a changé.

## Style de code commun

Règle `common-coding-style` :

- Créer un nouvel objet plutôt que muter l'existant.
- Petits fichiers, cohésion forte. Taille typique 200–400 lignes, plafond 800.
- Organiser par feature ou domaine, pas par type de fichier.
- Gérer les erreurs à chaque niveau. Message utile côté UI, détail côté serveur. Ne pas avaler une erreur.
- Valider aux frontières (schéma quand il existe). Échouer tôt.

UI des produits camerounais : textes en français, code, variables et commentaires en anglais. Montants en FCFA quand le produit est local.

## Fin de session

| Événement | Écrit où |
| --- | --- |
| Travail en cours, à reprendre demain | `HANDOFF.md` du dépôt, une page maximum |
| Choix d'architecture difficile à inverser | ADR dans `docs/decisions/` |
| Nouvelle contrainte permanente | `AGENTS.md`, et un lint ou un test si la règle doit tenir sans mémoire |
| Gros changement de structure | rafraîchir `docs/knowledge/` avec le skill `knowledge-memory-gen` |
| Récap pour quelqu'un qui ne lit pas le code | skill `weekly-features-recap` |

## Contrat avec les agents

Ces préférences sont actives dans Cursor au quotidien :

- Commit et push uniquement quand c'est demandé. Un déploiement demandé ou une publication GitHub explicite autorise le push correspondant.
- Messages de commit en Conventional Commits, passés par HEREDOC.
- Pas de modification de `git config`. Pas de push forcé. Pas de `--no-verify` sans demande explicite.
- Pull requests via `gh`, avec le résumé et le plan de test.
- Réponses directes, en langage affirmatif.
- Après un changement d'interface, vérifier le comportement dans le navigateur avant de déclarer la tâche finie.

## Agents spécialisés utilisés

La liste complète vit dans l'outillage Cursor. Ceux que les règles citent par nom :

| Agent | Moment |
| --- | --- |
| `planner` | feature ou refactor large |
| `tdd-guide` | nouvelle feature, bug, refactor |
| `code-reviewer` | après l'écriture |
| `security-reviewer` | auth, saisie, secrets, paiement |
| `react-reviewer` / `typescript-reviewer` | fichiers React ou TypeScript |
| reviewer du langage | tout changement dans ce langage |

Les sous-agents ne relisent pas tout le dépôt en parallèle. Un appel ciblé suffit.
