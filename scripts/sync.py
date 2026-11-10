#!/usr/bin/env python3
"""Regenerate the living inventory from this machine.

Curated pages under docs/setup, docs/methodes and docs/stacks are written by hand.
This script only rewrites docs/generated, kit/personal-rules and kit/mcp.example.json.

It refuses to write if a secret-shaped token would land in the output.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()
GENERATED = ROOT / "docs" / "generated"
PERSONAL_RULES = ROOT / "kit" / "personal-rules"
PERSONAL_RULE_NAMES = {
    "ai-context-compression.mdc",
    "ui-design-director-github.mdc",
}

SECRET_RE = re.compile(
    r"(figd_[A-Za-z0-9_\-]{8,}"
    r"|PMAK-[A-Za-z0-9\-]{8,}"
    r"|sk-[A-Za-z0-9_\-]{10,}"
    r"|ghp_[A-Za-z0-9]{10,}"
    r"|github_pat_[A-Za-z0-9_]{10,}"
    r"|xox[baprs]-[A-Za-z0-9\-]{8,}"
    r"|AKIA[0-9A-Z]{16}"
    r"|AIza[0-9A-Za-z_\-]{20,}"
    r"|AQ\.[A-Za-z0-9_\-]{8,}"
    r"|eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{10,})"
)
SECRET_KEY_RE = re.compile(
    r"(token|secret|password|authorization|api[-_]?key|bearer)",
    re.I,
)

DESIGN_SKILLS = {
    "anti-ui-slop",
    "frontend-design",
    "true-ui-redesign",
    "typeui-fundamentals",
    "ui-design",
    "ui-design-brain",
    "ui-design-director",
    "ui-radar",
    "ui-ux-pro-max",
}

TOOL_CANDIDATES = [
    "node",
    "npm",
    "pnpm",
    "bun",
    "fnm",
    "git",
    "gh",
    "flutter",
    "dart",
    "java",
    "ruby",
    "python3",
    "uv",
    "uvx",
    "vercel",
    "firebase",
    "maestro",
    "shorebird",
    "cursor",
    "brew",
    "adb",
    "pod",
    "fastlane",
    "rg",
    "headroom",
    "jcodemunch-mcp",
]


def redact(value: str) -> str:
    return SECRET_RE.sub("<REDACTED>", value)


def assert_clean(text: str, label: str) -> None:
    match = SECRET_RE.search(text)
    if match:
        raise SystemExit(f"Refusing to write {label}: secret-shaped token detected")


def write(path: Path, text: str) -> None:
    assert_clean(text, str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run(cmd: list[str], timeout: int = 20) -> str:
    try:
        result = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return (result.stdout or result.stderr or "").strip()


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    data: dict[str, str] = {}
    key: str | None = None
    buf: list[str] = []
    for line in text[3:end].splitlines():
        if re.match(r"^[A-Za-z0-9_-]+:", line):
            if key:
                data[key] = " ".join(part.strip() for part in buf if part.strip())
            key, val = line.split(":", 1)
            buf = [val.strip()]
        else:
            buf.append(line)
    if key:
        data[key] = " ".join(part.strip() for part in buf if part.strip())
    for name in list(data):
        data[name] = data[name].strip(" >-|\"'")
        data[name] = re.sub(r"\s+", " ", data[name])
    return data


def skill_records(root: Path, group: str) -> list[dict[str, str]]:
    if not root.exists():
        return []
    records = []
    for skill in sorted(root.rglob("SKILL.md")):
        rel = skill.parent.relative_to(root).as_posix()
        if rel.startswith(".git"):
            continue
        meta = frontmatter(skill)
        remote = ""
        git_dir = skill.parent / ".git"
        if git_dir.exists():
            remote = run(["git", "-C", str(skill.parent), "remote", "get-url", "origin"])
        records.append(
            {
                "group": group,
                "path": rel,
                "name": meta.get("name", skill.parent.name),
                "description": meta.get("description", ""),
                "remote": remote,
            }
        )
    return records


def collect_cursor_plugin_skills() -> list[dict[str, str]]:
    local = HOME / ".cursor/plugins/local"
    if not local.exists():
        return []
    records = []
    for plugin_dir in sorted(path for path in local.iterdir() if path.is_dir()):
        meta = read_json(plugin_dir / ".cursor-plugin" / "plugin.json")
        remote = str(meta.get("repository") or "")
        skills_root = plugin_dir / "skills"
        if not skills_root.exists():
            continue
        for skill in sorted(skills_root.rglob("SKILL.md")):
            meta_skill = frontmatter(skill)
            records.append(
                {
                    "group": "cursor-plugin",
                    "path": skill.parent.relative_to(local).as_posix(),
                    "name": meta_skill.get("name", skill.parent.name),
                    "description": meta_skill.get("description", ""),
                    "remote": remote,
                }
            )
    return records


def collect_skills() -> list[dict[str, str]]:
    records = []
    records.extend(skill_records(HOME / ".cursor/skills", "cursor"))
    records.extend(skill_records(HOME / ".cursor/skills-cursor", "cursor-builtin"))
    records.extend(skill_records(HOME / ".claude/skills", "claude"))
    records.extend(skill_records(HOME / ".agents/skills", "agents"))
    records.extend(collect_cursor_plugin_skills())
    store = HOME / "Library/Application Support/Cursor/AgentStores"
    if store.exists():
        for skill in sorted(store.glob("**/skills/*/SKILL.md")):
            meta = frontmatter(skill)
            records.append(
                {
                    "group": "agent-store",
                    "path": str(skill.parent),
                    "name": meta.get("name", skill.parent.name),
                    "description": meta.get("description", ""),
                    "remote": "",
                }
            )
    return records


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def shown(path: str) -> str:
    text = path or ""
    home = str(HOME)
    if text.startswith(home):
        return "~" + text[len(home) :]
    return text or "—"


def collect_plugins() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    local = HOME / ".cursor/plugins/local"
    if local.exists():
        for plugin_dir in sorted(path for path in local.iterdir() if path.is_dir()):
            meta = read_json(plugin_dir / ".cursor-plugin" / "plugin.json")
            if not meta:
                meta = read_json(plugin_dir / "plugin.json")
            sha_file = plugin_dir / ".egm-source-sha"
            sha = sha_file.read_text(encoding="utf-8").strip()[:12] if sha_file.exists() else ""
            rows.append(
                {
                    "harness": "Cursor",
                    "name": str(meta.get("name") or plugin_dir.name),
                    "version": str(meta.get("version") or ""),
                    "scope": "user",
                    "path": shown(str(plugin_dir)),
                    "source": str(meta.get("repository") or ""),
                    "sha": sha,
                }
            )

    installed = read_json(HOME / ".claude/plugins/installed_plugins.json")
    markets = read_json(HOME / ".claude/plugins/known_marketplaces.json")
    plugins = installed.get("plugins", {})
    if isinstance(plugins, dict):
        for plugin_id, entries in plugins.items():
            if not isinstance(entries, list):
                continue
            marketplace = plugin_id.split("@", 1)[1] if "@" in plugin_id else ""
            market = markets.get(marketplace, {}) if isinstance(markets, dict) else {}
            source = ""
            if isinstance(market, dict):
                origin = market.get("source", {})
                if isinstance(origin, dict) and origin.get("repo"):
                    source = "https://github.com/" + str(origin["repo"])
            for item in entries:
                if not isinstance(item, dict):
                    continue
                sha = str(item.get("gitCommitSha") or "")[:12]
                rows.append(
                    {
                        "harness": "Claude Code",
                        "name": plugin_id,
                        "version": str(item.get("version") or ""),
                        "scope": str(item.get("scope") or ""),
                        "path": shown(str(item.get("installPath") or "")),
                        "source": source,
                        "sha": sha,
                    }
                )

    gemini = HOME / ".gemini/config/plugins"
    if gemini.exists():
        for plugin_dir in sorted(path for path in gemini.iterdir() if path.is_dir()):
            meta = read_json(plugin_dir / "plugin.json")
            rows.append(
                {
                    "harness": "Antigravity",
                    "name": str(meta.get("name") or plugin_dir.name),
                    "version": str(meta.get("version") or ""),
                    "scope": "user",
                    "path": shown(str(plugin_dir)),
                    "source": str(meta.get("repository") or ""),
                    "sha": "",
                }
            )
    return rows


def classify_skill(record: dict[str, str]) -> str:
    path = record["path"]
    name = record["name"]
    if record["group"] == "cursor-plugin":
        return "Plugin Cursor"
    if record["group"] == "cursor-builtin":
        return "Cursor intégré"
    if record["group"] == "claude":
        return "Claude Code"
    if record["group"] == "agents":
        return "Agents partagés"
    if record["group"] == "agent-store":
        return "Agent store"
    if path.startswith("ecc/") or name.startswith("ecc"):
        return "ECC"
    if "paul-mbou" in record.get("remote", ""):
        return "Personnel"
    if name in DESIGN_SKILLS or path in DESIGN_SKILLS:
        return "Design"
    return "Cursor personnel"


def collect_rules() -> list[dict[str, str]]:
    rules_dir = HOME / ".cursor/rules"
    rows = []
    if not rules_dir.exists():
        return rows
    for path in sorted(rules_dir.glob("*.mdc")):
        text = path.read_text(encoding="utf-8", errors="replace")
        title = path.stem
        description = ""
        always = "false"
        in_front = text.startswith("---")
        for line in text.splitlines():
            if in_front and line.strip() == "---" and title != path.stem:
                in_front = False
            if line.startswith("description:"):
                description = line.split(":", 1)[1].strip().strip('"')
            if line.startswith("alwaysApply:"):
                always = line.split(":", 1)[1].strip()
            if line.startswith("# "):
                title = line[2:].strip()
                break
        family = path.name.split("-")[0]
        rows.append(
            {
                "file": path.name,
                "title": title,
                "description": description,
                "alwaysApply": always,
                "family": family,
                "personal": path.name in PERSONAL_RULE_NAMES,
            }
        )
    return rows


def sanitize_mcp(raw: dict) -> dict:
    servers = raw.get("mcpServers", {})
    clean = {}
    for name, spec in servers.items():
        item = {"name": name}
        if "command" in spec:
            item["command"] = redact(str(spec.get("command", "")))
        args = []
        for arg in spec.get("args", []) or []:
            text = redact(str(arg))
            if "=" in text and SECRET_KEY_RE.search(text.split("=", 1)[0]):
                key = text.split("=", 1)[0]
                text = f"{key}=<REDACTED>"
            args.append(text)
        if args:
            item["args"] = args
        if spec.get("url"):
            item["url"] = redact(str(spec["url"]))
        headers = spec.get("headers") or {}
        if headers:
            item["headers"] = {
                key: "<REDACTED>" if SECRET_KEY_RE.search(key) or str(value) else key
                for key, value in headers.items()
            }
            item["headers"] = {key: "<REDACTED>" for key in headers}
        if spec.get("env"):
            item["env"] = {key: "<REDACTED>" for key in spec["env"]}
        clean[name] = item
    return clean


def collect_mcp() -> dict:
    path = HOME / ".cursor/mcp.json"
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return sanitize_mcp(raw)


def which(cmd: str) -> str:
    path = shutil.which(cmd)
    if path:
        return path
    extras = [
        HOME / ".local/bin" / cmd,
        HOME / "Library/pnpm" / cmd,
        HOME / ".bun/bin" / cmd,
        HOME / ".maestro/bin" / cmd,
        HOME / ".shorebird/bin" / cmd,
        HOME / "Libs/flutter/bin" / cmd,
        HOME / "Development/flutter/bin" / cmd,
    ]
    for candidate in extras:
        if candidate.exists():
            return str(candidate)
    return ""


def version_of(cmd: str, path: str) -> str:
    if not path:
        return ""
    output = run([path, "--version"])
    if not output:
        output = run([path, "-v"])
    line = output.splitlines()[0] if output else ""
    return redact(line)[:180]


def collect_tools() -> list[dict[str, str]]:
    rows = []
    seen = set()
    for cmd in TOOL_CANDIDATES:
        path = which(cmd)
        key = path or cmd
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            {
                "command": cmd,
                "path": path or "absent",
                "version": version_of(cmd, path) if path else "",
                "present": bool(path),
            }
        )
    return rows


def detect_stack(directory: Path) -> str:
    hints = []
    pubspec = directory / "pubspec.yaml"
    package = directory / "package.json"
    if pubspec.exists():
        text = pubspec.read_text(encoding="utf-8", errors="replace")
        hints.append("Flutter")
        for marker in ("flutter_riverpod", "riverpod", "firebase_core", "go_router", "freezed", "shorebird"):
            if marker in text:
                hints.append(marker)
    if package.exists():
        try:
            data = json.loads(package.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        if "astro" in deps:
            hints.append("Astro")
        if "react" in deps:
            hints.append("React")
        if "vue" in deps or (directory / "nuxt.config.ts").exists():
            hints.append("Vue/Nuxt")
        if "tailwindcss" in deps or "@tailwindcss/vite" in deps:
            hints.append("Tailwind")
        if "appwrite" in deps or "node-appwrite" in deps:
            hints.append("Appwrite")
        if "vite" in deps:
            hints.append("Vite")
        if "firebase" in deps:
            hints.append("Firebase")
    if (directory / "nuxt.config.ts").exists() and "Vue/Nuxt" not in hints:
        hints.append("Nuxt")
    return ", ".join(dict.fromkeys(hints))


def collect_local_projects() -> list[dict[str, str]]:
    base = HOME / "My_Projects"
    rows = []
    if not base.exists():
        return rows
    candidates = []
    for child in sorted(base.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        if child.name in {"Flutter", "ReactJS"}:
            for sub in sorted(child.iterdir()):
                if not sub.is_dir():
                    continue
                if sub.name in {"Apps", "Packages"}:
                    for app in sorted(sub.iterdir()):
                        if app.is_dir():
                            candidates.append(app)
                else:
                    candidates.append(sub)
        else:
            candidates.append(child)
            for sub in sorted(child.iterdir()):
                if sub.is_dir() and not sub.name.startswith(".") and sub.name not in {"node_modules", "build", "dist"}:
                    if (sub / "pubspec.yaml").exists() or (sub / "package.json").exists():
                        candidates.append(sub)
    seen = set()
    for path in candidates:
        if path in seen or not path.is_dir():
            continue
        seen.add(path)
        stack = detect_stack(path)
        if not stack and path.parent.name not in {"Apps", "Packages", "ReactJS", "Flutter"}:
            stack = "dossier"
        if not stack:
            continue
        rows.append(
            {
                "name": path.name,
                "path": str(path.relative_to(HOME)),
                "stack": stack,
            }
        )
    return rows


def collect_github() -> list[dict]:
    raw = run(
        [
            "gh",
            "repo",
            "list",
            "--limit",
            "100",
            "--json",
            "name,description,isPrivate,url,primaryLanguage,updatedAt",
        ],
        timeout=40,
    )
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []
    return data


def stamp() -> str:
    now = datetime.now(timezone.utc).astimezone()
    return now.strftime("%Y-%m-%d %H:%M %Z")


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [cell.replace("|", "\\|").replace("\n", " ") for cell in row]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def render_skills(skills: list[dict[str, str]], when: str) -> str:
    buckets: dict[str, list[dict[str, str]]] = {}
    for record in skills:
        buckets.setdefault(classify_skill(record), []).append(record)
    order = ["Personnel", "Plugin Cursor", "Design", "Cursor personnel", "ECC", "Cursor intégré", "Claude Code", "Agents partagés", "Agent store"]
    lines = [
        "<!-- generated by scripts/sync.py — do not edit by hand -->",
        "",
        "# Skills",
        "",
        f"Généré le {when}. {len(skills)} fichiers `SKILL.md` détectés sur cette machine.",
        "",
        "Les skills personnels se réinstallent par `git clone` (voir Nouvelle machine). "
        "ECC se réinstalle depuis [affaan-m/ECC](https://github.com/affaan-m/ECC). "
        "Les skills Cursor intégrés reviennent avec l'application. "
        "Ceux d'un plugin Cursor restent dans `~/.cursor/plugins/local/<plugin>/skills`, avec `agents/` et `resources/`.",
        "",
    ]
    for bucket in order:
        items = buckets.get(bucket, [])
        if not items:
            continue
        lines.append(f"## {bucket} ({len(items)})")
        lines.append("")
        rows = []
        for item in items:
            remote = item["remote"] or "—"
            desc = item["description"][:240]
            rows.append([f"`{item['name']}`", f"`{item['path']}`", remote, desc])
        lines.append(md_table(["Skill", "Chemin", "Remote", "Rôle"], rows))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_rules(rules: list[dict[str, str]], when: str) -> str:
    lines = [
        "<!-- generated by scripts/sync.py — do not edit by hand -->",
        "",
        "# Règles Cursor",
        "",
        f"Généré le {when}. {len(rules)} fichiers dans `~/.cursor/rules`.",
        "",
        "Les deux règles personnelles sont copiées dans `kit/personal-rules/` à chaque sync "
        "et restaurées par `scripts/bootstrap.sh`. Le reste est la bibliothèque ECC : "
        "la réinstaller, puis comparer cette liste.",
        "",
        "## Règles personnelles",
        "",
    ]
    personal = [rule for rule in rules if rule["personal"]]
    if personal:
        lines.append(md_table(
            ["Fichier", "Titre", "alwaysApply", "Description"],
            [[f"`{r['file']}`", r["title"], r["alwaysApply"], r["description"]] for r in personal],
        ))
    else:
        lines.append("Aucune règle personnelle détectée.")
    lines.extend(["", "## Bibliothèque", ""])
    families: dict[str, list[dict[str, str]]] = {}
    for rule in rules:
        if rule["personal"]:
            continue
        families.setdefault(rule["family"], []).append(rule)
    for family in sorted(families):
        items = families[family]
        names = ", ".join(f"`{item['file']}`" for item in items)
        lines.append(f"- **{family}** ({len(items)}) — {names}")
    lines.append("")
    return "\n".join(lines)


def render_mcp(servers: dict, when: str) -> str:
    lines = [
        "<!-- generated by scripts/sync.py — do not edit by hand -->",
        "",
        "# Serveurs MCP",
        "",
        f"Généré le {when} depuis `~/.cursor/mcp.json`.",
        "",
        "Les valeurs de clés, tokens et en-têtes d'authentification sont remplacées par `<REDACTED>`. "
        "Le fichier d'exemple versionné est `kit/mcp.example.json`. "
        "Sur une nouvelle machine, recréer `~/.cursor/mcp.json` et remplir les secrets depuis le gestionnaire de mots de passe.",
        "",
    ]
    if not servers:
        lines.append("Aucun serveur MCP détecté.")
        return "\n".join(lines) + "\n"
    for name, spec in servers.items():
        lines.append(f"## {name}")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(spec, indent=2, ensure_ascii=False))
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def render_tools(tools: list[dict[str, str]], when: str) -> str:
    present = [tool for tool in tools if tool["present"]]
    absent = [tool for tool in tools if not tool["present"]]
    lines = [
        "<!-- generated by scripts/sync.py — do not edit by hand -->",
        "",
        "# Outils détectés",
        "",
        f"Généré le {when}. Présents : {len(present)}. Absents du PATH et des emplacements connus : {len(absent)}.",
        "",
        "Un outil retiré de la machine disparaît de la colonne Présent au prochain `python3 scripts/sync.py`.",
        "",
        "## Présents",
        "",
        md_table(
            ["Commande", "Chemin", "Version"],
            [[f"`{t['command']}`", f"`{t['path']}`", t["version"] or "—"] for t in present],
        ),
        "",
        "## Absents",
        "",
    ]
    if absent:
        lines.append(", ".join(f"`{tool['command']}`" for tool in absent))
    else:
        lines.append("Aucun.")
    lines.append("")
    return "\n".join(lines)


def render_projects(local: list[dict[str, str]], github: list[dict], when: str) -> str:
    lines = [
        "<!-- generated by scripts/sync.py — do not edit by hand -->",
        "",
        "# Projets",
        "",
        f"Généré le {when}.",
        "",
        "Ce dépôt est public. Les noms de dépôts privés GitHub apparaissent ici parce qu'ils font partie du workspace à restaurer.",
        "",
        "## Dossiers locaux (`~/My_Projects`)",
        "",
        md_table(
            ["Nom", "Chemin", "Stack détectée"],
            [[p["name"], f"`{p['path']}`", p["stack"] or "—"] for p in local],
        ),
        "",
        "## GitHub `paul-mbou`",
        "",
    ]
    if github:
        rows = []
        for repo in github:
            lang = (repo.get("primaryLanguage") or {}) or {}
            rows.append([
                repo.get("name", ""),
                "privé" if repo.get("isPrivate") else "public",
                lang.get("name", "—") if isinstance(lang, dict) else "—",
                (repo.get("description") or "—")[:140],
                repo.get("url", ""),
            ])
        lines.append(md_table(["Dépôt", "Visibilité", "Langage", "Description", "URL"], rows))
    else:
        lines.append("`gh repo list` n'a rien renvoyé. Relancer le sync une fois `gh auth status` valide.")
    lines.append("")
    return "\n".join(lines)


def render_plugins(plugins: list[dict[str, str]], when: str) -> str:
    lines = [
        "<!-- generated by scripts/sync.py — do not edit by hand -->",
        "",
        "# Plugins",
        "",
        f"Généré le {when}. {len(plugins)} plugins au scope utilisateur.",
        "",
        "Cursor découvre `~/.cursor/plugins/local`. "
        "Claude Code lit `~/.claude/plugins/installed_plugins.json`. "
        "Antigravity lit `~/.gemini/config/plugins`. "
        "Un plugin retiré de la machine disparaît au prochain sync.",
        "",
    ]
    if not plugins:
        lines.append("Aucun plugin détecté.")
        lines.append("")
        return "\n".join(lines)
    harnesses: dict[str, list[dict[str, str]]] = {}
    for plugin in plugins:
        harnesses.setdefault(plugin["harness"], []).append(plugin)
    for harness in ("Cursor", "Claude Code", "Antigravity"):
        items = harnesses.get(harness, [])
        if not items:
            continue
        lines.append(f"## {harness} ({len(items)})")
        lines.append("")
        lines.append(md_table(
            ["Plugin", "Version", "Scope", "Chemin", "Source", "Commit"],
            [[
                f"`{item['name']}`",
                item["version"] or "—",
                item["scope"] or "—",
                f"`{item['path']}`",
                item["source"] or "—",
                f"`{item['sha']}`" if item["sha"] else "—",
            ] for item in items],
        ))
        lines.append("")
    return "\n".join(lines)


def render_index(when: str, counts: dict[str, int]) -> str:
    return f"""<!-- generated by scripts/sync.py — do not edit by hand -->

