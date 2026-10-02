"""Assemble the GitHub Pages site into OUT_DIR (default _site).

- Runs every tool's build_manifest.py (if it has one) so its manifest matches the files.
- Copies every top-level folder that has an index.html (one tool per folder).
- Writes a root index.html linking to each tool.
"""
import html
import os
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, '_site'))

tools = sorted(
    d for d in os.listdir(REPO)
    if not d.startswith(('.', '_')) and os.path.isfile(os.path.join(REPO, d, 'index.html'))
)

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)

for tool in tools:
    src = os.path.join(REPO, tool)
    manifest_script = os.path.join(src, 'build_manifest.py')
    if os.path.isfile(manifest_script):
        subprocess.run([sys.executable, manifest_script], check=True)
    shutil.copytree(src, os.path.join(OUT, tool), ignore=shutil.ignore_patterns('*.py', '__pycache__'))
    print(f'  {tool}/')

items = '\n'.join(f'    <li><a href="{html.escape(t)}/">{html.escape(t)}</a></li>' for t in tools)
with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PD2 Tools</title>
<style>
  body {{ margin: 0; background: #111013; color: #e6e1d6; font: 15px/1.5 system-ui, Segoe UI, sans-serif; }}
  main {{ max-width: 640px; margin: 48px auto; padding: 0 16px; }}
  h1 {{ color: #c7b377; font-weight: 600; }}
  a {{ color: #c7b377; }}
</style>
</head>
<body>
<main>
  <h1>PD2 Tools</h1>
  <ul>
{items}
  </ul>
</main>
</body>
</html>
""")

# Serve files as-is (no Jekyll processing).
open(os.path.join(OUT, '.nojekyll'), 'w').close()
print(f'Built {len(tools)} tool(s) into {OUT}')
