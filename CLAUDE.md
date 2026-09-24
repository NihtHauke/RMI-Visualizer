# RMI Roof Visualizer — project context for Claude Code

## What this is
A private presentation tool for RMI's sales reps, used live with contractors, building owners and architects
(in person or over Zoom screen share). The rep picks a building type, roof type and the details on the roof,
then walks through RMI's fluid-applied system (primer → RMI-Flex → RMI-Thane or RMI-White Plus) stage by
stage. One Three.js scene: whole roof (macro) with click-to-zoom details (micro), a section-view toggle,
a material estimate and a photo panel for the prospect's own roof. Pre-filling RMI's Project Evaluation form
is built as the PDF export's appendix; a standalone form view is not built (`docs/TRACKER.md` §2 #13).

Direction (10 Sept 2026): the final product is a DESKTOP APPLICATION, not a website. Electron wraps the existing
index.html + models into an installer (Windows first; Mac if needed) that reps install and run offline in its own
window. No hosting, no login, no server. Prospect photos load from the rep's machine into a photo panel with pins
that link to details; saved prospects are local files (laptop or shared folder — TBD). Presenting is Zoom screen
share; no share-live link. Drawings may be bundled in the app later. GitHub is source-only and goes private.
GitHub Pages is temporary for team review and goes off at step 6 (repo private), before any RMI drawing is
committed. The installer replaces the review link for reps. Detail models continue in parallel;
nothing in the detail pipeline changes.

Team asks (11 Sept 2026), in build order after the installer:
1. Photo panel — rep loads prospect photos from disk; pins on a photo link to details; in memory only in v1.
2. Drawing panel — a "Drawing" button in detail view shows the RMI 2D drawing (zoomable), the application steps
   in plain language from the drawing notes (ASSUMED steps say so), and the 3D concept on a second tab. Drawings
   are rendered to images at build time from a local folder (`drawings/`, git-ignored until the repo is private)
   and bundled in the installer.
3. PDF export — one click: cover, configuration, six stage images with text, one page per selected detail
   (3D view + steps + drawing), material estimate (NO pricing), photos with pins, ASSUMED notes, pre-filled
   Project Evaluation appendix; per-section toggles. Use Electron's printToPDF and canvas captures.
4. EagleView import — parse the report XML (POINTS x,y,z ft; LINES typed PARAPET/EAVE/FLASHING/OTHER; FACES type
   ROOF with POLYGON path of line ids and elevation, and ROOFPENETRATION with unroundedsize) into a prospect
   building: facets as levels at their elevations, parapets/eaves/flashing lines as the matching details,
   penetrations placed exactly and classified by area (<1 sq ft pipe/vent; 1–10 curb/hatch; 10–30 RTU/skylight;
   >30 large equipment) as a best guess the rep confirms; estimate from the measured totals. Label the roof
   with report number and date; unconfirmed types stay ASSUMED. Report files are client data: local prospect
   folder only, never committed; a sample lives outside the repo for testing.
5. Saved prospects — configuration + photos + report + confirmations as a local file per prospect.

Current temporary build: https://nihthauke.github.io/RMI-Visualizer/ (GitHub Pages, `index.html` at repo root).
**Never publish to the roofrmi.com production domain.**

## Hard rules
- Commercial buildings only. No residential types.
- "Hotel / senior living" is the label for that market. Condominiums are never named anywhere in UI text.
- **No pricing anywhere.** The tool outputs a configuration and a material-quantity estimate; dollars come from an RMI rep.
- Every **detail** visual traces to an RMI document: spec plates for field application patterns and rates, 2D detail drawings for assemblies.
  Building shells (footprint, height, parapet, penthouse, where the RTUs sit) have no RMI drawings — they are generic commercial archetypes
  and are not claimed as RMI spec.
  **The 2D drawing and its notes are the source of truth.** The 3D concept renders in the library were RMI's own attempt to visualize the
  2D logic in three dimensions — treat them as a helpful reference, not as authority. If a more realistic way of showing the assembly
  keeps faith with the 2D drawing's logic, sequence and extents, build it that way.
  Anything not stated in a document (a wrap height, a flange width, an order of operations) is tagged **ASSUMED** in the UI text and the
  catalog so RMI can fill the gap; a source document always overrides an assumption.
