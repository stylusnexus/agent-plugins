// Helpers for keep.mjs: normalise what a page does into stable keys, and parse --drop specs.

const KINDS = ['href', 'form', 'field', 'button', 'handler', 'hook', 'heading', 'anchor', 'page'];

export const normText = (s) => String(s ?? '').normalize('NFC').replace(/\s+/g, ' ').trim();

// Same-origin results are pathname + search + hash with one trailing slash removed (root stays "/").
// Cross-origin and non-http schemes come back whole; so do values that are not valid URLs.
// A bare "#" keeps its "#" (so it is not the page's own path) and an empty value is its own key "(empty)".
export function normPath(urlOrPath, base) {
  if (urlOrPath === '') return '(empty)';
  if (urlOrPath === '(empty)') return urlOrPath;
  try {
    const u = new URL(urlOrPath, base);
    if (u.protocol !== 'http:' && u.protocol !== 'https:') return urlOrPath;
    if (u.hostname !== new URL(base).hostname) return urlOrPath;
    const path = u.pathname.length > 1 && u.pathname.endsWith('/') ? u.pathname.slice(0, -1) : u.pathname;
    return path + u.search + u.hash + (u.hash === '' && urlOrPath.endsWith('#') ? '#' : '');
  } catch {
    return urlOrPath;
  }
}

// Generated ids change on every render, so they are never recorded.
export const isUnstableId = (id) =>
  /^(:r|«r|_r_)[0-9a-z]+(:|»|_)/.test(id) || /^(radix-|headlessui-|react-aria)/.test(id) || /[0-9a-f]{8,}/i.test(id);

const usage = (why) => new Error(`usage: ${why}. Expected --drop "<kind>:<value> -- <reason>" with kind one of ${KINDS.join(', ')} and a reason of at least 10 characters`);

export function parseDrop(spec) {
  const at = spec.indexOf(' -- ');
  if (at < 0) throw usage(`missing " -- " in "${spec}"`);
  const key = spec.slice(0, at).trim();
  const reason = spec.slice(at + 4).trim();
  const colon = key.indexOf(':');
  const kind = colon < 0 ? '' : key.slice(0, colon);
  if (!KINDS.includes(kind)) throw usage(`unknown kind "${kind}" in "${spec}"`);
  if (reason.length < 10) throw usage(`reason is under 10 characters in "${spec}"`);
  let value = key.slice(colon + 1);
  const prefix = value.endsWith('*');
  if (prefix) value = value.slice(0, -1);
  return { kind, value, prefix, reason };
}

export function matchesDrop(drop, item) {
  if (drop.kind !== item.kind) return false;
  const want = `${drop.kind}:${drop.value}`;
  return drop.prefix ? item.key.startsWith(want) : item.key === want;
}

// Drop values are normalised the same way item keys are, so a pasted value still matches.
const BASE = 'http://localhost/';
function normDrop(drop) {
  let value = drop.value.trim();
  if (drop.kind === 'href' || drop.kind === 'form') {
    const keepSlash = drop.prefix && value.endsWith('/');
    // A form key is "<METHOD> <action>": only the action is a path.
    const space = drop.kind === 'form' ? value.indexOf(' ') : -1;
    if (drop.kind === 'form' && space < 0) return { ...drop, value };
    const method = space < 0 ? '' : `${value.slice(0, space).toUpperCase()} `;
    value = method + normPath(value.slice(space + 1), BASE);
    if (keepSlash && !value.endsWith('/')) value += '/';
  } else if (['field', 'button', 'handler', 'hook', 'heading'].includes(drop.kind)) {
    value = normText(value);
  }
  return { ...drop, value };
}

const withKind = (kind, key) => ({ kind, key: `${kind}:${key}` });
const dropSpec = (d) => `${d.kind}:${d.value}${d.prefix ? '*' : ''} -- ${d.reason}`;

