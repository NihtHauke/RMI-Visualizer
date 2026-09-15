"""
render_drawings.py — renders the RMI 2D detail drawings, 3D concept sheets and spec plates the visualizer
references into drawings/ as PNGs, one per drawing number, plus a manifest the Drawing panel reads.

    python scripts/render_drawings.py            # render everything index.html references (+ EXTRAS below)
    python scripts/render_drawings.py --check    # resolve only: show which number maps to which file, render nothing
    python scripts/render_drawings.py --dpi 200  # sharper (default 150)
    python scripts/render_drawings.py --only D-1-TYP CID-1-21-FT3D

Source: the local RMI library (LIB below; the path is also in CLAUDE.md). The library is NOT in the repo and
the PDFs never get copied in. drawings/ is git-ignored and must stay that way until the repo is private: the
PNGs are RMI's drawings. The installer bundles drawings/ (electron-builder.yml `files`), so run this before
`npm run dist`.

How a number finds its file:
  1. OVERRIDES — the odd ones (two sheets both numbered W-7-TYP, the spec plates, a title block that reads F20-TYP).
  2. A 3D concept sheet is named after its number (CID-1-21-FT3D.pdf), so the file stem matches.
  3. A 2D detail drawing's file name is loose ("CS 7 TYP Sleeper Support" carries title block CS-8-TYP), so the
     title block wins: the number is a line of the sheet's text on its own, followed by the title line, preceded
     by the ISSUE / REVISION date. Anything unresolved is reported at the end.

Outputs: drawings/<number>.png, drawings/index.js (window.RMI_DRAWINGS = {...}, loaded by index.html with a
plain <script> so it works from file:// in Electron too) and drawings/index.json (same data, for other tools).
Manifest entry: { file, kind: '2d'|'3d'|'plate', title, rev, w, h, source } where source is the file name inside
the library, for traceability. Requires PyMuPDF (pip install pymupdf).
"""
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "drawings"
LIB = Path(r"C:\Users\hcarr\OneDrive\Documents\Claude\Projects\2024 Master RMI Library")
FOLDERS = {
    "2d": LIB / "2024 Detail Drawings",
    "3d": LIB / "2024 3D Details",
    "plate": LIB / "2024 Specifications" / "2024 Master Specification Plates",
}

# number as index.html spells it -> path relative to LIB
OVERRIDES = {
    "W-7-TYP":        "2024 Detail Drawings/Typical Wall Configurations/W-7-TYP Wall Concrete 110524.pdf",   # silo walls
    "W-7-TYP-GUTTER": "2024 Detail Drawings/Drains - Typical  All susbstrates/W-7-TYPpdf.pdf",           # gutter seams: same number, different sheet
    "F-20-TYP":       "2024 Detail Drawings/Field Repairs - Typical All systems/F-20-TYP-field Metal Lap Stand Seam 2024.pdf",   # title block reads F20-TYP
    "Plate D":        "2024 Specifications/2024 Master Specification Plates/Plate-D- Metal Duct -Vents 01012020.pdf",
    "Plate MP":       "2024 Specifications/2024 Master Specification Plates/Plate-MP-Metal-01012020.pdf",
}
# referenced in detail text or the catalog but not in a `drawing:` / `concept:` field — cheap to carry along
EXTRAS = ["F-20-TYP", "P-10-MP", "P-7-C", "D-2-TYP", "P-1-S-TYP", "P-2-S-TYP", "P-3-S-TYP", "CS-1-TYP"]

NUM_LINE = re.compile(r"^\s*([A-Z]{1,3}-\d{1,2}(?:-[A-Z]{1,3})?(?:-[A-Z]{1,4})?)\s*$")
DATE = re.compile(r"^\s*(\d{1,2}/\d{1,2}/\d{2,4})\s*$")


def referenced():
    """Every drawing / concept / sheet string in index.html's DETAILS block (including byRoof overrides)."""
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    start = html.index("const DETAILS")
    end = html.index("function DET(", start)
    block = html[start:end]
    nums = set(re.findall(r"\b(?:drawing|concept|sheet):'([^']+)'", block))
    nums.discard("—")
    return sorted(nums | set(EXTRAS))


