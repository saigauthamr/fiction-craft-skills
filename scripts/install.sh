#!/bin/sh
# Install the skills into an agent's skills folder, by link (default) or by copy.
#
# Run it from your story project's folder:
#   install.sh                  ./.claude/skills   Claude Code, for this project
#   install.sh --agents         ./.agents/skills   the shared folder read by Codex, Gemini CLI, OpenCode,
#                                                  Cursor, and GitHub Copilot, for this project
#   install.sh --global         ~/.claude/skills   Claude Code, every session (the story skills then
#                                                  compete with all your other skills)
#   install.sh --agents --global                   ~/.agents/skills, the same for the shared folder
#   install.sh <folder>                            any other folder
# Options:
#   --copy      copy the skills instead of linking them, for tools that do not follow links
#   --help      show this text
#
# Install into ONE folder per tool. Tools that read both .claude/skills and .agents/skills would
# otherwise list every skill twice.
# Re-running is safe. A real folder or file already at a skill's name is never overwritten, except a
# copy this script made earlier (marked by a .installed-by-fiction-craft-skills file), which is refreshed.
set -eu

repo=$(cd "$(dirname "$0")/.." && pwd)
marker=.installed-by-fiction-craft-skills
layout=claude scope=project mode=link target=

usage() { sed -n '2,19p' "$0" | sed 's/^# \{0,1\}//'; }

while [ $# -gt 0 ]; do
  case "$1" in
    --agents) layout=agents ;;
    --claude) layout=claude ;;
    --global) scope=global ;;
    --copy) mode=copy ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "unknown option: $1 (see --help)" >&2; exit 2 ;;
    *) target=$1 ;;
  esac
  shift
done

if [ -z "$target" ]; then
  if [ "$scope" = global ]; then base=$HOME; else base=$(pwd); fi
  if [ "$scope" = project ] && [ "$(pwd -P)" = "$(cd "$repo" && pwd -P)" ]; then
    echo "Run this from your story project's folder, or give a target folder (or --global)." >&2
    exit 2
  fi
  target="$base/.$layout/skills"
fi
mkdir -p "$target"

status=0
# Remove dead links that point into this library (skills that were renamed or removed).
for dest in "$target"/*; do
  if [ -L "$dest" ] && [ ! -e "$dest" ]; then
    case "$(readlink "$dest")" in
      "$repo"/skills/*)
        rm "$dest"
        echo "removed stale link $(basename "$dest")" ;;
    esac
  fi
done

for dir in "$repo"/skills/*/; do
  name=$(basename "$dir")
  dest="$target/$name"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    if [ -L "$dest" ]; then
      rm "$dest"
    elif [ -d "$dest" ] && [ -f "$dest/$marker" ]; then
      rm -rf "$dest"
    else
      echo "skip $name: $dest exists and is not ours" >&2
      status=1
      continue
    fi
  fi
  if [ "$mode" = copy ]; then
    cp -R "${dir%/}" "$dest"
    find "$dest" -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true
    : > "$dest/$marker"
    echo "copied $name"
  else
    ln -s "${dir%/}" "$dest"
    echo "linked $name"
  fi
done
echo "installed into $target"
exit $status
