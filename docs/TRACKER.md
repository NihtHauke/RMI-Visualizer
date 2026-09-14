# RMI Roof Visualizer — Project Tracker

The single status page. Per-drawing ASSUMED questions live in the catalog, not here:
[RMI_Library_Catalog.md](RMI_Library_Catalog.md) — §3c is the per-detail sync table, [§5](RMI_Library_Catalog.md#5-open-questions-for-rmi)
is the numbered list of open questions for RMI (cited below as §5 #n).

Rule: every task updates the row it touched and adds one dated line to the update log, in the same commit as the work.

---

## 1. Details

28 rows = the 25 entries in `DETAILS` (index.html) + the 2 `byRoof` variants that show the rep a different detail on
concrete (Bin vent, Manway / bin hatch) + the Solar Post toggle (`S.solar`).

**Status key.** MODELLED+SPLICED — a Blender `.glb` is mounted in at least one building's scene (`mountModel`).
MODELLED — a `.glb` exists but nothing mounts it. CODE-DRAWN — generic Three.js geometry only. NOT STARTED — no geometry.
Where a model covers only some instances, the Detail cell says where; the rest of that detail is still code-drawn.
Roof types are those of the buildings that carry the detail.

| Detail | Drawing No. | Roof Types | Status | Open ASSUMED |
|---|---|---|---|---|
| HVAC curb on metal (`curb`) | CS-13-MP · SPF → SPF-12-TYP | R-panel, standing seam, SPF | CODE-DRAWN | Curb sizes; SPF wrap height (§5 #15) |
| R-panel side lap (`lap`) — warehouse slope | F-8-TYP | R-panel | MODELLED+SPLICED | Rib, lap lips, fastener spacing, Flex extent past the rib (§5 #10) |
| Standing seam (`sseam`) — manufacturing slope | F-9-TYP, F-20-TYP | Standing seam | MODELLED+SPLICED | Seam silhouette, clip spacing, Flex extent (§5 #11) |
| Skylight panels, flush (`mskylight`) | F-12-TYP · SPF → none | R-panel, standing seam, SPF | CODE-DRAWN | Geometry (no 3D render); SPF treated as a curb (§5 #13) |
| Vents on metal / SPF (`vent`) | Plate D · SPF → SPF-16-TYP | R-panel, standing seam, SPF | CODE-DRAWN | Whole metal assembly, no drawing (§5 #12); SPF wrap height (§5 #15) |
| Bin vent (`vent` on concrete) — silo cap | CS-12-CON; CS-1-TYP note 7 | Concrete | MODELLED+SPLICED | Shared curb numbers (§5 #5); concrete skinning of the curb |
| Pipes on metal (`mpipe`) | P-9-MP (P-10-MP alt.) · SPF → SPF-3-TYP | R-panel, standing seam, SPF | CODE-DRAWN | SPF wrap height (§5 #15) |
| Gutters (`gutter`) | W-7-TYP | Standing seam, R-panel, SPF | CODE-DRAWN | None flagged yet — sizes will be ASSUMED when modelled |
| Downspout inlets (`gutterinlet`) | D-8-TYP | Standing seam, R-panel, SPF | CODE-DRAWN | None flagged yet — sizes will be ASSUMED when modelled |
| Roof hatch on metal / SPF (`hatch`) — arena | CS-15-MP · SPF → SPF-12-TYP | Standing seam, R-panel, SPF | CODE-DRAWN | CS-15-MP is a different assembly, next curb model (§5 #14); SPF wrap (§5 #15) |
| Manway / bin hatch (`hatch` on concrete) — silo cap | CS-14-CON; CS-1-TYP note 7 | Concrete | MODELLED+SPLICED | Lid size, open angle, hinge; concrete skinning; shared curb numbers (§5 #5) |
| Ridge cap (`ridge`) — warehouse only | F-21-M-TYP · SPF → SPF-2-TYP | R-panel, standing seam, SPF | MODELLED+SPLICED | Cap lap, closure position (§5 #16); model built for a 1:12 gable |
| HVAC curbs / RTU (`rtu`) — 8 × 1.5 ft curbs: big-box, hospital wing | CS-1-TYP | TPO, mod-bit, gravel BUR, concrete | MODELLED+SPLICED | Curb and unit sizes, nailer, skirt, Flex apron and turn-down (§5 #5) |
| Drains (`drain`) — all seven flat buildings | D-1-TYP, D-2-TYP | TPO, mod-bit, gravel BUR, concrete | MODELLED+SPLICED | Bowl, clamping-ring and dish sizes |
| Scuppers (`scupper`) — big-box north parapet | D-4-TYP | TPO, mod-bit, gravel BUR | MODELLED+SPLICED | Tube size, exterior termination, 12" measured from where (§5 #8); cant and flashing height (§5 #7) |
| Wall tie-in, reglet (`wall`) — school gym wall | W-11-TYP | Mod-bit, TPO | MODELLED+SPLICED | Flashing height, reglet, counterflashing lap (§5 #6) |
| Soil stacks (`pipe`) — all five buildings | P-6-TYP | TPO, mod-bit, gravel BUR, concrete | MODELLED+SPLICED | Every dimension (§5 #9) |
| Skylights, curb-mounted (`skylight`) — school | CS-1-TYP note 7 | Mod-bit, TPO | MODELLED+SPLICED | Dome rise, retainer frame, condensation gutter; shared curb numbers (§5 #5) |
| Edge metal (`edge`) — office east edge at the hotspot; every office edge draws the same cross-section in code | F-1-TYP | TPO, concrete, mod-bit | MODELLED+SPLICED | Tape at the edge joint, Flex down the fascia and face fasteners (none on the drawing); flange, fascia, stripping and cleat sizes (§5 #22) |
| Penthouse walls (`penthouse`) — office penthouse west face | W-13-TYP | TPO, mod-bit, gravel BUR, concrete | MODELLED+SPLICED | Counterflashing height, depth and stand-off; cant; skirt size and lap; fastener spacing; skirt fitted after the topcoat (§5 #21) |
| Sleeper supports (`sleeper`) — office hotspot sleeper, hotel hotspot condenser | CS-8-TYP | TPO, mod-bit, concrete | MODELLED+SPLICED | Every dimension (NTS): sleeper, pad, 6" raise, patch; whether the (E) condition has a pad |
| Pipe clusters / Chem-Curb (`pitchpan`) — all three hospital pans | P-8-TYP | Gravel BUR, mod-bit, TPO, concrete | MODELLED+SPLICED | Every dimension (NTS): curb, penetrations, fill crown, Flex field extent; curb set before or after priming (§5 #20) |
| Expansion joint (`ej`) | A-3-TYP | Gravel BUR, mod-bit, TPO, concrete | CODE-DRAWN | Geometry, no 3D render (§5 #16) |
| Silo walls (`silowall`) | W-7-TYP | Concrete | CODE-DRAWN | Sequence and coverage on a curved wall (§5 #17) |
| Gallery supports (`support`) | P-5-C, P-7-C | Concrete | CODE-DRAWN | Wrap height (§5 #15) |
| Kitchen exhaust (`exhaust`) — restaurant | CS-1-TYP note 7 | TPO, mod-bit | MODELLED+SPLICED | Degreasing method (§5 #4); fan sizes; shared curb numbers (§5 #5) |
| Parapet / coping (`coping`) — big-box east run only | W-1-TYP | TPO, mod-bit, gravel BUR, concrete | MODELLED+SPLICED | Joint gap, fastener spacing, whole-coping primer (§5 #3) |
| Solar Post supports (toggle, not in `DETAILS`) | P-1-S-TYP, P-2-S-TYP, P-3-S-TYP | All | CODE-DRAWN | Geometry, no 3D render |

**Totals:** 17 MODELLED+SPLICED · 0 MODELLED · 11 CODE-DRAWN · 0 NOT STARTED.

---

## 2. Product features

**Built** — what `index.html` already does, each row checked against the code (2026-09-14).

| # | Feature | Status | Notes |
|---|---|---|---|
| B1 | Configurator | BUILT | 11 building types and 7 roof types (`BUILDINGS`, `ROOFS`). Each building offers only its own 1–4 roof types (silo: concrete only), so not every pairing exists. The detail checklist is set by the building (`BUILDINGS[].details`), not by roof type; the roof type swaps a detail's name and drawing through `byRoof` (e.g. vent → bin vent CS-12-CON on concrete) |
| B2 | Six-stage walkthrough | BUILT | Existing → Prep → Primer → RMI-Flex → RMI-Thane → Finished on every roof, with play, step and per-stage text. The stage timeline drives the layers: its progress shows each model's `existing` / `primer` / `flex` / `topcoat` collections and sweeps the clipped overlays across code-drawn roofs. The Finish toggle (RMI-Thane / RMI-White Plus) recolours the topcoat, swaps the system code, and renames stage 5 with its text and plate rates; the Finished text follows it (gravel BUR is Thane-only). Gravel removal is not a separate stage — it sweeps off during Prep on gravel BUR. No ballast removal in the code |
| B3 | Macro roof with click-to-zoom hotspots | BUILT | Whole-roof view with a marker per switched-on detail, labelled with its drawing number; click flies the camera to the detail, "Back to roof" returns. Photo pins (#1) use the same jump |
| B4 | Section-view toggle | BUILT | Detail view only: a cut plane through the detail, facing the camera, so the section follows the orbit |
| B5 | Material quantity estimate | BUILT | Gallons of primer, Flex and topcoat plus the system code, from the spec-plate rates in `ROOFS`. Metal takes off laps, end laps and fasteners; flat roofs full field +6% (ASSUMED); per-detail allowances ASSUMED; silo walls add their area. No pricing |
| B6 | glTF detail models (`mountModel`) | BUILT | Loads the `MODELS` `.glb` files, keeps only `<layer>__` meshes, scales metres to feet, skins parts to the roof's materials, and hides the code-drawn stand-in once loaded (kept if the load fails). Field cutouts (`applyCutouts`) open the membrane and coating sheets around flat-roof models; splices set 4-ft sections into parapet runs (coping, scupper), walls (W-11 reglet, W-13 penthouse), the office edge-metal run (F-1) and metal slopes (side lap, standing seam), plus the ridge cap |
| B7 | Environment map and bump textures | BUILT | Procedural, no image files: a gradient cube map as `scene.environment` for metal and Thane reflections; canvas-noise bump maps on mod-bit granules, SPF foam, concrete and felts. Image textures are still #4 |
| B8 | Solar Post visual toggle (`S.solar`) | BUILT | "Add Solar Post supports" under Finish shows code-drawn posts on all 11 buildings, adds an ASSUMED Flex allowance to the estimate and sets `solar_post: true` in `configuration()`. Geometry status in §1 |
| B9 | Lead-capture email modal | REMOVED 2026-09-14 | Obsolete under the desktop direction; it never sent anything. Button, modal, Copy/Close handlers and `__rmi.payload()` removed. The serialiser is kept as `configuration()` (`__rmi.configuration()`): building, roof and plate, system code, existing condition, checked details with drawing numbers, topcoat, sq ft, gallon estimate, photo file names and pins. No pricing. Needed by #9 and #11. The internal keys sit beside the labels so #11 can restore a prospect: `building_key`, `roof_key`, `topcoat_key`, and `detail_ids` (`{id, name}` per checked detail, same order as `details`). Both lists hold only the `DETAILS` checklist; the Solar Post toggle is its own field, `solar_post: true/false` |

**Numbered** — done items first, then the order of CLAUDE.md "What's left". Numbers are fixed: §3 and the update log cite them.

| # | Feature | Status | Notes |
|---|---|---|---|
| 0 | Desktop installer (Electron, Windows) | BUILT (v0.1.2) | `npm run dist` → `dist/RMI Roof Visualizer Setup 0.1.2.exe`; runs offline, vendored libs. Window title shows the version from package.json at runtime (`app.getVersion()`), e.g. "RMI Roof Visualizer 0.1.2". Mac only if needed. Rollout to reps not yet recorded |
| 1 | Photo panel | DONE (v1) | Photos from disk, pins that jump to details, native "Add photos" dialog in Electron. In memory only; saving comes with #11 |
| 2 | Remaining detail models | IN PROGRESS | 11 CODE-DRAWN rows in §1, in the order the buildings need them |
| 3 | Fine-tuning | OPEN | Labels, camera pass, silo headhouse/shed (fastener size done 2026-09-14) |
| 4 | Textures | NOT STARTED | `textures/` folder (planned layout) |
| 5 | Catalog alignment with the 25 `DETAILS` entries | OPEN | Catalog rows ↔ the 25 `DETAILS` entries. The detail menu is a per-building checkbox list, not a dropdown (B1) |
| 6 | ASSUMED questions to RMI | OPEN | [Catalog §5](RMI_Library_Catalog.md#5-open-questions-for-rmi); each answer moves an item to VERIFIED |
| 7 | Repo private, Pages off, transfer to an RMI-owned GitHub organization | NOT STARTED | One step, so RMI controls collaborator access. Until then the repo stays under nihthauke for team review. Blocks #8 |
| 8 | Drawing panel | NOT STARTED | Can't start until #7 is done. 2D drawing (zoomable), plain-language steps (ASSUMED steps say so), 3D concept tab. Images rendered at build time from `drawings/` (git-ignored) |
| 9 | PDF export | NOT STARTED | Electron `printToPDF` + canvas captures; cover, config, six stages, one page per detail, estimate (no pricing), photos, ASSUMED notes, Project Evaluation appendix; per-section toggles |
| 10 | EagleView import | NOT STARTED | Parse report XML → facets, parapet/eave/flashing lines, penetrations classified by area for the rep to confirm; estimate from measured totals. Report files never committed |
| 11 | Saved prospects | NOT STARTED | Config + photos + report + confirmations as one local file per prospect under `prospects/` (git-ignored); location TBD |
| 12 | Bundled drawings, code signing, wide rollout | NOT STARTED | |
| 13 | Project Evaluation pre-fill | NOT STARTED | No summary view fills RMI's Project Evaluation form. The two-field `project_evaluation_prefill` stub (existing roof system, checked details) went out with B9; `configuration()` carries both. Feeds the #9 appendix; numbered 13 so #0–#12 keep their cross-references |

---

## 3. Fine-tuning & housekeeping

- [x] Add `drawings/` and `prospects/` to `.gitignore` before any drawing or prospect record is copied in (nothing tracked under either)
- [ ] Decide where saved prospects live: rep laptop or shared folder
- [ ] Keep a sample EagleView report outside the repo for testing EagleView import (§2 #10)
- [ ] Mac installer, only if needed
- [ ] Split `index.html` into `src/` JS modules (planned layout; `models/`, `scripts/`, `docs/` exist; textures are §2 #4)
- [x] Refresh CLAUDE.md "Current state" to match §1 and §2
- [ ] Extend spliced models to the instances still code-drawn: RTU curbs at other sizes (school, office, hotel, restaurant); coping on hospital, restaurant, hotel; ridge cap on manufacturing, airport, arena (confirm pitch vs. the 1:12 model)
- [ ] Next curb model: CS-15-MP fixed metal curb for the arena hatch (§5 #14)
- [ ] Ask RMI whether reps see ballasted single-ply roofs (Plate SPB) — candidate 8th roof type; ballast removal is not built

---

## 4. Update log

Newest first, one line each.

- 2026-09-14 — Perimeter edge metal F-1-TYP modelled and spliced into the office east edge at the hotspot (`perimeter-edge-metal-F-1-TYP.glb`). Every office edge now draws the same cross-section in code (`EM`, mitred at the corners) in place of the old box flange, and on a metal-edged block the field sheets run out to the wall face. Built to the drawing: flange flat on the roof (no raised stop, which is F-2-TYP), stripped in, fascia hooked over a continuous cleat. Now VERIFIED (was "no VERIFIED tag"): the stripping over the flange stepping down onto the field; confirm seam and flashing integrity; the cleat; Flex over the stripped flange and the field; topcoat to all surface areas. ASSUMED, not on the drawing: the tape over the metal-to-membrane joint, Flex down the fascia face, exposed face fasteners and their encapsulation, and every size (was "flange width"), §5 #22. Detail camera brought in from 14 to 3.5 ft. The penthouse prism helpers are now shared (`prismRun`, `rectYZ`, `sheetYZ`); `prismRun` can leave a run end open where it meets a spliced model
- 2026-09-14 — Desktop app 0.1.2 (package.json, package-lock.json, CLAUDE.md installer line). Installer rebuilt as `dist/RMI Roof Visualizer Setup 0.1.2.exe`, the first with the version in the window title. Packaged app opened from `dist/win-unpacked`: title "RMI Roof Visualizer 0.1.2", left panel ends at "Open photo panel"
- 2026-09-14 — Electron window title now shows the app version, read from package.json at runtime (`app.getVersion()` in electron/main.js, no hard-coded number): "RMI Roof Visualizer 0.1.1" confirmed with `npm start`. The 0.1.1 installer already in dist/ was built before this change; the next `npm run dist` includes it
- 2026-09-14 — Desktop app 0.1.1 (package.json, package-lock.json; the version is not shown anywhere in the UI). Installer rebuilt as `dist/RMI Roof Visualizer Setup 0.1.1.exe`, the first build without the B9 email modal. Opened with `npm start` and from `dist/win-unpacked`: the left panel ends at "Open photo panel", no email button. CLAUDE.md installer line bumped
- 2026-09-14 — `configuration()`: Solar Post taken out of `details` and `detail_ids` (now the checklist only) and returned as its own field `solar_post: true/false`; field check run with it on and off. B8 note and the catalog's Solar Post line updated to match
- 2026-09-14 — `configuration()` now returns internal keys beside its labels: `building_key`, `roof_key`, `topcoat_key`, `detail_ids` (`{id, name}` per checked detail; Solar Post as `solar`). Existing fields unchanged; a photo-panel snapshot still returns the pins
- 2026-09-14 — B9 lead-capture email modal REMOVED: button, modal HTML/CSS, Copy/Close handlers and `__rmi.payload()`. The serialiser is kept as `configuration()` / `__rmi.configuration()`, minus the website-only fields (`source`, empty `contact`, `project_evaluation_prefill` stub). snapshot.py reads it instead of opening the modal. The photo panel note no longer mentions an email. Catalog lines about the emailed configuration reworded. CLAUDE.md modal sentence deleted
- 2026-09-14 — CLAUDE.md: "fastener size" off What's left item 2 (done); public-repo rule now also bars prospect addresses and EagleView report numbers, including from this tracker and the catalog; new hard rule: "Hotel / senior living" is the market label and condominiums are never named in UI text
- 2026-09-14 — Topcoat labels: stage 5 and the stage text follow the Finish toggle (RMI-White Plus name, text and Plate rates WP23 1.5 / WP30 2 gal/sq on every roof but gravel BUR); ridge cap source no longer hard-codes Thane. CLAUDE.md synced to the code: gravel removal runs inside Prep and there is no ballast stage (SPB question added to §3); Project Evaluation pre-fill is #13 NOT STARTED; the detail menu is a per-building checkbox list (#5 reworded)
- 2026-09-14 — §2: "Built" table (B1–B9) added above the numbered features, each row checked against index.html; #0–#12 unchanged. Found in the code: the detail checklist is set by building, not roof type; gravel removal runs inside Prep and there is no ballast removal; the Project Evaluation pre-fill is only a stub in the email payload (added as #13 NOT STARTED); the lead-capture email modal is still wired (B9, obsolete, pending removal)
- 2026-09-14 — Penthouse wall W-13-TYP modelled and spliced on the office penthouse west face at the hotspot (`wall-counterflashing-fixed-W-13-TYP.glb`). Every penthouse now draws the same cross-section in code, mitred at the corners. Now VERIFIED: the counterflashing is fixed and never removed (note 7); sealant bead at its top edge; Flex encapsulates the (E) flashing up to the counterflashing (was "Flex height ASSUMED", off §5 #15); topcoat over the Flex; 24 ga. skirt min 4" over the RMI system. No term bar on the drawing. Sizes, skirt timing and the optional coated counterflashing are ASSUMED (§5 #21). Detail camera unchanged — at distance 20 the section reads small
- 2026-09-14 — Pipe clusters P-8-TYP modelled and spliced on all three hospital pans (`chem-curb-P-8-TYP.glb`). Built to the drawing, not the old code geometry: a Chem-Curb set in M-1 sealant (no metal flange), the pocket filled with Flex tapered outward (not pourable sealer), Flex min 4" and topcoat min 2" up the penetrations — now VERIFIED; sizes, fill crown, field extent and curb-before-primer ASSUMED (§5 #20). One hospital pan moved off the penthouse wall line; detail camera brought in
- 2026-09-14 — Sleeper support CS-8-TYP modelled and spliced (office hotspot sleeper, both sleepers under the hotel hotspot condenser). Per the drawing the coats run continuous under the raised sleeper and the walkpad goes down after cure — no Flex wrap (was ASSUMED in the code geometry; now VERIFIED, dropped from §5 #15). Code-drawn sleepers resized to match; condenser sleepers now parallel; field cutouts accept rectangles
- 2026-09-14 — Code-drawn purlin fasteners on R-panel and standing seam cut from ~3" discs to true scale (~5/8" head, ~1.5" Flex dab, sizes ASSUMED) to match the F-8-TYP model washers at detail cameras; rust patches and lap strips unchanged, whole-roof view still reads as metal
- 2026-09-12 — CLAUDE.md direction: Pages goes off at What's left step 6 (repo private) before any RMI drawing is committed, not when the first installer ships; the installer replaces the review link for reps
- 2026-09-12 — Repo private, Pages off and transfer to an RMI org folded into one step (§2 #7) just before the drawing panel, which it blocks; #12 is now bundled drawings, code signing, wide rollout
- 2026-09-12 — Webflow re-test dropped (desktop program, nothing hosted on roofrmi.com); repo transfer reworded to an RMI-owned GitHub org at the same time as going private; stale #4 reference fixed
- 2026-09-12 — CLAUDE.md Blender conventions: rebuild order now points to the §1 details table (curb variants share the CS-1 pattern; gutter pairs with inlet)
- 2026-09-12 — `drawings/` and `prospects/` git-ignored (nothing was tracked); CLAUDE.md "Current state" synced to this tracker and a "What's left" order added; §2 features table reordered to match it
- 2026-09-12 — Tracker created: 28 details (13 MODELLED+SPLICED, 15 CODE-DRAWN) checked against index.html; features and housekeeping seeded from CLAUDE.md