export function compare(before, after, drops) {
  const normDrops = drops.map(normDrop);
  const used = new Set();
  const findings = [];
  const dropped = [];
  const counts = {};

  const dropFor = (kind, key) => {
    const probe = withKind(kind, key);
    let hit = null;
    normDrops.forEach((d, i) => {
      if (matchesDrop(d, probe)) {
        used.add(i);
        hit ??= d;
      }
    });
    return hit;
  };

  const emit = (level, kind, key, page, message) => {
    const d = dropFor(kind, key);
    if (d) {
      dropped.push({ kind, key, page, reason: d.reason });
      return true;
    }
    findings.push({ level, kind, key, page, message, drop: `${kind}:${key} -- <reason>` });
    return false;
  };

  const beforePages = Object.entries(before.pages ?? {});
  if (beforePages.length === 0) {
    findings.push({ level: 'WARN', kind: 'page', key: '*', page: '*', message: 'nothing recorded: the before record has no pages', drop: 'page:* -- <reason>' });
  }

  for (const [path, was] of beforePages) {
    const now = after.pages?.[path];
    const items = was.items ?? [];
    const bump = (item, kept) => {
      const c = (counts[item.kind] ??= { kept: 0, total: 0 });
      c.total += 1;
      if (kept) c.kept += 1;
    };
    // A drop that names a recorded item counts as used even when the item survived.
    for (const item of items) dropFor(item.kind, item.key);

    if (items.length === 0) {
      emit('WARN', 'page', path, path, `nothing recorded on ${path}: nothing to compare, so a pass here would mean nothing`);
    }
    if (!now) {
      emit('FAIL', 'page', path, path, `${path} was recorded before but is missing from the after run`);
      for (const item of items) bump(item, false);
      continue;
    }
    if (now.status >= 400) {
      emit('FAIL', 'page', path, path, `${path} returned status ${now.status}`);
      for (const item of items) bump(item, false);
      continue;
    }
    if (now.finalPath !== was.finalPath) {
      emit('WARN', 'page', path, path, `${path} ended on ${now.finalPath}, it ended on ${was.finalPath} before`);
    }

    const afterIndex = new Map((now.items ?? []).map((i) => [`${i.kind}:${i.key}`, i]));
    const beforeKeys = new Set(items.map((i) => `${i.kind}:${i.key}`));
    // Links present only after, by label, so a rewritten href is reported once as "changed".
    const newLinks = (now.items ?? []).filter((i) => i.kind === 'href' && !beforeKeys.has(`href:${i.key}`) && i.label);

    for (const item of items) {
      const there = afterIndex.get(`${item.kind}:${item.key}`);
      if (there) {
        bump(item, true);
        if (item.visible && !there.visible) {
          emit('WARN', item.kind, item.key, path, `${item.kind} ${item.key} was visible and is now hidden`);
        }
        continue;
      }
      if (item.kind === 'href' && item.label) {
        const at = newLinks.findIndex((n) => n.label === item.label);
        if (at >= 0) {
          const [moved] = newLinks.splice(at, 1);
          emit('FAIL', 'href', item.key, path, `changed: link "${item.label}" went from ${item.key} to ${moved.key}`);
          bump(item, false);
          continue;
        }
      }
      const level = item.kind === 'heading' ? 'WARN' : 'FAIL';
      emit(level, item.kind, item.key, path, `${item.kind} ${item.key} is missing after`);
      bump(item, false);
    }
  }

  const unmatchedDrops = normDrops.flatMap((d, i) => (used.has(i) ? [] : [dropSpec(d)]));
  return { findings, dropped, counts, unmatchedDrops };
}

