// Helpers for keep.mjs: normalise what a page does into stable keys, and parse --drop specs.

const KINDS = ['href', 'form', 'field', 'button', 'handler', 'hook', 'heading', 'anchor', 'page'];

export const normText = (s) => String(s ?? '').normalize('NFC').replace(/\s+/g, ' ').trim();

// Same-origin results are pathname + search + hash with one trailing slash removed (root stays "/").
// Cross-origin and non-http schemes come back whole; so do values that are not valid URLs.
export function normPath(urlOrPath, base) {
  try {
    const u = new URL(urlOrPath, base);
    if (u.protocol !== 'http:' && u.protocol !== 'https:') return urlOrPath;
    if (u.hostname !== new URL(base).hostname) return urlOrPath;
    const path = u.pathname.length > 1 && u.pathname.endsWith('/') ? u.pathname.slice(0, -1) : u.pathname;
    return path + u.search + u.hash;
  } catch {
    return urlOrPath;
  }
}

// Generated ids change on every render, so they are never recorded.
export const isUnstableId = (id) =>
  /^:r[0-9a-z]+:$/.test(id) || /^(radix-|headlessui-|react-aria)/.test(id) || /[0-9a-f]{8,}/i.test(id);

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
