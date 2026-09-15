"""
snapshot.py — visual check for the RMI Roof Visualizer.

Serves the repo root on a local port, opens index.html in headless Chromium, selects a
building (and optionally a detail), steps through the six stages, and saves one PNG per
stage plus a contact sheet. Run it after every model or code change and LOOK at the output.

Usage (from the repo root):
    python scripts/snapshot.py --building bigbox --detail drain
    python scripts/snapshot.py --building bigbox                 # whole-roof view only
    python scripts/snapshot.py --building bigbox --detail rtu --section   # section view on
    python scripts/snapshot.py --building bigbox --detail coping --cam 7,1.75,1.1 --stages 6   # try a camera, one stage
    python scripts/snapshot.py --building warehouse --roof sseam                  # a roof other than the building's first
    python scripts/snapshot.py --building bigbox --detail drain --drawing            # Drawing panel open, 2D tab
    python scripts/snapshot.py --building bigbox --detail drain --drawing steps      # ... "How it's applied" tab (or 3d)
    python scripts/snapshot.py --eagleview ../RMI-prospects/x/report.XML                   # EagleView prospect roof (the file stays where it is)
    python scripts/snapshot.py --eagleview ../RMI-prospects/x/report.XML --detail pipe --pdf  # ... a hotspot, and the PDF via page.pdf()
    python scripts/snapshot.py --building bigbox --photos a.jpg,b.png --width 1366 --height 768
        # prospect photos: loads the files into the photo strip, pins the first photo to the building's details
        # (which docks the slider on the right), shoots the split layout at laptop size, then clicks the first pin
        # and shoots the detail it zooms to (<tag>-pin.png). Without --photos the strip is hidden and the sheet is
        # the plain default-camera layout. Each run is a fresh browser profile, so nothing restores from storage.

A --detail the building does not carry is skipped with a message listing the ones it does have.
--drawing needs the rendered sheets in drawings/ (scripts/render_drawings.py); without them the panel shows its
"not bundled" message, which is also worth a look. The run prints the panel state (sheet number, loaded/missing).

One-time setup:
    pip install playwright pillow
    playwright install chromium

Outputs go to snapshots/<building>-<detail>-<stage>.png and snapshots/<building>-<detail>-sheet.png.
The snapshots/ folder is git-ignored; attach the sheet to a message rather than committing it.
"""
import argparse, http.server, os, socketserver, threading, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "snapshots"
STAGES = ["existing", "prep", "primer", "flex", "thane", "done"]


def serve(port):
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *a, **k: None
    os.chdir(ROOT)
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def unlocked(path):
    """Windows image viewers (and the app's file panel) hold PNGs open, which makes the next write fail with
    EINVAL. Remove the old file if we can; otherwise hand back a fresh name so the run still completes."""
    try:
        if path.exists():
            path.unlink()
        return path
    except OSError:
        alt = path.with_name(f"{path.stem}-{int(time.time()) % 10000}{path.suffix}")
        print("locked, writing", alt.name, "instead")
        return alt


