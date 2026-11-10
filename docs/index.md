# Atelier

Ce dépôt est la copie portable du workspace de Paul Mbou. Il sert à retrouver, sur une autre machine, les outils, les méthodes et les contrats déjà utilisés sur les projets web et mobile.

Le site rendu est la lecture. Le dépôt Git est la sauvegarde. Les deux avancent ensemble : un `git push` sur `main` reconstruit GitHub Pages.

## Lire selon le besoin

| Besoin | Page |
| --- | --- |
| Réinstaller un Mac | [Nouvelle machine](setup/nouvelle-machine.md) |
| Un outil a été ajouté ou retiré | [Mettre à jour](setup/mettre-a-jour.md) |
| Savoir comment une session de code se déroule | [Session de travail](methodes/session.md) |
| Reprendre un projet avec n'importe quel agent | [Continuité](methodes/continuite.md) |
| Chercher dans un gros dépôt sans noyer le contexte | [Contexte](methodes/contexte.md) |
| Commits, pull requests, déploiement | [Git et livraison](methodes/git.md) |
| Tests, revue, secrets | [Qualité et sécurité](methodes/qualite.md) |
| UI web ou mobile | [Interface](methodes/interface.md) |
| Stack du moment | [Web](stacks/web.md), [Mobile](stacks/mobile.md), [Services](stacks/services.md) |
| Liste réelle des skills, plugins, règles, MCP, projets | [Inventaire](generated/index.md) |

## Ce qui est figé, ce qui est régénéré

Les pages de méthodes décrivent des choix durables : ordre de lecture d'un dépôt, règles de commit, façon de vérifier une interface, séparation entre skill personnel et bibliothèque ECC.

L'inventaire est une photo de la machine au dernier sync. Ajouter un skill, un plugin, retirer une règle ou installer un CLI change cette photo uniquement après `python3 scripts/sync.py`.

## Identité observée

| Champ | Valeur |
| --- | --- |
| Nom | Paul Mbou |
| GitHub | [paul-mbou](https://github.com/paul-mbou) |
| Git `user.name` | `paul-mbou` |
| Git `user.email` | `paulmbou068@gmail.com` |
| Machine de référence | macOS, Apple Silicon |
| Dossier projets | `~/My_Projects` |

## Hors de ce dépôt

- Les clés API et les fichiers `.env`
- Le code des applications (chaque projet a son propre dépôt)
- Les skills fournis par l'application Cursor, qui reviennent avec Cursor
- Le corps complet des règles ECC, qui se réinstalle depuis [affaan-m/ECC](https://github.com/affaan-m/ECC)
