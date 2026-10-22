#!/usr/bin/env python3
"""WCAG 2.2 contrast ratios for colour pairs, or for named custom properties in a CSS file.

    contrast.py '#767676' '#ffffff'                 # one pair: text colour, then background
    contrast.py '#767676' '#fff' '#4b5563' '#fff'   # several pairs
    contrast.py --css app.css --pair text:surface --pair muted:surface

Accepts #rgb, #rrggbb, #rrggbbaa and rgb()/rgba(). A colour with alpha is composited over the
background. Ratios are truncated, never rounded up, so 4.499 does not show as 4.5.
Exit status is 1 when any pair misses --need (default: 4.5, normal text at AA).
"""
import argparse
import json
import re
import sys
from pathlib import Path

LEVELS = {"normal-AA": 4.5, "large-AA": 3.0, "ui-AA": 3.0, "normal-AAA": 7.0, "large-AAA": 4.5}


def parse(text):
    """Return (r, g, b, a) with channels 0-255 and alpha 0-1."""
    s = text.strip().lower()
    m = re.fullmatch(r"#([0-9a-f]{3,4}|[0-9a-f]{6}|[0-9a-f]{8})", s)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return r, g, b, a
    m = re.fullmatch(r"rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)(?:\s*[,/]\s*([\d.]+%?))?\s*\)", s)
    if m:
        r, g, b = (min(255.0, float(m.group(i))) for i in (1, 2, 3))
        a = m.group(4)
        a = 1.0 if a is None else float(a[:-1]) / 100 if a.endswith("%") else float(a)
        return r, g, b, min(1.0, a)
    raise ValueError(f"cannot read colour: {text!r} (use #hex or rgb())")


def composite(fg, bg):
    r, g, b, a = fg
    return tuple(a * c + (1 - a) * bc for c, bc in zip((r, g, b), bg[:3]))


def luminance(rgb):
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg_text, bg_text):
    bg = parse(bg_text)
    if bg[3] < 1:
        raise ValueError("background must be opaque; composite it over its own background first")
    fg = composite(parse(fg_text), bg)
    hi, lo = sorted((luminance(fg), luminance(bg[:3])), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def truncate(value, places=2):
    scale = 10 ** places
    return int(value * scale) / scale


def check(fg, bg):
    r = ratio(fg, bg)
    return {"fg": fg, "bg": bg, "ratio": truncate(r), **{k: r >= v for k, v in LEVELS.items()}}


def css_properties(path):
    """Custom properties declared in a CSS file. Returns (plain colours, notes).

    Later declarations win whatever their selector or media query, so a property declared more
    than once is reported in notes, as is any value that is not a plain colour (for example var()).
    """
    props, seen, notes = {}, {}, {}
    for name, value in re.findall(r"--([\w-]+)\s*:\s*([^;}]+)", Path(path).read_text()):
        value = value.strip()
        seen[name] = seen.get(name, 0) + 1
        try:
            parse(value)
        except ValueError:
            props.pop(name, None)
            notes[name] = f"--{name} is {value!r}, not a plain colour" + (" (var() is not resolved)" if "var(" in value else "")
            continue
        props[name] = value
        notes.pop(name, None)
    for name, count in seen.items():
        if count > 1 and name in props:
            notes[name] = f"--{name} is declared {count} times; the last one is used, whatever its selector or media query"
    return props, notes


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("colours", nargs="*", help="foreground background [foreground background ...]")
    parser.add_argument("--css", type=Path, help="CSS file whose --custom-properties are looked up by --pair")
    parser.add_argument("--pair", action="append", default=[], metavar="FG:BG", help="property names, without the leading --")
    parser.add_argument("--need", choices=sorted(LEVELS), default="normal-AA", help="level that sets the exit status")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    pairs = []
    if len(args.colours) % 2:
        parser.error("colours come in foreground/background pairs")
    pairs += list(zip(args.colours[::2], args.colours[1::2]))
    if args.pair:
        if not args.css:
            parser.error("--pair needs --css")
        props, notes = css_properties(args.css)
        for spec in args.pair:
            fg, _, bg = spec.partition(":")
            for name in (fg, bg):
                if name not in props:
                    parser.error(notes.get(name) or f"--{name} is not declared in {args.css}")
                if name in notes:
                    print(f"warning: {notes[name]}", file=sys.stderr)
            pairs.append((props[fg], props[bg]))
    if not pairs:
        parser.error("give at least one colour pair")

    results = []
    for fg, bg in pairs:
        try:
            results.append(check(fg, bg))
        except ValueError as error:
            parser.error(str(error))

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"{'text':<12}{'background':<12}{'ratio':>7}  " + "  ".join(LEVELS))
        for r in results:
            marks = "  ".join(("pass" if r[k] else "FAIL").ljust(len(k)) for k in LEVELS)
            print(f"{r['fg']:<12}{r['bg']:<12}{r['ratio']:>6.2f}:1  {marks}")
        print("\nnormal text AA 4.5, large text AA 3 (24px, or 18.66px bold), UI parts and graphics 3, AAA 7 / 4.5.")
        print("Measured on the colours given. Text over images, gradients or translucent layers needs its own check.")
    return 0 if all(r[args.need] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