def save_png(page, path):
    path = unlocked(path)
    for attempt in range(3):
        try:
            page.screenshot(path=str(path), timeout=60000); return path
        except OSError:
            time.sleep(0.5); path = unlocked(path)
    page.screenshot(path=str(path), timeout=60000); return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--building", default="bigbox")
    ap.add_argument("--detail", default=None, help="detail id, e.g. drain, rtu, coping, pipe")
    ap.add_argument("--roof", default=None, help="roof id to switch to after the building loads, e.g. sseam, spf (default: the building's first)")
    ap.add_argument("--section", action="store_true", help="turn on Section view in detail mode")
    ap.add_argument("--eagleview", default=None, help="EagleView report XML to import (client data: read from where it is, never copied); selects the prospect roof")
    ap.add_argument("--pdf", action="store_true", help="also build the PDF document and save it with page.pdf() (headless Chromium)")
    ap.add_argument("--topcoat", default="thane", choices=["thane", "white"])
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--width", type=int, default=1400)
    ap.add_argument("--height", type=int, default=860)
    ap.add_argument("--cam", default=None, help="override the detail camera: dist,theta,phi[,drop] (tune DETAILS[...] without editing index.html)")
    ap.add_argument("--stages", default=None, help="comma list of stage numbers to shoot, e.g. 4,6 (default: all six)")
    ap.add_argument("--photos", default=None, help="comma list of image files to load into the Prospect photos strip (JPG/PNG/HEIC); pins the first one, which opens the slider")
    ap.add_argument("--drawing", nargs="?", const="2d", default=None, choices=["2d", "steps", "3d"], help="open the Drawing panel in detail view on this tab (default 2d)")
    args = ap.parse_args()
    want = {int(x) - 1 for x in args.stages.split(",")} if args.stages else set(range(len(STAGES)))

    from playwright.sync_api import sync_playwright

    OUT.mkdir(exist_ok=True)
    httpd = serve(args.port)
    if args.eagleview:
        args.building = "prospect"
    tag = f"{args.building}{'-' + args.roof if args.roof else ''}-{args.detail or 'roof'}{'-section' if args.section else ''}{'-photos' if args.photos else ''}{'-drawing-' + args.drawing if args.drawing else ''}"
    photos = [str(Path(f.strip()).resolve()) for f in args.photos.split(",")] if args.photos else []
    for f in photos:
        if not Path(f).exists():
            raise SystemExit(f"no such photo: {f}")
    files = []
    errors = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader",
                                              "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
            page = browser.new_page(viewport={"width": args.width, "height": args.height})
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("console", lambda m: errors.append(m.text) if m.type in ("error", "warning") else None)
            page.goto(f"http://127.0.0.1:{args.port}/index.html")
            page.wait_for_timeout(3000)
            if args.eagleview:
                xml_path = Path(args.eagleview).resolve()
                xml = xml_path.read_text(encoding="utf-8")
                date = time.strftime("%B %d, %Y", time.localtime(xml_path.stat().st_mtime))
                ok = page.evaluate("([t,n,d])=>window.__rmi.eagleview.import(t,n,d)", [xml, xml_path.name, date])
                page.wait_for_timeout(7000)  # every penetration mounts a model
                st = page.evaluate("window.__rmi.eagleview.state()")
                print(f"eagleview import: ok={ok} report={st['report']} facets={len(st['facets'])} penetrations={st['penetrations']} kinds={st['kinds']} details={st['details']} hots={st['hots']}")
                for f in st["facets"]:
                    print(f"  facet {f['id']} {f['des']}: elevation {f['elevation']} ft, {f['area']} sq ft, edges {f['edges']}")
                print("  unused:", *st["unused"], sep="\n    ")
                page.evaluate("window.__rmi.eagleview.open(false); window.__rmi.finishCam();")
            else:
                page.evaluate(f"window.__rmi.selectBuilding('{args.building}'); window.__rmi.finishCam();")
                page.wait_for_timeout(3500)  # models load async
            if args.roof:
                page.evaluate(f"const r=document.getElementById('roof'); r.value='{args.roof}'; r.dispatchEvent(new Event('change')); window.__rmi.finishCam();")
                page.wait_for_timeout(3500)
            if photos:
                page.evaluate("window.__rmiQuiet = true")
                page.set_input_files("#photoInput", photos)
                page.wait_for_timeout(2500)  # decode (a HEIC loads the vendored heic2any converter first)
                have = page.evaluate("window.__rmi.details()")
                want_pins = ([args.detail] if args.detail else []) + [d for d in have if d != args.detail]
                spots = [(0.64, 0.5), (0.28, 0.74), (0.11, 0.58)]
                for (x, y), d in zip(spots, want_pins[:3]):
                    page.evaluate("([x,y,d])=>window.__rmi.photos.pin(0,x,y,d)", [x, y, d])
                page.evaluate("window.__rmi.finishCam()")  # docking the slider refits the whole-roof camera; skip the fly (slow under swiftshader)
                page.wait_for_timeout(300)
                st = page.evaluate("window.__rmi.photos.state()")
                for ph in st["photos"]:
                    print(f"photo {ph['name']}: {ph['status']} {ph['w']}x{ph['h']} pins={[p['drawing'] for p in ph['pins']]}")
            if args.topcoat == "white":
                page.evaluate("document.querySelector('#topcoat button[data-v=white]').click()")
            if args.detail:
                if args.cam:
                    v = [float(x) for x in args.cam.split(",")]
                    keys = ["dist", "theta", "phi", "drop"][:len(v)]
                    page.evaluate("([id,o])=>Object.assign(window.__rmi.DETAILS[id],o)", [args.detail, dict(zip(keys, v))])
                # goDetail returns false when this building has no such hotspot (e.g. office has no coping,
                # it uses edge metal). Nothing to photograph, so say which details it does have and stop.
                if page.evaluate(f"window.__rmi.goDetail('{args.detail}') === false"):
                    have = ", ".join(page.evaluate("window.__rmi.details()")) or "none"
                    print(f"skipped: {args.building} has no '{args.detail}' hotspot. It has: {have}")
                    browser.close()
                    return
                page.evaluate("window.__rmi.finishCam();")
                page.wait_for_timeout(800)
                if args.section:
                    page.click("#secBtn")
                    page.wait_for_timeout(500)
                if args.drawing:
                    page.click("#drwBtn")
                    page.evaluate(f"window.__rmi.drawing.tab('{args.drawing}')")
                    page.wait_for_timeout(1200)  # manifest script + sheet PNG
                    st = page.evaluate("window.__rmi.drawing.state()")
                    print(f"drawing panel: tab={st['tab']} sheet={st['number']} status={st['status']} zoom={st['zoom']} steps={st['steps']} manifest={st['manifest']}")
            for i, name in enumerate(STAGES):
                if i not in want:
                    continue
                page.evaluate(f"window.__rmi.setStage({i}, true); window.__rmi.S.prog = 1;")
                page.wait_for_timeout(700)
                files.append(save_png(page, OUT / f"{tag}-{i+1}-{name}.png"))
            if args.pdf:
                st = page.evaluate("window.__rmi.pdf.prepare()")
                print(f"pdf prepared: {st['pages']} pages, {st['images']} images")
                page.emulate_media(media="print")
                pdf_path = unlocked(OUT / f"{tag}.pdf")
                page.pdf(path=str(pdf_path), format="Letter", print_background=True, prefer_css_page_size=True)
                page.emulate_media(media="screen")
                page.evaluate("window.__rmi.pdf.done(true)")
                print("wrote", pdf_path)
            if photos:
                # click the first pin: the 3D view should fly to that detail with the slider still docked
                page.evaluate("window.__rmi.photos.click(0,0); window.__rmi.finishCam();")
                page.wait_for_timeout(800)
                pin_png = save_png(page, OUT / f"{tag}-pin.png")
                print("pin click ->", page.evaluate("window.__rmi.S.view"), "wrote", pin_png)
                cfg = page.evaluate("window.__rmi.configuration()")
                print("configuration.prospect_photos:", cfg.get("prospect_photos"))
            browser.close()
    finally:
        httpd.shutdown()

    # contact sheet
    try:
        from PIL import Image, ImageDraw
        ims = [Image.open(f) for f in files]
        w, h = ims[0].size
        shot = sorted(want)
        cols = min(3, len(shot)); rows = (len(shot) + cols - 1) // cols
        sheet = Image.new("RGB", (w * cols, h * rows), "white")
        d = ImageDraw.Draw(sheet)
        for n, (i, im) in enumerate(zip(shot, ims)):
            x, y = (n % cols) * w, (n // cols) * h
            sheet.paste(im, (x, y))
            d.rectangle([x, y, x + 260, y + 34], fill="#12213A")
            d.text((x + 10, y + 8), f"{i+1}. {STAGES[i]}", fill="white")
        sheet_path = unlocked(OUT / f"{tag}-sheet.png")
        sheet.save(sheet_path)
        print("contact sheet:", sheet_path)
    except ImportError:
        print("pillow not installed; skipping contact sheet")

    for f in files:
        print("wrote", f)
    if errors:
        print("\nBROWSER CONSOLE (errors/warnings):")
        for e in errors[:20]:
            print("  ", e)
    else:
        print("\nno console errors")


if __name__ == "__main__":
    main()