- Never present an ASSUMED sequence as RMI spec in customer-facing text.
- Chemistry / formulation data never enters this repo. Product performance data (rates, mils, warranties) is fine.
- Until the repo is private and Pages is off: no RMI PDFs, no client names, no prospect addresses, no EagleView report numbers
  and no real buildings anywhere in it — except `samples/`: client roof photos RMI has written permission to share, EXIF stripped,
  unnamed, unaddressed (exception logged 14 Sept 2026). This covers code and docs alike, including `docs/TRACKER.md` and
  `docs/RMI_Library_Catalog.md`. Chemistry never. The generic
  buildings are archetypes; prospect photos are the only real-roof content and never become part of the archetypes.
- **`drawings/` is never committed while the repo is public.** It holds RMI's detail sheets rendered to PNG (plus `index.js` /
  `index.json`) by `scripts/render_drawings.py` from the local library, is git-ignored, and reaches reps only inside the installer
  (electron-builder.yml `files`). Re-render before every `npm run dist`. Nothing under `drawings/` goes into git until step 6 is done.
- Everything must keep working from a local folder with no network: no CDN dependencies once packaged (vendor
  three.js and GLTFLoader into the repo), no absolute URLs, model paths relative to index.html.

## Current state (Sept 2026)
- 11 building types: warehouse, big-box retail, school, office, manufacturing, hospital, arena/gym,
  silo/grain elevator, hotel/senior living, airport hangar, restaurant.
- 7 roof types, each from its spec plate: R-panel (MP), standing seam (MP), SPF (SPF), TPO/PVC/EPDM (SP),
  mod-bit granule (A-G), gravel BUR (MA-GR, Thane only), concrete/LIC (C).
- Two field patterns: **seam-trace** (metal: primer + Flex on seams, laps, fasteners, curbs, penetrations; full-field topcoat)
  and **full-field** (everything else: primer, Flex, topcoat over the whole roof). Every roof runs the same six stages
  (existing, prep, primer, Flex, topcoat, finished); on gravel BUR the gravel is swept off inside Prep, not as a separate stage.
  Ballast removal is not built — ballasted single-ply (Plate SPB) is not one of the 7 roof types.
- Detail menu: a per-building checkbox list (`BUILDINGS[].details`) — not a roof-type filter and not a dropdown. The roof type
  only swaps a detail's name and drawing (`byRoof`).
- 28 detail rows (the 25 `DETAILS` entries + 2 concrete `byRoof` variants + the Solar Post toggle), keyed to drawing numbers.
  Status as in `docs/TRACKER.md` §1: **22 MODELLED+SPLICED · 0 MODELLED · 6 CODE-DRAWN · 0 NOT STARTED.**
  Spliced models still carry open ASSUMED items (listed per row in the tracker).
  - **MODELLED+SPLICED (19):** R-panel side lap F-8-TYP · standing seam F-9-TYP / F-20-TYP · bin vent CS-12-CON (CS-1-TYP note 7) ·
    manway / bin hatch CS-14-CON (CS-1-TYP note 7) · ridge cap F-21-M-TYP · HVAC curbs / RTU CS-1-TYP · drains D-1-TYP / D-2-TYP ·
    scuppers D-4-TYP · wall tie-in, reglet W-11-TYP · soil stacks P-6-TYP · skylights, curb-mounted CS-1-TYP note 7 ·
    kitchen exhaust CS-1-TYP note 7 · parapet / coping W-1-TYP · sleeper supports CS-8-TYP · pipe clusters / Chem-Curb P-8-TYP ·
    penthouse walls, fixed counterflashing W-13-TYP · perimeter edge metal F-1-TYP · expansion joint A-3-TYP ·
    gallery supports P-5-C (P-7-C reference) · HVAC curb on metal CS-13-MP (warehouse) · vents on metal CS-13-MP note 7
    (no vent sheet exists; manufacturing, arena) · roof hatch on metal CS-15-MP (arena). The three metal curbs share
    `scripts/rmi_metal_curb.py`: one model per roof profile and pitch, spliced into the slope like the lap (`MCURB`, `unitAt`).
  - **CODE-DRAWN (6):** skylight panels, flush F-12-TYP · pipes on metal P-9-MP · gutters W-7-TYP · downspout inlets D-8-TYP ·
    silo walls W-7-TYP · Solar Post supports P-1-S-TYP / P-2-S-TYP / P-3-S-TYP.
