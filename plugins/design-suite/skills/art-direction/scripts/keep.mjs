#!/usr/bin/env node
// tasteskill / keep — check that a redesign kept what the old page did.
//
//   node keep.mjs record <url>... [--out DIR] [--width 1440] [--force] [--json]
//   node keep.mjs check  <url>... [--out DIR] [--width 1440] [--drop "<kind>:<value> -- <reason>"]... [--json]
//
// record  opens each page in a real browser and writes what it does to <out>/before.json (default
//         .taste-skill/kept). It will not overwrite an earlier record without --force,
//         and --force replaces EVERY recorded page, so record all pages in one command.
// check   opens the same pages again (the port and host may differ: pages match by path), writes
//         after.json and report.json, and reports what was lost: links, forms, fields, buttons,
//         inline handlers, test hooks, headings and in-page anchors. A loss is a FAIL unless it is
//         named with --drop and a reason of at least 10 characters. A --drop that matches nothing is a
//         FAIL too. A report with only warnings (including "nothing recorded") exits 0 and prints them.
//
// Exit code 0 = no FAIL. Exit code 1 = at least one FAIL. Exit code 2 = usage error (no record,
// a URL with no record or that cannot be reached, a bad flag).
//
// What it sees: the page after load, as a visitor's browser builds it. What it does not see: handlers
// attached by scripts (framework event handlers), logins, state after interaction. Buttons with no
// accessible name are counted and not recorded. Zero dependencies: drives an installed Chrome. Node 22+.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { Browser, sleep } from './lib/cdp.mjs';
import { snapshot, normPath, parseDrop, compare } from './lib/kept.mjs';

const NOT_CHECKED = 'Not checked: handlers attached by scripts (framework event handlers), logins, state after interaction.';
const USAGE = 'usage: node keep.mjs record <url>... [--out DIR] [--width 1440] [--force] [--json]\n' +
  '       node keep.mjs check <url>... [--out DIR] [--width 1440] [--drop "<kind>:<value> -- <reason>"]... [--json]';
const LABELS = { href: 'links', form: 'forms', field: 'fields', button: 'buttons', handler: 'handlers', hook: 'hooks', heading: 'headings', anchor: 'anchors' };

const args = process.argv.slice(2);
const flag = (name, def) => { const i = args.indexOf('--' + name); if (i === -1) return def; const v = args[i + 1]; args.splice(i, 2); return v; };
const has = (name) => { const i = args.indexOf('--' + name); if (i === -1) return false; args.splice(i, 1); return true; };
const fail = (msg) => { console.error(msg); process.exit(2); };

