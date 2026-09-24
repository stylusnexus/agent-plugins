#!/usr/bin/env python3
"""Search the bundled metric reference; no network or writes."""
import argparse
import json
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('query', nargs='?', default='')
    p.add_argument('--category', default='')
    p.add_argument('--json', action='store_true')
    a=p.parse_args()
    records=json.loads((Path(__file__).resolve().parents[1]/'skills/pm-objectives/references/metrics-catalog.json').read_text())
    matches=[r for r in records if a.query.casefold() in ' '.join(r.values()).casefold() and (not a.category or r['category'].casefold()==a.category.casefold())]
    if a.json:print(json.dumps(matches,indent=2,ensure_ascii=False))
    else:
        for r in matches:print(f"{r['id']} — {r['name']} [{r['category']}]\n{r['definition']}\nCaution: {r['caution']}\n")
        if not matches:print('No matching metrics. Try a broader term or omit --category.')
if __name__=='__main__':main()
