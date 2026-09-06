# RMI Roof Visualizer — project context for Claude Code

## What this is
An interactive web tool for roofrmi.com. A building owner picks a building type, roof type and the
details on their roof, then watches RMI's fluid-applied system (primer → RMI-Flex → RMI-Thane or
RMI-White Plus) applied stage by stage. One Three.js scene: whole roof (macro) with click-to-zoom
details (micro), a section-view toggle, a material estimate and an "email me this configuration" lead capture.

Live demo: https://nihthauke.github.io/RMI-Visualizer/ (GitHub Pages, `index.html` at repo root).
Embedded on Webflow staging at https://roofrmi-update.webflow.io/visualize-your-roof as an iframe.
**Never publish to the roofrmi.com production domain.**

## Hard rules
- Commercial buildings only. No residential types.
- **No pricing anywhere.** The tool outputs a configuration and a material-quantity estimate; dollars come from an RMI rep.
- Every visual traces to an RMI document: spec plates for field application, detail drawings (2D logic + 3D concept) for assemblies.
  Anything not in a document is tagged **ASSUMED** in the UI text; a source document always overrides an assumption.
- Never present an ASSUMED sequence as RMI spec in customer-facing text.
- Chemistry / formulation data never enters this repo. Product performance data (rates, mils, warranties) is fine.
- Drawings and plates in `docs/` are RMI's; the tool depicts generic archetypes, never a real client building.

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
- Three.js r128 from cdnjs; fonts from Google Fonts. Keep the grid tracks `minmax(0,1fr)` — a `1fr` track let the canvas grow the layout inside the Webflow iframe (fixed bug, don't regress).
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

## Working style
Heath prefers short answers and things he can look at. Build one detail, show it in the tool, adjust, then the next.
When a drawing changes something from ASSUMED to VERIFIED, say so explicitly.
