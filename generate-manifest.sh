#!/usr/bin/env bash
# generate-manifest.sh — scans people/ directory and writes people/manifest.js

set -euo pipefail

PEOPLE_DIR="$(dirname "$0")/people"
OUTPUT="$PEOPLE_DIR/manifest.js"

if [ ! -d "$PEOPLE_DIR" ]; then
    echo "Error: people/ directory not found" >&2
    exit 1
fi

# Collect image files, sorted
images=()
while IFS= read -r -d '' f; do
    images+=("$(basename "$f")")
done < <(find "$PEOPLE_DIR" -maxdepth 1 \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.gif' -o -iname '*.webp' \) -print0 | sort -z)

if [ ${#images[@]} -eq 0 ]; then
    echo "Warning: no image files found in $PEOPLE_DIR" >&2
fi

# Write JS (works with file:// URLs unlike fetch+JSON)
{
    printf 'window.PEOPLE_MANIFEST = [\n'
    for i in "${!images[@]}"; do
        if [ $i -lt $(( ${#images[@]} - 1 )) ]; then
            printf '  "%s",\n' "${images[$i]}"
        else
            printf '  "%s"\n' "${images[$i]}"
        fi
    done
    printf '];\n'
} > "$OUTPUT"

echo "Written: $OUTPUT (${#images[@]} images)"

# ── topics.js ──────────────────────────────────────────
TOPICS_TXT="$(dirname "$0")/topics.txt"
TOPICS_OUT="$(dirname "$0")/topics.js"

if [ ! -f "$TOPICS_TXT" ]; then
    echo "Warning: topics.txt not found, skipping topics.js" >&2
else
    topics=()
    while IFS= read -r line; do
        # Skip blank lines and # comments
        [[ -z "$line" || "$line" == \#* ]] && continue
        topics+=("$line")
    done < "$TOPICS_TXT"

    {
        printf 'window.PANEL_TOPICS = [\n'
        for i in "${!topics[@]}"; do
            # Escape backslashes then double-quotes
            escaped="${topics[$i]//\\/\\\\}"
            escaped="${escaped//\"/\\\"}"
            if [ $i -lt $(( ${#topics[@]} - 1 )) ]; then
                printf '  "%s",\n' "$escaped"
            else
                printf '  "%s"\n' "$escaped"
            fi
        done
        printf '];\n'
    } > "$TOPICS_OUT"

    echo "Written: $TOPICS_OUT (${#topics[@]} topics)"
fi
