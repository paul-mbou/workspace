#!/usr/bin/env bash
# One-shot restore of Paul Mbou's workstation contracts.
# Does not install secrets. Fill ~/.cursor/mcp.json from the password manager.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOME_DIR="${HOME}"

say() { printf '\n== %s\n' "$1"; }

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "Ce script cible macOS (Darwin). Adapter les chemins avant de continuer sur un autre OS."
  exit 1
fi

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew est absent. Installer https://brew.sh puis relancer."
  exit 1
fi

say "Outils de base"
brew install git gh fnm ripgrep cocoapods fastlane uv || true
brew install --cask cursor android-studio || true

say "Node via fnm"
if command -v fnm >/dev/null 2>&1; then
  eval "$(fnm env --shell bash)"
  fnm install 24
  fnm default 24
fi

say "Dossiers de travail"
mkdir -p "${HOME_DIR}/My_Projects/Flutter/Apps" \
  "${HOME_DIR}/My_Projects/Flutter/Packages" \
  "${HOME_DIR}/My_Projects/ReactJS" \
  "${HOME_DIR}/.cursor/skills" \
  "${HOME_DIR}/.cursor/rules" \
  "${HOME_DIR}/.local/bin"

say "Flutter stable dans ~/Libs/flutter"
if [[ ! -x "${HOME_DIR}/Libs/flutter/bin/flutter" ]]; then
  mkdir -p "${HOME_DIR}/Libs"
  git clone https://github.com/flutter/flutter.git -b stable "${HOME_DIR}/Libs/flutter"
fi

say "Skills personnels"
clone_skill() {
  local name="$1"
  local url="$2"
  local dest="${HOME_DIR}/.cursor/skills/${name}"
  if [[ -d "${dest}/.git" ]]; then
    git -C "${dest}" pull --ff-only || true
  else
    git clone "${url}" "${dest}"
  fi
}
clone_skill ai-continuity-kit https://github.com/paul-mbou/ai-continuity-kit.git
clone_skill knowledge-memory-gen https://github.com/paul-mbou/knowledge-memory-gen.git
clone_skill payment-gateway https://github.com/paul-mbou/payment-gateway.git
clone_skill payunit-integration https://github.com/paul-mbou/payunit-integration.git
clone_skill weekly-features-recap https://github.com/paul-mbou/weekly-features-recap.git
clone_skill ui-design-director https://github.com/Endeavor068/ui-design-director.git

say "Règles personnelles"
cp -f "${ROOT}/kit/personal-rules/"*.mdc "${HOME_DIR}/.cursor/rules/"

say "Ce que ce script ne fait pas"
cat <<'EOF'
- Xcode s'installe depuis le Mac App Store, puis : sudo xcodebuild -license accept && xcodebuild -runFirstLaunch
- Android Studio : ouvrir une fois pour installer SDK, platform-tools et licences.
- ECC (skills + règles de langages) : réinstaller depuis https://github.com/affaan-m/ECC puis comparer docs/generated/rules.md
- Secrets MCP : copier kit/mcp.example.json vers ~/.cursor/mcp.json et remplacer <REDACTED> depuis le gestionnaire de mots de passe. Ne jamais committer ce fichier.
- PATH shell : reprendre le bloc documenté dans docs/setup/nouvelle-machine.md
- jCodeMunch : uv tool install jcodemunch-mcp   (binaire observé : ~/.local/bin/jcodemunch-mcp, lancé via uvx)
- Headroom : uv tool install headroom-ai        (binaire observé : ~/.local/bin/headroom)
- Maestro : https://maestro.mobile.dev  → ~/.maestro/bin
- Shorebird : https://shorebird.dev     → ~/.shorebird/bin
- Firebase CLI et Vercel CLI : npm install -g firebase-tools vercel
- Authentifications à refaire à la main : gh auth login, vercel login, firebase login, flutter doctor
EOF

say "Terminé"
echo "Comparer ensuite la machine avec le site : python3 ${ROOT}/scripts/sync.py"
