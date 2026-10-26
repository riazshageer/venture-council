#!/bin/sh
set -eu

PROVIDER="${1:-all}"
REPOSITORY="${BOARDROOM_GITHUB_REPOSITORY:-riazshageer/venture-council}"

case "$PROVIDER" in
  all|codex|claude) ;;
  *) echo "Usage: install.sh [all|codex|claude]" >&2; exit 2 ;;
esac

if ! command -v python3 >/dev/null 2>&1; then
  echo "Boardroom requires Python 3.10 or later (python3)." >&2
  exit 1
fi
if ! command -v curl >/dev/null 2>&1; then
  echo "Remote installation requires curl." >&2
  exit 1
fi
if ! command -v tar >/dev/null 2>&1; then
  echo "Remote installation requires tar." >&2
  exit 1
fi

TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT HUP INT TERM
ARCHIVE="$TEMP_DIR/boardroom.tar.gz"
URL="https://github.com/$REPOSITORY/releases/latest/download/boardroom.tar.gz"

echo "Downloading Boardroom from $URL"
curl --fail --location --silent --show-error "$URL" --output "$ARCHIVE"
tar -xzf "$ARCHIVE" -C "$TEMP_DIR"
python3 "$TEMP_DIR/boardroom/scripts/install_global.py" --provider "$PROVIDER"
