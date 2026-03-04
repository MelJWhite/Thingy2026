#!/usr/bin/env python3
"""generate-manifest.py — scans people/ directory and writes people/manifest.js"""

import os
import sys

EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

script_dir = os.path.dirname(os.path.abspath(__file__))
people_dir = os.path.join(script_dir, 'people')
output_path = os.path.join(people_dir, 'manifest.js')

if not os.path.isdir(people_dir):
    print(f"Error: people/ directory not found at {people_dir}", file=sys.stderr)
    sys.exit(1)

images = sorted(
    f for f in os.listdir(people_dir)
    if os.path.splitext(f)[1].lower() in EXTENSIONS
)

if not images:
    print(f"Warning: no image files found in {people_dir}", file=sys.stderr)

with open(output_path, 'w') as f:
    f.write('window.PEOPLE_MANIFEST = [\n')
    for i, img in enumerate(images):
        comma = ',' if i < len(images) - 1 else ''
        f.write(f'  "{img}"{comma}\n')
    f.write('];\n')

print(f"Written: {output_path} ({len(images)} images)")

# ── topics.js ──────────────────────────────────────────
topics_txt = os.path.join(script_dir, 'topics.txt')
topics_out = os.path.join(script_dir, 'topics.js')

if not os.path.isfile(topics_txt):
    print("Warning: topics.txt not found, skipping topics.js", file=sys.stderr)
else:
    topics = []
    with open(topics_txt, 'r') as tf:
        for line in tf:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            topics.append(line)

    with open(topics_out, 'w') as f:
        f.write('window.PANEL_TOPICS = [\n')
        for i, topic in enumerate(topics):
            escaped = topic.replace('\\', '\\\\').replace('"', '\\"')
            comma = ',' if i < len(topics) - 1 else ''
            f.write(f'  "{escaped}"{comma}\n')
        f.write('];\n')

    print(f"Written: {topics_out} ({len(topics)} topics)")
