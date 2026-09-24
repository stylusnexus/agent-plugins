#!/usr/bin/env python3
"""Validate local discovery JSONL and print a traceable Markdown digest; no network or writes."""
import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path

SOURCES = ('customer_interview', 'sales_call_note', 'support_ticket', 'survey',
           'product_analytics', 'usability_test', 'site_search_log', 'experiment',
           'app_store_review', 'competitor_product',
           'synthetic_research')
STATUSES = ('observation', 'reported', 'inference', 'hypothesis', 'synthetic')


def clean(value):
    return str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('|', '&#124;').replace('\n', ' ').replace('\r', ' ')


def read_records(path):
    records, seen = [], set()
    for line_no, line in enumerate(Path(path).read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError('expected a JSON object')
            for key in ('id', 'source_type', 'status', 'summary'):
                if not isinstance(row.get(key), str) or not row[key].strip():
                    raise ValueError(f'{key} must be a nonempty string')
            if row['id'] in seen:
                raise ValueError(f'duplicate id: {row["id"]}')
            if row['source_type'] not in SOURCES or row['status'] not in STATUSES:
                raise ValueError('unrecognized source_type or status')
            if row['source_type'] == 'synthetic_research' and row['status'] != 'synthetic':
                raise ValueError('synthetic_research must have synthetic status')
            for key in ('source_ref', 'date', 'segment', 'theme'):
                if key in row and not isinstance(row[key], str):
                    raise ValueError(f'{key} must be a string')
            if row.get('date'):
                if date.fromisoformat(row['date']).isoformat() != row['date']:
                    raise ValueError('date must be YYYY-MM-DD')
            seen.add(row['id'])
            records.append(row)
        except (ValueError, TypeError) as exc:
            raise ValueError(f'line {line_no}: {exc}') from exc
    return records


def render(rows):
    counts = Counter(r['source_type'] for r in rows)
    out = ['# Discovery evidence digest', '',
           f'{len(rows)} records. Counts describe submitted records, not unique people, prevalence or validation.', '',
           'Source references are not opened or verified. Labels are supplied by the user; this tool cannot detect mislabelled AI text.', '',
           '## Source coverage', '', '| Source | Records |', '|---|---:|']
    out += [f'| {s} | {counts[s]} |' for s in SOURCES]
    out += ['', 'Unused sources are options, not mandatory research tasks.', '',
            '## Traceable records', '', '| ID | Source type / status | Segment | Date | Summary | Source reference | Theme |', '|---|---|---|---|---|---|---|']
    for r in rows:
        values = [r['id'], r['source_type'] + ' / ' + r['status'], r.get('segment') or 'unknown',
                  r.get('date') or 'unknown', r['summary'], r.get('source_ref') or 'MISSING', r.get('theme') or 'unassigned']
        out.append('| ' + ' | '.join(map(clean, values)) + ' |')
    out += ['', '## Review flags', '']
    flags = []
    for r in rows:
        missing = [k for k in ('source_ref', 'date', 'segment') if not r.get(k, '').strip()]
        if missing:
            flags.append(f'- {clean(r["id"])}: missing ' + ', '.join(missing))
        if r['status'] == 'synthetic':
            flags.append(f'- {clean(r["id"])}: synthetic material; use for hypotheses, never customer evidence.')
    out += flags or ['No missing-provenance flags. This does not establish evidence quality.']
    out += ['', '## Human synthesis', '',
            'Check source independence, recruitment bias, contradictory observations and alternate explanations. Repeated reports may describe the same event. Select a decision-changing follow-up; do not treat volume as priority.']
    return '\n'.join(out) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='UTF-8 JSONL, one evidence record per line')
    args = parser.parse_args()
    try:
        report = render(read_records(args.input))
    except (OSError, ValueError) as exc:
        parser.exit(2, f'Error: {exc}\n')
    print(report, end='')


if __name__ == '__main__':
    main()
