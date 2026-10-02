"""Write manifest.json: every file under font/ and palette/, as paths relative to this folder.

Static hosts such as GitHub Pages have no directory listings, so the page reads this list to
discover font families, fonts and palettes. The Pages workflow runs this on every deploy; run it
by hand only if you want to commit an up-to-date manifest.json.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOTS = ('font', 'palette')

files = []
for root in ROOTS:
    for dirpath, dirnames, filenames in os.walk(os.path.join(HERE, root)):
        dirnames.sort()
        for name in sorted(filenames):
            files.append(os.path.relpath(os.path.join(dirpath, name), HERE).replace(os.sep, '/'))

with open(os.path.join(HERE, 'manifest.json'), 'w', encoding='utf-8', newline='\n') as f:
    json.dump({'files': files}, f, indent=1)
    f.write('\n')

print(f'manifest.json: {len(files)} files')
