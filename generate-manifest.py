#!/usr/bin/env python3
"""generate-manifest.py — scans people/ directory and writes people/manifest.json"""

import json
import os
import sys

EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

script_dir = os.path.dirname(os.path.abspath(__file__))
people_dir = os.path.join(script_dir, 'people')
output_path = os.path.join(people_dir, 'manifest.json')

if not os.path.isdir(people_dir):
    print(f"Error: people/ directory not found at {people_dir}", file=sys.stderr)
    sys.exit(1)

images = sorted(
    f for f in os.listdir(people_dir)
    if os.path.splitext(f)[1].lower() in EXTENSIONS
)

if not images:
    print(f"Warning: no image files found in {people_dir}", file=sys.stderr)

manifest = {"images": images}

with open(output_path, 'w') as f:
    json.dump(manifest, f, indent=2)
    f.write('\n')

print(f"Written: {output_path} ({len(images)} images)")
