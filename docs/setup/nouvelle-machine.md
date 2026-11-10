# Nouvelle machine

Objectif : un Mac neuf retrouve le même contrat de travail, puis les dépôts. Le script `scripts/bootstrap.sh` installe la base et clone les skills personnels. Il ne copie aucun secret.

## 1. Préparer le compte

```bash
git config --global user.name "paul-mbou"
git config --global user.email "paulmbou068@gmail.com"
gh auth login
```

Cloner ce handbook en premier :

```bash
git clone https://github.com/paul-mbou/workspace.git ~/My_Projects/workspace
cd ~/My_Projects/workspace
bash scripts/bootstrap.sh
```

## 2. PATH du shell

Le `~/.zshrc` de la machine d'origine accumule des blocs PATH dupliqués (Antigravity répété plusieurs fois) et des `FIGMA_TOKEN` vides. Sur une machine neuve, poser ce bloc une seule fois, puis remplir les jetons localement.

```bash
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
export PATH="$PATH:$HOME/.pub-cache/bin"
export PATH="$PATH:$HOME/Library/Android/sdk/platform-tools"
export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
export PATH="$JAVA_HOME/bin:$PATH"
export PATH="$HOME/Libs/flutter/bin:$PATH"
export PATH="$HOME/.gem/bin:$PATH"

export PNPM_HOME="$HOME/Library/pnpm"
export PATH="$PNPM_HOME:$PATH"

export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

export PATH="$HOME/.shorebird/bin:$PATH"
export PATH="$HOME/.maestro/bin:$PATH"
export PATH="$HOME/.antigravity/antigravity/bin:$PATH"
export PATH="$HOME/.antigravity-ide/antigravity-ide/bin:$PATH"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

FNM_PATH="/opt/homebrew/opt/fnm/bin"
if [ -d "$FNM_PATH" ]; then
  eval "$(fnm env --shell zsh)"
fi

. "$HOME/.local/bin/env"
```

`FIGMA_TOKEN` reste dans le shell local ou dans le gestionnaire de mots de passe. Il ne va pas dans Git.

## 3. Ce que le script installe

| Élément | Emplacement attendu |
| --- | --- |
| Homebrew, git, gh, fnm, ripgrep, cocoapods, fastlane | `/opt/homebrew` |
| Node 24 | fnm |
| Flutter stable | `~/Libs/flutter` |
| Cursor, Android Studio | `/Applications` (casks) |
| Skills personnels | `~/.cursor/skills/<nom>` |
| Règles personnelles | `~/.cursor/rules/*.mdc` copiées depuis `kit/personal-rules` |

Skills clonés :

- `https://github.com/paul-mbou/ai-continuity-kit.git`
- `https://github.com/paul-mbou/knowledge-memory-gen.git`
- `https://github.com/paul-mbou/payment-gateway.git`
- `https://github.com/paul-mbou/payunit-integration.git`
- `https://github.com/paul-mbou/weekly-features-recap.git`
- `https://github.com/Endeavor068/ui-design-director.git`

Toute modification du skill `ui-design-director` se commit et se pousse sur `origin`. C'est la seule exception à « commit uniquement sur demande » : la règle `ui-design-director-github` l'exige.

## 4. À installer à la main

Ces outils étaient présents, mais leur installeur officiel est le bon chemin de restauration.

| Outil | Observation | Restauration |
| --- | --- | --- |
| Xcode | version relevée sur la machine d'origine | Mac App Store, puis `sudo xcodebuild -license accept` |
| Android SDK | `~/Library/Android/sdk` | premier lancement d'Android Studio, accepter les licences |
| ECC | `~/.cursor/skills/ecc` et la majorité de `~/.cursor/rules` | [affaan-m/ECC](https://github.com/affaan-m/ECC), puis comparer [Règles](../generated/rules.md) |
| jCodeMunch | `uvx jcodemunch-mcp`, binaire `~/.local/bin/jcodemunch-mcp` | `uv tool install jcodemunch-mcp` |
| Headroom | `~/.local/bin/headroom` → outil uv `headroom-ai` 0.42.0 | `uv tool install headroom-ai` |
| Maestro | `~/.maestro/bin/maestro` | [maestro.mobile.dev](https://maestro.mobile.dev) |
| Shorebird | `~/.shorebird/bin/shorebird` | [shorebird.dev](https://docs.shorebird.dev) |
| Vercel CLI, Firebase CLI | binaires npm globaux | `npm install -g vercel firebase-tools` |
| uv | `~/.local/bin/uv` | [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/) |

`pnpm` et `bun` ont un emplacement prévu dans `.zshrc` (`~/Library/pnpm`, `~/.bun`). Au moment du dernier inventaire, les binaires n'étaient pas résolus. Les réinstaller seulement si un projet les réclame.

## 5. MCP et secrets

```bash
cp kit/mcp.example.json ~/.cursor/mcp.json
```

Remplacer chaque `<REDACTED>` depuis le gestionnaire de mots de passe. Le fichier réel contient des jetons Figma, Postman et Google Stitch. Il reste sur la machine.

Hooks Claude Code observés dans `~/.claude/settings.json` : `PostToolUse` (Edit|Write), `PreCompact` et `TaskCompleted` appellent `jcodemunch-mcp`. Plugin activé : `floorplan@floorplan` (marketplace `haydenschmitty/floorplan`). Thème : `dark-ansi`.

## 6. Vérifier

```bash
flutter doctor
node -v
gh auth status
vercel whoami
firebase projects:list
python3 ~/My_Projects/workspace/scripts/sync.py
```

Le diff du sync doit être vide si la machine correspond au dernier inventaire publié. Sinon, c'est la liste de ce qui manque encore.

## 7. Reprendre les projets

L'ordre des dossiers :

```text
~/My_Projects/ReactJS
~/My_Projects/Flutter/Apps
~/My_Projects/Flutter/Packages
~/My_Projects/Appwrite
~/My_Projects/Directus
~/My_Projects/Serverpod
```

Cloner depuis GitHub les dépôts listés dans [Projets](../generated/projets.md). Les dépôts privés demandent `gh auth login` avant le clone. Chaque dépôt se lit ensuite via [Continuité](../methodes/continuite.md), pas via ce handbook.