- Product features: desktop installer v0.3.0 **built** (`dist/RMI Roof Visualizer Setup 0.3.0.exe`; RMI crest icon in `build/`, RMI logo `assets/rmi-logo.png` in the header, PDF cover and PDF page header);
  v0.3.1 packages (`dist/win-unpacked`) but the `.exe` does not: Smart App Control blocks the unsigned NSIS uninstaller stub `npm run dist` has to run (`docs/TRACKER.md` §2 #12);
  photo panel **done** (v2: top strip, docked slider, IndexedDB persistence, sample set — the app reads the bundled `samples/` through `rmiDesktop.samplePhotos`, since `fetch()` cannot read inside `app.asar`);
  drawing panel **built** (15 Sept 2026: "Drawing" button in detail view docks a panel with the 2D sheet zoom/pan, "How it's applied" steps from `STEPS` in
  index.html with ASSUMED tagged, and the 3D concept; sheet number and issue/revision date from the sheet; 52 sheets rendered locally into `drawings/`, bundled by the installer, git-ignored).
  PDF export **built** (15 Sept 2026: "Export PDF" in the header; dialog with prospect, rep, notes and per-section toggles; canvas captures at the default
  cameras; Electron `printToPDF` via `rmiDesktop.exportPdf`, browser print dialog otherwise; the Project Evaluation pre-fill ships as its appendix).
  EagleView import **built** (15 Sept 2026: "Import EagleView report" in the header reads the report XML — native dialog in Electron via
  `rmiDesktop.pickEagleView`, a file input in a browser — and builds `BUILDINGS.prospect` / `buildProspect()`: each ROOF facet a polygon block
  (`makePolyBlock`) at its elevation, PARAPET edges parapet + coping, EAVE edges F-1 edge metal, FLASHING edges the W-11 tie-in, a PARAPET edge
  against a higher facet the W-13 penthouse wall; penetrations at their centroids typed by area (best guess, ASSUMED until confirmed in the
  "Penetrations" panel); the estimate from the report's measured totals with the parapet height entered by the rep; PDF cover, configuration,
  penetration schedule, estimate basis and notes carry the report; `configuration().eagleview` for saved prospects; `__rmi.eagleview` API).
  Saved prospects **built** (16 Sept 2026: "Open prospect" / "Save prospect" in the header; one `.rmiproject` per prospect — a zip written and read in
  the page, no library — holding `prospect.json` (prospect / address / rep / notes, restore keys, parapet height, the EagleView block with every penetration's
  type and confirmation, photo files and pins, the full `configuration()`), the original XML under `eagleview/` and the photos under `photos/`. Desktop:
  `rmiDesktop.prospects` writes to a folder chosen once and remembered in userData `settings.json` (default Documents\RMI Prospects), saving again
  updates the same file, another prospect's file is never overwritten; browser: downloads. Open dialog: "Recent prospects" (desktop settings; browser
  IndexedDB copies) + Browse…; open validates the whole file before changing anything, then rebuilds the roof from the embedded XML, the confirmations,
  the photos and pins; `__rmi.prospect` API. `*.rmiproject` is git-ignored — prospect files are client data).
