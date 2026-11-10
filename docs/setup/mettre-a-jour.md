# Mettre à jour ce handbook

Le site ne voit pas la machine. GitHub Actions construit les pages Markdown déjà commitées. La mise à jour est donc locale, puis poussée.

## Quand lancer un sync

| Événement | Action |
| --- | --- |
| Skill ajouté, déplacé ou supprimé | sync |
| Règle `.mdc` ajoutée ou supprimée | sync |
| Serveur MCP ajouté ou retiré | sync |
| CLI installé ou désinstallé parmi la liste surveillée | sync |
| Nouveau dossier de projet sous `~/My_Projects` | sync |
| Dépôt GitHub créé ou archivé | sync |
| Changement de méthode (ordre de travail, stack par défaut, règle de revue) | éditer la page de `docs/methodes` ou `docs/stacks` |

## Commande

Depuis la racine de ce dépôt :

```bash
python3 scripts/sync.py
git diff -- docs/generated inventory.json kit
```

Le script réécrit uniquement :

- `docs/generated/*.md`
- `inventory.json`
- `kit/mcp.example.json` (commandes et URL, secrets masqués)
- `kit/personal-rules/*.mdc` (les deux règles personnelles)

S'il détecte un jeton (`figd_`, `PMAK-`, `ghp_`, `AQ.`, clé Google, JWT), il s'arrête sans écrire.

## Publier

```bash
git add docs/generated inventory.json kit
git commit -m "$(cat <<'EOF'
docs: refresh the workspace inventory

EOF
)"
git push
```

Pages se déploie via `.github/workflows/pages.yml` sur `main`. L'URL reste https://paul-mbou.github.io/workspace/

Prévisualisation locale :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

## Ajouter un outil à la surveillance

1. L'installer sur la machine.
2. Ajouter son nom dans `TOOL_CANDIDATES` de `scripts/sync.py` s'il n'y est pas déjà.
3. Relancer le sync.

Retirer un outil : le désinstaller, lancer le sync. Il passe dans la section Absents, ou disparaît si son nom est aussi retiré de `TOOL_CANDIDATES`.

## Ajouter une règle personnelle

Les règles copiées pour la restauration sont nommées dans `PERSONAL_RULE_NAMES` (`scripts/sync.py`). Une nouvelle règle à emporter sur chaque machine s'ajoute à cet ensemble, puis le sync la copie dans `kit/personal-rules/`.

Les règles de langage ECC ne se copient pas ici. Elles se réinstallent avec ECC. L'inventaire en garde la liste pour comparer.

## Ce qu'il ne faut pas versionner

- `~/.cursor/mcp.json`
- `.env`, keystores, `google-services.json`, `GoogleService-Info.plist`
- dumps de sessions, historiques d'agents, caches
