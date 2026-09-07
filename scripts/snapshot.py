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

A --detail the building does not carry is skipped with a message listing the ones it does have.

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
    ap.add_argument("--section", action="store_true", help="turn on Section view in detail mode")
    ap.add_argument("--topcoat", default="thane", choices=["thane", "white"])
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--width", type=int, default=1400)
    ap.add_argument("--height", type=int, default=860)
    ap.add_argument("--cam", default=None, help="override the detail camera: dist,theta,phi[,drop] (tune DETAILS[...] without editing index.html)")
    ap.add_argument("--stages", default=None, help="comma list of stage numbers to shoot, e.g. 4,6 (default: all six)")
    args = ap.parse_args()
    want = {int(x) - 1 for x in args.stages.split(",")} if args.stages else set(range(len(STAGES)))

    from playwright.sync_api import sync_playwright

    OUT.mkdir(exist_ok=True)
    httpd = serve(args.port)
    tag = f"{args.building}-{args.detail or 'roof'}{'-section' if args.section else ''}"
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
            page.evaluate(f"window.__rmi.selectBuilding('{args.building}'); window.__rmi.finishCam();")
            page.wait_for_timeout(3500)  # models load async
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
            for i, name in enumerate(STAGES):
                if i not in want:
                    continue
                page.evaluate(f"window.__rmi.setStage({i}, true); window.__rmi.S.prog = 1;")
                page.wait_for_timeout(700)
                files.append(save_png(page, OUT / f"{tag}-{i+1}-{name}.png"))
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
