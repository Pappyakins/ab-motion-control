#!/usr/bin/env python3
"""Build www/index.html from www/index.template.html + data/ab-motion-control-data.json.

The data is inlined as AB_DATA so the single-file app works offline from
file:// (fetch() is blocked on file:// in Chrome), on GitHub Pages, and inside
Capacitor (which serves www/ over http). Run assemble.py first, then this.
Also copies the JSON into www/ for reference and future fetch-based use.
"""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "www" / "index.template.html"
DATA = ROOT / "data" / "ab-motion-control-data.json"
OUT = ROOT / "www" / "index.html"

data = json.loads(DATA.read_text())
html = TEMPLATE.read_text()
token = "/*__AB_DATA__*/"
assert token in html, "template placeholder missing"
blob = "const AB_DATA = " + json.dumps(data) + ";"
html = html.replace(token, blob)
OUT.write_text(html)
shutil.copyfile(DATA, ROOT / "www" / "ab-motion-control-data.json")
print(f"built {OUT} ({OUT.stat().st_size} bytes, "
      f"{data['stats']['families']} families, "
      f"{data['stats']['modules']} modules, "
      f"{data['stats']['lessons']} lessons)")
