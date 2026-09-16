"""
check_prospect.py — round-trip check for saved prospects in the browser build (the desktop build has its own:
RMI_SELFTEST_PROSPECT in electron/main.js).

Serves the repo root, opens index.html in headless Chromium, imports an EagleView report, changes the roof, finish,
parapet height, one detail and Solar Post through the form controls, adds two photos through the photo input and pins
both, confirms five penetrations in the Penetrations panel (the first by changing its type), fills in the Save dialog
and saves — in a browser that downloads the .rmiproject file. Then it opens that prospect two ways and compares
window.__rmi.prospect.state() with the state before the save:
  1. same browser profile, after a reload that clears the photo strip: "Open prospect" → the row in "Recent prospects"
  2. a fresh browser profile: "Open prospect" → Browse… → the downloaded file
It prints PASS or FAIL with the differences and every console error or warning, and shoots the dialogs into snapshots/.

Usage (from the repo root; the report and the saved file stay outside the repo — they are client data):
    python scripts/check_prospect.py --eagleview ../RMI-prospects/x/report.XML
    python scripts/check_prospect.py --eagleview ../RMI-prospects/x/report.XML --out ../RMI-prospects/check
"""
import argparse, json, tempfile, time, zipfile
from pathlib import Path

from snapshot import ROOT, OUT, serve, save_png

PHOTOS = [ROOT / "samples" / "sample-01.jpg", ROOT / "samples" / "sample-02.jpg"]


def launch(p):
    return p.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])


def watch(page, errors, tag):
    page.on("pageerror", lambda e: errors.append(f"[{tag}] {e}"))
    page.on("console", lambda m: errors.append(f"[{tag}] {m.type}: {m.text}") if m.type in ("error", "warning") else None)


def idle(page, ms=500):
    page.wait_for_timeout(ms)
    page.wait_for_function("!window.__rmi.prospect.busy()", timeout=120000)


