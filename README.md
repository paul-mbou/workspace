# Atelier

Handbook portable du workspace de Paul Mbou : méthodes, skills, règles, outils et projets. Le site est publié sur GitHub Pages.

**Site :** https://paul-mbou.github.io/workspace/  
**Source :** https://github.com/paul-mbou/workspace

Deux couches :

| Couche | Où | Qui l'écrit |
| --- | --- | --- |
| Méthodes stables | `docs/setup`, `docs/methodes`, `docs/stacks` | à la main, quand une façon de travailler change |
| Inventaire | `docs/generated`, `inventory.json`, `kit/` | `python3 scripts/sync.py`, depuis la machine |

Les secrets (clés MCP, `.env`, jetons) ne sont jamais versionnés. `scripts/sync.py` refuse d'écrire s'il détecte un jeton.

```bash
python3 scripts/sync.py
mkdocs serve
```

Nouvelle machine : `docs/setup/nouvelle-machine.md` et `scripts/bootstrap.sh`.
