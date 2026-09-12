# RMI Roof Visualizer — project context for Claude Code

## What this is
A private presentation tool for RMI's sales reps, used live with contractors, building owners and architects
(in person or over Zoom screen share). The rep picks a building type, roof type and the details on the roof,
then walks through RMI's fluid-applied system (primer → RMI-Flex → RMI-Thane or RMI-White Plus) stage by
stage. One Three.js scene: whole roof (macro) with click-to-zoom details (micro), a section-view toggle,
a material estimate, a photo panel for the prospect's own roof, and a summary that pre-fills RMI's
Project Evaluation form.

Direction (10 Sept 2026): the final product is a DESKTOP APPLICATION, not a website. Electron wraps the existing
index.html + models into an installer (Windows first; Mac if needed) that reps install and run offline in its own
window. No hosting, no login, no server. Prospect photos load from the rep's machine into a photo panel with pins
that link to details; saved prospects are local files (laptop or shared folder — TBD). Presenting is Zoom screen
share; no share-live link. Drawings may be bundled in the app later. GitHub is source-only and goes private;
Pages is a temporary review build until the first installer ships. Detail models continue in parallel;
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
- Until the repo is private and Pages is off: no RMI PDFs, no client names, no real buildings in it. Chemistry never. The generic
  buildings are archetypes; prospect photos are the only real-roof content and never become part of the archetypes.
- Everything must keep working from a local folder with no network: no CDN dependencies once packaged (vendor
  three.js and GLTFLoader into the repo), no absolute URLs, model paths relative to index.html.

## Current state (Sept 2026)
- 11 building types: warehouse, big-box retail, school, office, manufacturing, hospital, arena/gym,
  silo/grain elevator, hotel/senior living, airport hangar, restaurant.
- 7 roof types, each from its spec plate: R-panel (MP), standing seam (MP), SPF (SPF), TPO/PVC/EPDM (SP),
  mod-bit granule (A-G), gravel BUR (MA-GR, Thane only), concrete/LIC (C).
- Two field patterns: **seam-trace** (metal: primer + Flex on seams, laps, fasteners, curbs, penetrations; full-field topcoat)
  and **full-field** (everything else: primer, Flex, topcoat over the whole roof). Two roof-specific pre-stages: gravel removal, ballast removal.
- 28 detail types, keyed to drawing numbers. Eight are rebuilt to their drawings and VERIFIED:
  curb CS-1-TYP / CS-13-MP, drain D-1-TYP, soil stack P-6-TYP, coping W-1-TYP, reglet W-11-TYP,
  R-panel lap F-8-TYP, standing seam F-9-TYP, scupper D-4-TYP. The rest are generic code geometry pending the same treatment.
- Full index of drawings ↔ details ↔ status: `docs/RMI_Library_Catalog.md` (keep it current; it is the punch list for RMI's technical side).

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
- Test with Playwright + swiftshader; `window.__rmi` exposes `S`, `setStage`, `goDetail`, `goRoof`, `selectBuilding`, `finishCam` for scripted screenshots.

## Blender model conventions (for the detail rebuild)
- One `.blend` + one `.glb` per detail in `models/`, named `<detail>-<DRAWING-NO>.glb` (e.g. `cast-iron-drain-D-1-TYP.glb`).
- Build scripts in `scripts/`, one per detail, dimensions as named constants at the top with the drawing note they came from.
- Units: metres in Blender, modelled from inches (`IN = 0.0254`). The web scene is in feet; the loader scales by 3.2808.
- Layers are **collections named exactly** `existing`, `primer`, `flex`, `topcoat`. The visualizer toggles them per stage.
- Materials come from one shared library: `RMI_Flex`, `RMI_Thane`, `RMI_White`, `RMI_primer`, `RMI_castiron`, `RMI_coping_metal`,
  `RMI_membrane`, `RMI_modbit`, `RMI_concrete`, `RMI_tape`, `RMI_sealant`, `RMI_fastener`. Change a material once, every detail follows.
- Export: glTF Binary, apply modifiers, Draco compression on. Keep textures at 1K–2K.
- Order of rebuild: the eight VERIFIED details first, then the remaining twenty in the order the buildings need them.

## The working loop (Claude Code)
For every detail or code change, in this order:
1. Read the drawing(s) for the detail (2D logic + 3D concept). **Drawings and plates are NOT in the repo** — the repo is public. Read them from the local library:
   `C:\Users\hcarr\OneDrive\Documents\Claude\Projects\2024 Master RMI Library\`
   (2D details under `2024 Detail Drawings\...`, 3D renders under `2024 3D Details\...`, plates under `2024 Specifications\2024 Master Specification Plates\`; `docs/RMI_Library_Catalog.md` maps every detail to its drawing numbers). Never copy PDFs into the repo.
   Write down the dimensions the drawing gives; anything it doesn't give is ASSUMED.
2. Write `scripts/build_<detail>_<DRAWING-NO>.py` using `scripts/rmi_blender.py` (see its docstring). Dimensions as named constants at the top with the note they came from.
   Run it headless: `blender -b --python scripts/build_<...>.py` (Blender is at `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`). Never open .blend files from inside a running Blender session via script — it crashes.
3. Register the model in `index.html` (`MODELS` map) and give it a mount point + cutout sizes in the builder (see `addDrain` / `addRTU`). The coating cutout must sit just INSIDE the model's own Flex extent; the membrane cutout just inside the model's roof patch.
4. Visual check: `python scripts/snapshot.py --building <b> --detail <id>` (and `--section`). Open the contact sheet and LOOK at every stage. Fix anything wrong before pushing. Zero console errors is the bar.
5. `git add . && git commit -m "<what changed>" && git push`. Pages updates in about a minute.
6. Update the detail's line in `docs/RMI_Library_Catalog.md` (model file, VERIFIED/ASSUMED) and tell Heath what moved from ASSUMED to VERIFIED.
Setup once: `pip install playwright pillow && playwright install chromium`. `snapshots/` is git-ignored.

## Lessons already learned (don't repeat)
- The glTF exporter writes hidden objects. Cutters/boolean helpers must be baked and deleted before export (`finalize()` does this). The loader also ignores any mesh not named `<layer>__...`.
- Roof field sheets are flat planes an inch above the deck; a model with a recessed part (drain sump) needs a cutout in those sheets or the sweep covers it.
- CSS grid tracks must be `minmax(0,1fr)`; a bare `1fr` let the canvas grow the layout inside the Webflow iframe.
- Blender's `.blend1` backups are git-ignored; keep it that way.

## Working style
Heath prefers short answers and things he can look at. Build one detail, show it in the tool, adjust, then the next.
When a drawing changes something from ASSUMED to VERIFIED, say so explicitly.