# Inventaire vivant

Généré le {when}.

| Catalogue | Entrées |
| --- | ---: |
| Skills | {counts['skills']} |
| Plugins | {counts['plugins']} |
| Règles Cursor | {counts['rules']} |
| Serveurs MCP | {counts['mcp']} |
| Outils présents | {counts['tools']} |
| Projets locaux | {counts['local']} |
| Dépôts GitHub | {counts['github']} |

Après un ajout ou un retrait, lancer `python3 scripts/sync.py`, relire le diff, puis commit et push. GitHub Pages se reconstruit sur `main`.
"""


def copy_personal_rules() -> None:
    source = HOME / ".cursor/rules"
    if PERSONAL_RULES.exists():
        for old in PERSONAL_RULES.glob("*.mdc"):
            if old.name not in PERSONAL_RULE_NAMES:
                old.unlink()
    PERSONAL_RULES.mkdir(parents=True, exist_ok=True)
    for name in sorted(PERSONAL_RULE_NAMES):
        src = source / name
        if not src.exists():
            continue
        text = src.read_text(encoding="utf-8")
        assert_clean(text, name)
        (PERSONAL_RULES / name).write_text(text, encoding="utf-8")


def main() -> None:
    when = stamp()
    skills = collect_skills()
    plugins = collect_plugins()
    rules = collect_rules()
    mcp = collect_mcp()
    tools = collect_tools()
    local = collect_local_projects()
    github = collect_github()

    write(GENERATED / "skills.md", render_skills(skills, when))
    write(GENERATED / "plugins.md", render_plugins(plugins, when))
    write(GENERATED / "rules.md", render_rules(rules, when))
    write(GENERATED / "mcp.md", render_mcp(mcp, when))
    write(GENERATED / "outils.md", render_tools(tools, when))
    write(GENERATED / "projets.md", render_projects(local, github, when))
    write(
        GENERATED / "index.md",
        render_index(
            when,
            {
                "skills": len(skills),
                "plugins": len(plugins),
                "rules": len(rules),
                "mcp": len(mcp),
                "tools": sum(1 for tool in tools if tool["present"]),
                "local": len(local),
                "github": len(github),
            },
        ),
    )
    inventory = {
        "generatedAt": when,
        "skills": skills,
        "plugins": plugins,
        "rules": rules,
        "mcp": mcp,
        "tools": tools,
        "localProjects": local,
        "github": [
            {
                "name": repo.get("name"),
                "private": repo.get("isPrivate"),
                "url": repo.get("url"),
                "description": repo.get("description") or "",
            }
            for repo in github
        ],
    }
    payload = json.dumps(inventory, indent=2, ensure_ascii=False) + "\n"
    write(ROOT / "inventory.json", payload)
    example = {
        "_comment": "Modèle sans secrets. Copier vers ~/.cursor/mcp.json et remplir les jetons localement.",
        "mcpServers": mcp,
    }
    write(ROOT / "kit" / "mcp.example.json", json.dumps(example, indent=2, ensure_ascii=False) + "\n")
    copy_personal_rules()
    print(f"Synced at {when}")


if __name__ == "__main__":
    main()