- Full index of drawings ↔ details ↔ status: `docs/RMI_Library_Catalog.md` (keep it current; it is the punch list for RMI's technical side).

## What's left (in order)
1. Remaining detail models — the 6 CODE-DRAWN rows, in the order the buildings need them.
2. Fine-tuning — labels, camera pass, silo headhouse/shed.
3. Textures.
4. Catalog alignment with the 25 `DETAILS` entries (the detail menu is a per-building checkbox list, not a dropdown).
5. ASSUMED questions to RMI (catalog §5).
6. Repo private, Pages off, transfer to an RMI-owned GitHub organization — in one step, so RMI controls
   collaborator access. Until then the repo stays under nihthauke for team review. Committing `drawings/` waits on
   this (no RMI drawings in the repo while it is public); the panel itself is built and reads the git-ignored folder.
7. Drawing panel — **built 15 Sept 2026** (sheets render locally; see the `drawings/` rule above).
8. PDF export — **built 15 Sept 2026** (the Project Evaluation pre-fill is its appendix; a standalone form view is still open).
9. EagleView import — **built 15 Sept 2026** (report files stay outside the repo; `*.xml` is git-ignored).
10. Saved prospects — **built 16 Sept 2026** (`*.rmiproject` is git-ignored; where the folder lives — laptop or shared — is still the team's call).
11. Bundled drawings, code signing, wide rollout.

## Code layout
- `index.html` — currently the whole app (CSS + JS in one file, ~125 KB). Data-driven:
  `ROOFS` (per-plate rates, stage text, system codes), `DETAILS` (per-drawing name, layers text, camera, `byRoof` overrides),
  `BUILDINGS` (shell + which roofs/details), builders (`buildGable`, `makeBlock` + flat helpers, per-building functions).
  Stage progress `p = {prep, primer, flex, thane}` drives everything; flat roofs use world-space clipping planes to "sweep"
  overlays across x; metal roofs animate seam strips along the slope.
- Planned split: `src/` for JS modules, `models/` for `.glb` + `.blend`, `scripts/` for Blender build scripts, `textures/`, `docs/`.
- Three.js r128 + GLTFLoader, heic2any and the Barlow woff2 fonts are vendored in `vendor/` (no CDN, no Google Fonts).
  `electron/main.js` + `electron/preload.js` wrap the same `index.html`; `npm start` runs it, `npm run dist` builds the Windows
  installer into `dist/` (electron-builder.yml; `.blend` files are excluded). `RMI_DEBUG=1` mirrors the page console to stdout;
  F12 opens DevTools. The web build (Pages, snapshot.py) is unchanged — same file, no fork. Keep the grid tracks `minmax(0,1fr)` — a `1fr` track let the canvas grow the layout inside the Webflow iframe (fixed bug, don't regress).
- Test with Playwright + swiftshader; `window.__rmi` exposes `S`, `setStage`, `goDetail`, `goRoof`, `selectBuilding`, `finishCam`, `flyTo` (aim at any point), `photos`, `drawing`
  (`open`, `tab`, `state`), `prospect` (`save`, `open`, `openRecent`, `state`) for scripted screenshots; `snapshot.py --drawing [2d|steps|3d]` shoots the panel. `RMI_SELFTEST=<png>` makes the
  packaged app open the big-box drain with the panel, print the panel state and save a screenshot, then quit (the installer check).
  `RMI_SELFTEST_PDF=<pdf>` exports the big-box presentation with the sample photos pinned to that path and quits (the export check).
  `RMI_SELFTEST_EV=<xml>` imports that EagleView report, prints the import state, saves a whole-roof screenshot (`RMI_SELFTEST_PNG`) and, with
  `RMI_SELFTEST_PDF`, exports its PDF (the import check); the selftests run in their own userData folder. `snapshot.py --eagleview <xml>` shoots the
  prospect roof (`--detail`, `--pdf` for a page.pdf() export); the sample report lives outside the repo (`../RMI-prospects/`).
  Saved prospects: `scripts/check_prospect.py --eagleview <xml>` is the browser round trip (save → reopen from Recent and from Browse…, state compared,
  zip entries byte-identical); `RMI_SELFTEST_PROSPECT=<folder>` is the installed-app round trip in two launches — with `RMI_SELFTEST_PROSPECT_XML=<xml>`
  and `RMI_SELFTEST_PHOTOS=<a,b>` it builds and saves the prospect (two photos pinned, five penetrations confirmed), without them it reopens it from
  "Recent prospects", compares, re-saves in place and prints PASS / FAIL. Keep its folder and the saved file outside the repo.
- PDF export: `pdfExport()` in index.html — `pdfCaptures` renders the scene at fixed sizes (`pdfCapture`, 2D composite so JPEG gets the
  view background, hotspot labels drawn on the configuration image), `pdfBuild` writes the sections into `#pdfDoc`, `body.pdf` switches the
  `@media print` CSS to that document, then `rmiDesktop.exportPdf` (Electron: save dialog + `printToPDF`, main.js) or `window.print()`.
  `__rmi.pdf` exposes `open`, `export`, `prepare` (build without printing, for `page.pdf()` checks), `done`, `state`. `DETAIL_GAL` holds
  the per-detail Flex allowances the estimate and the PDF share; `PE_ITEMS` maps detail ids to RMI's Project Evaluation checklist.
- Drawing panel data: `DETAILS[].drawing` / `.concept` name the sheets; `DETAILS[].steps` (from the `STEPS` block above `DETAILS`) is the
  plain-language sequence; `sheet` overrides the image name when two sheets share a number (gutter seams: `W-7-TYP-GUTTER`). Images are
  `drawings/<number>.png`; `drawings/index.js` sets `window.RMI_DRAWINGS` (title, issue/revision, size) and is loaded with a `<script>` on
  first open because `fetch()` does not work on `file://` in Electron. A missing sheet shows a message, never an error.

## Blender model conventions (for the detail rebuild)
- One `.blend` + one `.glb` per detail in `models/`, named `<detail>-<DRAWING-NO>.glb` (e.g. `cast-iron-drain-D-1-TYP.glb`).
- Build scripts in `scripts/`, one per detail, dimensions as named constants at the top with the drawing note they came from.
- Units: metres in Blender, modelled from inches (`IN = 0.0254`). The web scene is in feet; the loader scales by 3.2808.
- Layers are **collections named exactly** `existing`, `primer`, `flex`, `topcoat`. The visualizer toggles them per stage.
- Materials come from one shared library: `RMI_Flex`, `RMI_Thane`, `RMI_White`, `RMI_primer`, `RMI_castiron`, `RMI_coping_metal`,
  `RMI_membrane`, `RMI_modbit`, `RMI_concrete`, `RMI_tape`, `RMI_sealant`, `RMI_fastener`. Change a material once, every detail follows.
- Export: glTF Binary, apply modifiers, Draco compression on. Keep textures at 1K–2K.
- Remaining models follow the TRACKER.md details table; curb variants (vents, hatch, exhaust) share the CS-1 pattern, gutter pairs with inlet.
- Metal-roof curbs (`scripts/rmi_metal_curb.py`): the panel patch is built in the panel frame from the app's own rib / coat numbers, the
  curb and unit level and then tilted onto the slope; the build script carries each building's lap phase and purlin rows, so moving a
  unit on a slope means rebuilding its model. A liftable unit ships lifted `MCURB[kind].lift` inches (14" — its counterflashing is 4").

## The working loop (Claude Code)
For every detail or code change, in this order:
1. Read the drawing(s) for the detail (2D logic + 3D concept). **Drawings and plates are NOT in the repo** — the repo is public. Read them from the local library:
   `C:\Users\hcarr\OneDrive\Documents\Claude\Projects\2024 Master RMI Library\`
   (2D details under `2024 Detail Drawings\...`, 3D renders under `2024 3D Details\...`, plates under `2024 Specifications\2024 Master Specification Plates\`; `docs/RMI_Library_Catalog.md` maps every detail to its drawing numbers). Never copy PDFs into the repo.
   Write down the dimensions the drawing gives; anything it doesn't give is ASSUMED.
2. Write `scripts/build_<detail>_<DRAWING-NO>.py` using `scripts/rmi_blender.py` (see its docstring). Dimensions as named constants at the top with the note they came from.
   Run it headless: `blender -b --python scripts/build_<...>.py` (Blender is at `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`). Never open .blend files from inside a running Blender session via script — it crashes.
3. Register the model in `index.html` (`MODELS` map) and give it a mount point + cutout sizes in the builder (see `addDrain` / `addRTU`). The coating cutout must sit just INSIDE the model's own Flex extent; the membrane cutout just inside the model's roof patch.
4. Visual check: `python scripts/snapshot.py --building <b> --detail <id>` (and `--section`, `--drawing`). Open the contact sheet and LOOK at every stage. Fix anything wrong before pushing. Zero console errors is the bar.
   Sheet numbers changed or a new detail added? `python scripts/render_drawings.py` re-renders `drawings/` (it reports any number it cannot find).
5. `git add . && git commit -m "<what changed>" && git push`
6. Update the detail's line in `docs/RMI_Library_Catalog.md` (model file, VERIFIED/ASSUMED) and tell Heath what moved from ASSUMED to VERIFIED.

**`docs/TRACKER.md`** is the single project status page. Every task still updates its TRACKER rows (status tables,
detail table) in the same commit — those must stay accurate. Do NOT add per-task log lines. §4 is a weekly update
written on Fridays. Per-drawing ASSUMED questions stay in the catalog; the tracker links to them.
Setup once: `pip install playwright pillow && playwright install chromium`. `snapshots/` is git-ignored.

## Lessons already learned (don't repeat)
- The glTF exporter writes hidden objects. Cutters/boolean helpers must be baked and deleted before export (`finalize()` does this). The loader also ignores any mesh not named `<layer>__...`.
- Roof field sheets are flat planes an inch above the deck; a model with a recessed part (drain sump) needs a cutout in those sheets or the sweep covers it.
- CSS grid tracks must be `minmax(0,1fr)`; a bare `1fr` let the canvas grow the layout inside the Webflow iframe.
- Blender's `.blend1` backups are git-ignored; keep it that way.

## Working style
Heath prefers short answers and things he can look at. Build one detail, show it in the tool, adjust, then the next.
When a drawing changes something from ASSUMED to VERIFIED, say so explicitly.