def diff(a, b, at=""):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if at + "." + k in (".dirty",):
                continue
            out += diff(a.get(k), b.get(k), f"{at}.{k}")
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            out += diff(x, y, f"{at}[{i}]")
    elif json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True):
        out.append(f"{at}: {json.dumps(a)[:120]} -> {json.dumps(b)[:120]}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eagleview", required=True, help="EagleView report XML (read where it is, never copied into the repo)")
    ap.add_argument("--out", default=None, help="folder for the downloaded .rmiproject (default: a temp folder)")
    ap.add_argument("--port", type=int, default=8766)
    args = ap.parse_args()
    xml_path = Path(args.eagleview).resolve()
    out = Path(args.out).resolve() if args.out else Path(tempfile.mkdtemp(prefix="rmi-prospect-check-"))
    out.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(exist_ok=True)

    from playwright.sync_api import sync_playwright

    httpd = serve(args.port)
    url = f"http://127.0.0.1:{args.port}/index.html"
    errors, results = [], {}
    try:
        with sync_playwright() as p:
            browser = launch(p)
            ctx = browser.new_context(viewport={"width": 1400, "height": 860}, accept_downloads=True)
            page = ctx.new_page(); watch(page, errors, "save")
            page.goto(url); page.wait_for_timeout(3000)
            xml = xml_path.read_bytes().decode("utf-8")   # no newline translation: the file inside the prospect must match byte for byte
            date = time.strftime("%B %d, %Y", time.localtime(xml_path.stat().st_mtime))
            page.evaluate("([t,n,d])=>{ window.__rmiQuiet=true; return window.__rmi.eagleview.import(t,n,d); }", [xml, xml_path.name, date])
            page.wait_for_timeout(4000)
            page.select_option("#roof", "modbit"); page.wait_for_timeout(3000)
            page.click("#topcoat button[data-v=white]"); page.click("#solar")
            page.fill("#evPH", "4"); page.dispatch_event("#evPH", "change"); page.wait_for_timeout(3000)
            page.locator("#detailChecks input").nth(1).click()
            page.set_input_files("#photoInput", [str(f) for f in PHOTOS]); idle(page, 2000)
            page.evaluate("""()=>{ const d=window.__rmi.eagleview.state().details; window.__rmi.photos.pin(0,0.32,0.46,d[0]); window.__rmi.photos.pin(0,0.7,0.62,d[d.length-1]);
                window.__rmi.photos.pin(1,0.5,0.55,d[Math.min(2,d.length-1)]); window.__rmi.photos.slider(false); window.__rmi.eagleview.open(true); }""")
            page.wait_for_timeout(500)
            sel = page.locator("#evList .evrow select").first
            cur = sel.input_value()
            other = [o for o in sel.locator("option").evaluate_all("os=>os.map(o=>o.value)") if o != cur][0]
            sel.select_option(other); page.wait_for_timeout(3000)
            for i in range(1, 5):
                page.locator("#evList .evrow input[type=checkbox]").nth(i).click(); page.wait_for_timeout(150)
            page.click("#saveBtn"); page.wait_for_timeout(300)
            page.fill("#sName", "Check prospect"); page.fill("#sAddress", "Sample address"); page.fill("#sRep", "RMI rep")
            page.fill("#sNotes", "Browser round trip: two photos pinned, five penetrations confirmed.")
            print("save dialog:", page.inner_text("#sWhat"))
            save_png(page, OUT / "prospect-save-dialog.png")
            with page.expect_download() as dl:
                page.click("#sGo")
            file = out / dl.value.suggested_filename
            dl.value.save_as(str(file)); idle(page)
            print("saved:", page.inner_text("#sStatus"), "->", file, f"{file.stat().st_size:,} bytes")
            before = page.evaluate("window.__rmi.prospect.state()")
            with zipfile.ZipFile(file) as z:   # a standard zip that any tool opens, holding the report and the photos exactly as read
                bad = z.testzip(); pj = json.loads(z.read("prospect.json"))
                same_xml = z.read(pj["eagleview"]["xml"]) == xml_path.read_bytes()
                same_photos = [z.read(ph["file"]) == f.read_bytes() for ph, f in zip(pj["photos"], PHOTOS)]
                print("zip:", [(i.filename, i.file_size) for i in z.infolist()], "| crc ok" if bad is None else f"| BAD {bad}",
                      "| xml identical" if same_xml else "| XML DIFFERS", "| photos identical" if all(same_photos) else "| PHOTOS DIFFER")
                results["file"] = ([] if bad is None else [f"bad zip entry {bad}"]) + ([] if same_xml else ["embedded XML differs from the report"]) + ([] if all(same_photos) and len(same_photos) == 2 else ["embedded photos differ"])
            print(f"before: {before['building']} / {before['roof']} / {before['topcoat']} solar={before['solar']} parapet={before['eagleview']['parapet_height_ft']} "
                  f"confirmed={before['eagleview']['confirmed']} photos={[(x['name'], len(x['pins'])) for x in before['photos']]} dirty={before['dirty']}")

            # 1. same profile: reload, clear what came back from browser storage, open from Recent prospects
            page.reload(); page.wait_for_timeout(3500)
            page.evaluate("window.__rmiQuiet=true; window.__rmi.photos.clear(); window.__rmi.selectBuilding('warehouse');"); page.wait_for_timeout(1500)
            page.click("#openBtn"); page.wait_for_timeout(800)
            print("recent:", [r.replace("\n", " | ") for r in page.locator("#oList .rrow").all_inner_texts()])
            save_png(page, OUT / "prospect-open-dialog.png")
            page.locator("#oList .rrow").first.click(); idle(page, 1500); page.wait_for_timeout(3000)
            results["recent"] = diff(before, page.evaluate("window.__rmi.prospect.state()"))
            page.evaluate("window.__rmi.finishCam(); window.__rmi.setStage(5,false);"); page.wait_for_timeout(800)
            save_png(page, OUT / "prospect-opened.png")
            ctx.close()

            # 2. fresh profile: Browse… → the downloaded file
            ctx = browser.new_context(viewport={"width": 1400, "height": 860})
            page = ctx.new_page(); watch(page, errors, "browse")
            page.goto(url); page.wait_for_timeout(3000)
            page.click("#openBtn"); page.wait_for_timeout(500)
            with page.expect_file_chooser() as fc:
                page.click("#oBrowse")
            fc.value.set_files(str(file)); idle(page, 1500); page.wait_for_timeout(3000)
            after = page.evaluate("window.__rmi.prospect.state()")
            results["browse"] = diff(before, after)
            print(f"after:  {after['building']} / {after['roof']} / {after['topcoat']} solar={after['solar']} parapet={after['eagleview']['parapet_height_ft']} "
                  f"confirmed={after['eagleview']['confirmed']} photos={[(x['name'], x['status'], len(x['pins'])) for x in after['photos']]} dirty={after['dirty']}")
            page.evaluate("window.__rmi.photos.select(0)"); page.wait_for_timeout(800)
            save_png(page, OUT / "prospect-opened-photo.png")
            browser.close()
    finally:
        httpd.shutdown()

    ok = True
    for k, d in results.items():
        print(f"\nround trip via {k}: {'PASS' if not d else 'FAIL'}")
        for line in d[:40]:
            print("  ", line)
        ok = ok and not d
    print("\nBROWSER CONSOLE (errors/warnings):" if errors else "\nno console errors")
    for e in errors[:30]:
        print("  ", e)
    print("\nPASS" if ok and not errors else "\nFAIL")


if __name__ == "__main__":
    main()