def sheet_info(pdf):
    """Title-block number, title and revision date read from the sheet's own text."""
    import pymupdf
    doc = pymupdf.open(pdf)
    lines = [l.strip() for l in doc[0].get_text().splitlines() if l.strip()]
    num = title = rev = None
    for i, l in enumerate(lines):
        m = NUM_LINE.match(l)
        if m and num is None:
            num = m.group(1)
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if nxt and not nxt.upper().startswith(("COPYRIGHT", "ALL RIGHTS", "WWW.", "DETAIL NUMBER", "ISSUE")):
                title = re.sub(r"\s+", " ", nxt).replace("\ufffd", "–").replace("\x96", "–")
        d = DATE.match(l)
        if d and rev is None:
            rev = d.group(1)
    if rev is None:  # spec plates: "REVISED 1/01/2020" inside a header line
        m = re.search(r"REVISED\s+(\d{1,2}/\d{1,2}/\d{2,4})", "\n".join(lines))
        rev = m.group(1) if m else None
    if title is None and pdf.name.lower().startswith("plate"):
        m = re.search(r"\n([A-Z]{1,4} - [^\n]+?)\s*\n", "\n".join(lines))
        title = m.group(1).strip() if m else None
    return doc, num, title, rev


def index_library():
    """kind -> {stem: path} and {title-block number: path} for the 2D drawings."""
    by_stem, by_title = {}, {}
    for kind, folder in FOLDERS.items():
        for p in sorted(folder.rglob("*.pdf")):
            by_stem[(kind, p.stem.strip().upper())] = p
    for p in sorted(FOLDERS["2d"].rglob("*.pdf")):
        try:
            _, num, _, _ = sheet_info(p)
        except Exception as e:  # noqa: BLE001
            print(f"  ! could not read {p.name}: {e}")
            continue
        if num and num not in by_title:
            by_title[num] = p
    return by_stem, by_title


def resolve(num, by_stem, by_title):
    """-> (kind, path) or (None, None)."""
    if num in OVERRIDES:
        p = LIB / OVERRIDES[num]
        kind = "plate" if num.startswith("Plate") else "2d"
        return (kind, p) if p.exists() else (None, None)
    key = num.upper()
    if ("3d", key) in by_stem:
        return "3d", by_stem[("3d", key)]
    if num in by_title:
        return "2d", by_title[num]
    if ("2d", key) in by_stem:
        return "2d", by_stem[("2d", key)]
    return None, None


def safe_name(num):
    return re.sub(r"[^A-Za-z0-9.-]+", "-", num).strip("-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--check", action="store_true", help="resolve numbers to files and stop")
    ap.add_argument("--only", nargs="*", help="render just these numbers")
    args = ap.parse_args()

    if not LIB.exists():
        sys.exit(f"RMI library not found at {LIB}")
    try:
        import pymupdf  # noqa: F401
    except ImportError:
        sys.exit("pip install pymupdf")

    nums = args.only or referenced()
    print(f"{len(nums)} drawing numbers referenced; indexing the library …")
    by_stem, by_title = index_library()

    manifest, missing = {}, []
    if not args.check:
        OUT.mkdir(exist_ok=True)
    for num in nums:
        kind, pdf = resolve(num, by_stem, by_title)
        if not pdf:
            missing.append(num)
            print(f"  MISSING  {num}")
            continue
        doc, tb_num, title, rev = sheet_info(pdf)
        if kind == "3d":
            title, tb_num = title or pdf.stem, pdf.stem
        flag = "" if (tb_num or "").replace(" ", "") in (num.replace(" ", ""), "") or num in OVERRIDES else f"   (title block reads {tb_num})"
        print(f"  {kind:5s}  {num:16s} <- {pdf.name}{flag}")
        entry = {"file": safe_name(num) + ".png", "kind": kind, "title": title, "rev": rev, "source": pdf.name}
        if not args.check:
            pix = doc[0].get_pixmap(dpi=args.dpi, alpha=False)
            pix.save(OUT / entry["file"])
            entry["w"], entry["h"] = pix.width, pix.height
        manifest[num] = entry
        doc.close()

    if not args.check:
        (OUT / "index.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
        (OUT / "index.js").write_text(
            "// generated by scripts/render_drawings.py — RMI drawings rendered from the local library. Never commit drawings/.\n"
            "window.RMI_DRAWINGS = " + json.dumps(manifest, ensure_ascii=False) + ";\n", encoding="utf-8")
        total = sum((OUT / e["file"]).stat().st_size for e in manifest.values())
        print(f"\nwrote {len(manifest)} PNGs ({total / 1e6:.1f} MB) + index.js / index.json to {OUT}")
    if missing:
        print("\nNOT FOUND in the library (the panel will say so for these):", ", ".join(missing))
    else:
        print("\nevery referenced number resolved")


if __name__ == "__main__":
    main()