// Runs inside the page (page.eval serialises it with toString()), so it uses nothing from this module:
// the normalisation below is a copy of normText, normPath and isUnstableId.
// Keys come out already normalised, because compare() matches on them as given.
export function snapshot(base) {
  const text = (s) => String(s ?? '').normalize('NFC').replace(/\s+/g, ' ').trim();
  const path = (value) => {
    if (value === '') return '(empty)';
    if (value === '(empty)') return value;
    try {
      const u = new URL(value, base);
      if (u.protocol !== 'http:' && u.protocol !== 'https:') return value;
      if (u.hostname !== new URL(base).hostname) return value;
      const p = u.pathname.length > 1 && u.pathname.endsWith('/') ? u.pathname.slice(0, -1) : u.pathname;
      return p + u.search + u.hash + (u.hash === '' && value.endsWith('#') ? '#' : '');
    } catch {
      return value;
    }
  };
  const unstable = (id) =>
    /^(:r|«r|_r_)[0-9a-z]+(:|»|_)/.test(id) || /^(radix-|headlessui-|react-aria)/.test(id) || /[0-9a-f]{8,}/i.test(id);
  const shown = (el) => el.getClientRects().length > 0;

  const items = [];
  const seen = new Map();
  const add = (kind, key, label, el) => {
    if (!key) return;
    // The same key can appear twice (a hidden drawer copy and a visible one): visible if any copy is.
    if (seen.has(kind + ':' + key)) {
      if (!seen.get(kind + ':' + key).visible && shown(el)) seen.get(kind + ':' + key).visible = true;
      return;
    }
    const item = { kind, key, visible: shown(el) };
    seen.set(kind + ':' + key, item);
    if (label) item.label = label;
    items.push(item);
  };
  const all = (selector) => Array.from(document.querySelectorAll(selector));
  const basePage = path(base).split('#')[0];

  for (const a of all('a[href]')) {
    const raw = a.getAttribute('href');
    const key = path(raw);
    add('href', key, text(a.textContent) || text(a.getAttribute('aria-label')), a);
    // A link to a spot on this same page: remember the spot it points at.
    const hash = key.indexOf('#');
    if (hash >= 0 && key.slice(0, hash) === basePage) {
      let id = key.slice(hash + 1);
      try { id = decodeURIComponent(id); } catch {}
      const target = id ? document.getElementById(id) : null;
      if (target) add('anchor', id, '', target);
    }
  }

  for (const f of all('form')) {
    const action = f.getAttribute('action');
    let where;
    try { where = path(new URL(action || '', base).href); } catch { where = action; }
    add('form', String(f.getAttribute('method') || 'get').toUpperCase() + ' ' + where, '', f);
  }

  for (const el of all('input, select, textarea')) {
    const type = String(el.getAttribute('type') || '').toLowerCase();
    if (['submit', 'button', 'reset', 'image'].includes(type)) continue; // these inputs are buttons
    const name = el.getAttribute('name');
    const id = el.getAttribute('id');
    const key = text(name) || (id && !unstable(id) ? text(id) : '');
    add('field', key, el.tagName === 'INPUT' ? type || 'text' : el.tagName.toLowerCase(), el);
  }

  let skippedButtons = 0;
  for (const b of all('button, [role=button], input[type=submit], input[type=button], input[type=reset], input[type=image]')) {
    const name = text(b.getAttribute('aria-label')) || text(b.tagName === 'INPUT' ? b.getAttribute('value') : b.textContent) || text(b.getAttribute('value')) || text(b.getAttribute('alt'));
    if (!name) { skippedButtons += 1; continue; }
    add('button', name, '', b);
  }

  for (const el of all('*')) {
    for (const attr of Array.from(el.attributes)) {
      if (!/^on/i.test(attr.name)) continue;
      const who = text(el.getAttribute('id')) || text(el.getAttribute('name')) || text(text(el.textContent).slice(0, 40));
      add('handler', attr.name.toLowerCase() + ' ' + el.tagName.toLowerCase() + '#' + who, '', el);
    }
  }

  for (const attr of ['data-testid', 'data-test', 'data-cy', 'data-qa']) {
    for (const el of all('[' + attr + ']')) add('hook', attr + '=' + text(el.getAttribute(attr)), '', el);
  }

  for (const h of all('h1, h2, h3')) add('heading', text(h.textContent), '', h);

  return { items, skippedButtons };
}