const dropSpecs = [];
while (args.includes('--drop')) {
  const v = flag('drop');
  if (v === undefined || v.startsWith('--')) fail('--drop needs a value\n' + USAGE);
  dropSpecs.push(v);
}
const outFlag = flag('out', '.taste-skill/kept');
const widthFlag = flag('width');
const force = has('force');
const asJson = has('json');
const [command, ...urls] = args;
if (!['record', 'check'].includes(command) || urls.length === 0) fail(USAGE);
const stray = urls.find((u) => u.startsWith('--'));
if (stray) fail(`unknown flag ${stray}\n${USAGE}`);
const bad = urls.find((u) => !/^https?:\/\//.test(u));
if (bad) fail(`not an http(s) URL: ${bad}`);
if (widthFlag !== undefined && !(Number(widthFlag) >= 200)) fail(`--width needs a number of 200 or more, got "${widthFlag}"`);
if (command === 'record' && dropSpecs.length) fail('--drop belongs to check\n' + USAGE);
if (command === 'check' && force) fail('--force belongs to record\n' + USAGE);

let drops;
try { drops = dropSpecs.map(parseDrop); } catch (e) { fail(e.message); }

const outDir = resolve(outFlag);
const beforeFile = join(outDir, 'before.json');
const pageKey = (u) => normPath(u, u);

let before = null;
if (command === 'record') {
  if (existsSync(beforeFile) && !force) fail(`${beforeFile} already exists. Pass --force to replace the record; --force replaces every recorded page, so record all pages in one command.`);
} else {
  if (!existsSync(beforeFile)) fail(`No record at ${beforeFile}. Run "node keep.mjs record <url>" on the old page first.`);
  try { before = JSON.parse(readFileSync(beforeFile, 'utf8')); } catch (e) { fail(`${beforeFile} is not valid JSON: ${e.message}`); }
  const missing = urls.filter((u) => !before.pages?.[pageKey(u)]);
  if (missing.length) fail(`No record for ${missing.map(pageKey).join(', ')} in ${beforeFile}. Recorded pages: ${Object.keys(before.pages ?? {}).join(', ') || 'none'}`);
}
const width = Number(widthFlag ?? before?.width ?? 1440);

// page.eval passes `arg` as the function's one argument; snapshot needs the page's own address as its base.
async function run() {
  const browser = await Browser.launch({ width, height: 900 });
  const pages = {};
  try {
    for (const url of urls) {
      let got;
      {
        const page = await browser.newPage({ width, height: 900 });
        try {
          await page.send('Network.enable');
          // Only the main frame's document sets the status; an iframe's response must not.
          const mainFrame = (await page.send('Page.getFrameTree')).frameTree.frame.id;
          let status;
          browser.on(page.sessionId, 'Network.responseReceived', (p) => {
            if (p.type === 'Document' && p.frameId === mainFrame) status = p.response.status;
          });
          await page.goto(url).catch((e) => { throw new Error(`Cannot reach ${url}: ${e.message}`); });
          if (status === undefined) throw new Error(`Cannot reach ${url}: no response`);
          const href = await page.eval('location.href');
          const snap = await page.eval(snapshot, href);
          got = { status, href, snap };
        } finally {
          await page.close();
        }
      }
      pages[pageKey(url)] = {
        finalPath: pageKey(got.href),
        status: got.status,
        skippedButtons: got.snap.skippedButtons,
        items: got.snap.items,
      };
    }
  } finally {
    // Let Chrome shut itself down and wait for it, so its helper processes go too before the profile is removed.
    const exited = new Promise((r) => browser.proc.once('exit', r));
    await browser.send('Browser.close', {}, undefined, 3000).catch(() => {});
    await Promise.race([exited, sleep(5000)]);
    await browser.close();
  }
  return pages;
}

const skippedLine = (pages, was) => {
  const parts = Object.entries(pages).filter(([k, p]) => p.skippedButtons > 0 || was?.[k]?.skippedButtons > 0)
    .map(([k, p]) => `${was ? `${was[k]?.skippedButtons ?? 0}→` : ''}${p.skippedButtons} on ${k}`);
  return parts.length ? `Skipped buttons with no accessible name (not recorded): ${parts.join(', ')}` : '';
};

mkdirSync(outDir, { recursive: true });
let pages;
try { pages = await run(); } catch (e) { fail(e.message); }
const now = new Date().toISOString();

if (command === 'record') {
  const record = { version: 1, width, at: now, pages };
  writeFileSync(beforeFile, JSON.stringify(record, null, 2) + '\n');
  if (asJson) {
    console.log(JSON.stringify(record, null, 2));
  } else {
    for (const [k, p] of Object.entries(pages)) {
      console.log(`Recorded ${p.items.length} items on ${k} (status ${p.status})`);
      if (p.items.length === 0) console.log(`WARN nothing recorded on ${k}: a check against it would compare nothing`);
    }
    const skipped = skippedLine(pages);
    if (skipped) console.log(skipped);
    console.log(`Wrote ${beforeFile}`);
    console.log(NOT_CHECKED);
  }
  process.exit(0);
}

const after = { version: 1, width, at: now, pages };
const result = compare(before, after, drops);
// Icon-only buttons are not recorded, so a drop in their number is the only sign one was lost.
for (const [k, p] of Object.entries(pages)) {
  const was = before.pages?.[k]?.skippedButtons ?? 0;
  if (p.skippedButtons < was) {
    result.findings.push({ level: 'WARN', kind: 'page', key: k, page: k, message: `buttons with no accessible name went from ${was} to ${p.skippedButtons} on ${k}: one may have been lost, and they are not recorded` });
  }
}
const skippedNow = Object.fromEntries(Object.entries(pages).map(([k, p]) => [k, p.skippedButtons]));
writeFileSync(join(outDir, 'after.json'), JSON.stringify(after, null, 2) + '\n');
const fails = result.findings.filter((f) => f.level === 'FAIL');
const warns = result.findings.filter((f) => f.level === 'WARN');
const report = { at: now, urls, ...result, skippedButtons: skippedNow, notChecked: NOT_CHECKED };
writeFileSync(join(outDir, 'report.json'), JSON.stringify(report, null, 2) + '\n');

if (asJson) {
  console.log(JSON.stringify(report, null, 2));
} else {
  // Single-quoted so a shell leaves "$", backticks and double quotes alone.
  const hint = (f) => `--drop '${f.drop.replace(/'/g, `'\\''`)}'`;
  for (const f of fails) console.log(`FAIL ${f.page}: ${f.message}\n     to accept this loss: ${hint(f)}`);
  for (const u of result.unmatchedDrops) console.log(`FAIL --drop matched nothing: "${u}" (check the spelling against the record)`);
  for (const f of warns) console.log(`WARN ${f.page}: ${f.message}${f.drop ? `\n     to accept this: ${hint(f)}` : ''}`);
  for (const d of result.dropped) console.log(`dropped ${d.kind}:${d.key} on ${d.page} -- ${d.reason}`);
  const kept = Object.entries(LABELS).filter(([k]) => result.counts[k]).map(([k, label]) => `${result.counts[k].kept}/${result.counts[k].total} ${label}`);
  console.log(kept.length ? `Kept ${kept.join(' · ')}` : 'Kept nothing to count');
  const skipped = skippedLine(pages, before.pages);
  if (skipped) console.log(skipped);
  console.log(NOT_CHECKED);
}
process.exit(fails.length || result.unmatchedDrops.length ? 1 : 0);
