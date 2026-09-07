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
- The repo is public (GitHub Pages). No RMI PDFs, no chemistry, no client names in it. The tool depicts generic archetypes, never a real client building.

## Current state (Sept 2026)
- 11 building types: warehouse, big-box retail, school, office, manufacturing, hospital, arena/gym,
  silo/grain elevator, hotel/senior living, airport hangar, restaurant.
- 7 roof types, each from its spec plate: R-panel (MP), standing seam (MP), SPF (SPF), TPO/PVC/EPDM (SP),
  mod-bit granule (A-G), gravel BUR (MA-GR, Thane only), concrete/LIC (C).
- Two field patterns: **seam-trace** (metal: primer + Flex on seams, laps, fasteners, curbs, penetrations; full-field topcoat)
  and **full-field** (everything else: primer, Flex, topcoat over the whole roof). Two roof-specific pre-stages: gravel removal, ballast removal.
- 28 detail types, keyed to drawing numbers. Eight are rebuilt to their drawings and VERIFIED:
  curb CS-1-TYP / CS-13-MP, drain D-1-TYP, soil stack P-6-TYP, coping W-1-TYP, reglet W-11-TYP,
  R-panel lap F-8-TYP, standing seam F-9-TYP, scupper D-4-TYP. Eight ship as Blender models in `models/` (curb, drain, soil stack, coping,
  reglet, scupper, R-panel side lap, standing seam); the rest are generic code geometry pending the same treatment.
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
- `scripts/snapshot.py --building <b> --detail <id> [--section]`: a `<id>` the building does not carry (office has no `coping`) is skipped with a message listing the ones it does have. It retries around Windows file locks on the PNGs.

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
- Cutout margins: the field coating sheets float ~1" above the roof, so at the oblique detail camera you see ~1.7" of ground under the far edge of a hole. The primer/Flex hole must sit **≥2.5" inside** the model's own Flex extent (not "just inside"), and the topcoat sheet's hole is 1" smaller again (`applyCutouts`), otherwise the Flex sheet shows as a yellow arc at the finished stage.
- CSS grid tracks must be `minmax(0,1fr)`; a bare `1fr` let the canvas grow the layout inside the Webflow iframe.
- Blender's `.blend1` backups are git-ignored; keep it that way.
- Coping runs are built in a run-local frame where +z is world +z on N/S and world +x on W/E, so it points OUTWARD only on S and E. Anything one-sided (fasteners, and a spliced model's fastener face) needs the `out` sign, or it lands on the inside face of half the building.
- A model spliced into a code-drawn run (the W-1-TYP coping section) must copy the run's cross-section exactly, and its coat boxes must be the same shape as the run's overlay boxes — any coplanar overlap or a filled-vs-notched corner shows as a bright line at the seams in the finished stage.
- Every shipped model has a build script in `scripts/` (`build_<detail>_<DRAWING-NO>.py`). Regenerate, never hand-edit a `.blend`. `rmi_blender.Shell` builds revolved parts as one mesh per layer (cheap when a roof carries dozens of instances); `box`/`cyl`/`torus` + `helper`/`cut` for the rest. Blender's cone `radius1` is the BOTTOM.
- `index.html` is one-line-per-function in places. Never append a `//` comment to a replaced fragment unless it is the true end of the line — twice now a trailing comment swallowed the rest of a function (`condFor`, `tilt`) and took the whole page down. Use `/* */` mid-line, and run `node --check` on the extracted inline script before a snapshot.
- Every `skins` entry passed to `mountModel` must exist in `M`. A missing one (`M.wood` did not exist) assigns `undefined` as a mesh material, which crashes three's render loop — the page then silently shows the roof view in every snapshot.
- makeBlock insets the field by `PT` on every side, including a skipped (parapet-less) side. A wall tie-in on such a side sits at `IL/2 + PT`, not `IL/2`, and needs a filler strip of field material across that inch-per-foot ledge (`addWallTie` does this).
- Cameras: `python scripts/snapshot.py --building <b> --detail <id> --cam dist,theta,phi[,drop] --stages 4,6` tries a camera without editing `DETAILS` (it writes `window.__rmi.DETAILS[id]`). At the finished stage everything is topcoat-grey and a frontal view has no depth cues — judge a camera on stages 1 and 4, then check 6.
- Every parapet run carries a cant + base flashing + full-height coats (`parapetBase`, constants in `PB`). A wall-mounted model that splices into a parapet (`makeBlock` `splices:[{k,at,id}]`) must draw that same base from the same numbers, or the seams show; `build_overflow_scupper_D-4-TYP.py` is the pattern. A splice that hides with a checkbox needs a plug (see `setScuppers`) or the parapet shows a hole.
- The field overlay sheets float ~1" up, so a model's roof patch must be re-skinned with the block's field material (`mountModel(..., {membrane: b.fieldPlanes[0].material})`) or it shows as a grey disc on mod-bit/concrete roofs.
- Metal (gable) roofs sweep only the topcoat; `buildGable`'s `applyStage` used to park `clipFlex`/`clipPrim` at -1000, which clips away any model's primer/Flex there. They now sit at +1000. A model on a slope is skinned with the slope's `M.*` materials (`panel`, `rib`, `fastener`, `rust`, `sealant`, `primer`, `flex`, `topcoat`) and its holder gets `userData.gate={flex:z0/SL}` so its Flex appears when the lap strip has swept down to it (`applyModels` honours the gate). `M.rust` on a model's rust discs fades them through prep for free.
- Splicing into a panel run (`cfg.lapModel` in `buildGable`): the field and topcoat sheets get a hole (`slopeSheet`), the rib and lap `InstancedMesh`es carry one extra instance so the bay's rib is drawn as two pieces, purlin fasteners inside the bay are dropped and rust patches keep off that lap. The lap coat profiles come from `LAP` + `lapProfile()` and the build script's `lap_profile()` — same numbers or the bay ends show.
- `prepModel`'s primer-opacity statement was the third swallowed-by-`//` casualty; model primer now renders at 75% opacity as intended (checked on the coping).
- A model part named `<layer>__..._before_...` / `..._after_...` is swapped by `applyModels` at the halfway point of the prep stage — the way the standing seam's loose cap is re-crimped (F-9-TYP note 11). Use it for prep work that CHANGES geometry; `M.rust`'s fade covers prep work that only changes colour.
- A spliced model must cover its whole bay with no butt lines: the standing seam's two pans left a hairline at x=0 and an open slot between the seam legs, and the concealed clip underneath showed through both. One continuous pan sheet under the seam fixed it. Anything meant to be hidden inside an assembly needs the assembly to actually be closed.
- Judge a detail camera on the stage where the geometry reads, not the finished stage — and check the sun. On standing seam the seam's own shadow is a 1-ft band on a 2-ft pitch, and at some thetas the seam's lit face is the same value as the pan, so a correct model looks like a flat stripe. `theta` near the seam's own direction (0.45 on the manufacturing slope) gives depth; the Section view is the clearest shot of a seam assembly.
- A contact sheet used to sign off a detail must be shot with the **default** camera (`snapshot.py --building <b> --detail <id>`, no `--cam`). `--cam` is for hunting a camera only; a sheet shot with an override proves nothing about what a visitor sees when they click the hotspot, and it hides anchor/framing bugs. Once a camera is chosen, write it into `DETAILS` and re-shoot without `--cam`.

## Working style
Heath prefers short answers and things he can look at. Build one detail, show it in the tool, adjust, then the next.
When a drawing changes something from ASSUMED to VERIFIED, say so explicitly.
