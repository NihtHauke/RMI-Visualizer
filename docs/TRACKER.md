# RMI Roof Visualizer — Project Tracker

Tracker updated: Fri 18 Sept 2026

The single status page. Per-drawing ASSUMED questions live in the catalog, not here:
[RMI_Library_Catalog.md](RMI_Library_Catalog.md) — §3c is the per-detail sync table, [§5](RMI_Library_Catalog.md#5-open-questions-for-rmi)
is the numbered list of open questions for RMI (cited below as §5 #n).

Rule: every task updates the rows it touched (§1–§3) in the same commit as the work, so the tables stay accurate.
No per-task log lines: §4 is a weekly update, written on Fridays.

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
| HVAC curb on metal (`curb`) | CS-13-MP · SPF → SPF-13-TYP | R-panel, standing seam, SPF | CODE-DRAWN | Curb sizes; SPF wrap height (§5 #15) |
| R-panel side lap (`lap`) — warehouse slope | F-8-TYP | R-panel | MODELLED+SPLICED | Rib, lap lips, fastener spacing, Flex extent past the rib (§5 #10) |
| Standing seam (`sseam`) — manufacturing slope | F-9-TYP, F-20-TYP | Standing seam | MODELLED+SPLICED | Seam silhouette, clip spacing, Flex extent (§5 #11) |
| Skylight panels, flush (`mskylight`) | F-12-TYP · SPF → none | R-panel, standing seam, SPF | CODE-DRAWN | Geometry (no 3D render); SPF treated as a curb (§5 #13) |
| Vents on metal / SPF (`vent`) | Plate D · SPF → SPF-16-TYP · membrane (EagleView prospect) → CS-1-TYP note 7 | R-panel, standing seam, SPF | CODE-DRAWN | Whole metal assembly, no drawing (§5 #12); SPF wrap height (§5 #15) |
| Bin vent (`vent` on concrete) — silo cap | CS-12-CON; CS-1-TYP note 7 | Concrete | MODELLED+SPLICED | Shared curb numbers (§5 #5); concrete skinning of the curb |
| Pipes on metal (`mpipe`) | P-9-MP (P-10-MP alt.) · SPF → SPF-4-TYP | R-panel, standing seam, SPF | CODE-DRAWN | SPF wrap is on the sheet (Flex 1" above the collar flashing); code geometry not yet checked against it (§5 #15) |
| Gutters (`gutter`) | W-7-TYP (gutter-seams sheet; the concrete-wall sheet carries the same number, so the panel renders this one as `W-7-TYP-GUTTER`) | Standing seam, R-panel, SPF | CODE-DRAWN | None flagged yet — sizes will be ASSUMED when modelled |
| Downspout inlets (`gutterinlet`) | D-8-TYP | Standing seam, R-panel, SPF | CODE-DRAWN | None flagged yet — sizes will be ASSUMED when modelled |
| Roof hatch on metal / SPF (`hatch`) — arena | CS-15-MP · SPF → SPF-13-TYP · membrane (EagleView prospect) → CS-1-TYP note 7 | Standing seam, R-panel, SPF | CODE-DRAWN | CS-15-MP is a different assembly, next curb model (§5 #14); SPF wrap (§5 #15) |
| Manway / bin hatch (`hatch` on concrete) — silo cap | CS-14-CON; CS-1-TYP note 7 | Concrete | MODELLED+SPLICED | Lid size, open angle, hinge; concrete skinning; shared curb numbers (§5 #5) |
| Ridge cap (`ridge`) — warehouse only | F-21-M-TYP · SPF → SPF-3-TYP | R-panel, standing seam, SPF | MODELLED+SPLICED | Cap lap, closure position (§5 #16); model built for a 1:12 gable |
| HVAC curbs / RTU (`rtu`) — 8 × 1.5 ft curbs: big-box, hospital wing | CS-1-TYP | TPO, mod-bit, gravel BUR, concrete | MODELLED+SPLICED | Curb and unit sizes, nailer, skirt, Flex apron and turn-down (§5 #5) |
| Drains (`drain`) — all seven flat buildings | D-1-TYP, D-2-TYP | TPO, mod-bit, gravel BUR, concrete | MODELLED+SPLICED | Bowl, clamping-ring and dish sizes |
| Scuppers (`scupper`) — big-box north parapet | D-4-TYP | TPO, mod-bit, gravel BUR | MODELLED+SPLICED | Tube size, exterior termination, 12" measured from where (§5 #8); cant and flashing height (§5 #7) |
| Wall tie-in, reglet (`wall`) — school gym wall | W-11-TYP | Mod-bit, TPO | MODELLED+SPLICED | Flashing height, reglet, counterflashing lap (§5 #6) |
| Soil stacks (`pipe`) — all five buildings | P-6-TYP | TPO, mod-bit, gravel BUR, concrete | MODELLED+SPLICED | Every dimension (§5 #9) |
| Skylights, curb-mounted (`skylight`) — school | CS-1-TYP note 7 | Mod-bit, TPO | MODELLED+SPLICED | Dome rise, retainer frame, condensation gutter; shared curb numbers (§5 #5) |
| Edge metal (`edge`) — office east edge at the hotspot; every office edge draws the same cross-section in code | F-1-TYP | TPO, concrete, mod-bit | MODELLED+SPLICED | Flex and topcoat down the fascia (the 2D drawing ends them at the roof edge); flange, fascia, stripping and cleat sizes (§5 #22) |
| Penthouse walls (`penthouse`) — office penthouse west face | W-13-TYP | TPO, mod-bit, gravel BUR, concrete | MODELLED+SPLICED | Counterflashing height, depth and stand-off; cant; skirt size and lap; fastener spacing; skirt fitted after the topcoat (§5 #21) |
| Sleeper supports (`sleeper`) — office hotspot sleeper, hotel hotspot condenser | CS-8-TYP | TPO, mod-bit, concrete | MODELLED+SPLICED | Every dimension (NTS): sleeper, pad, 6" raise, patch; whether the (E) condition has a pad |
| Pipe clusters / Chem-Curb (`pitchpan`) — all three hospital pans | P-8-TYP | Gravel BUR, mod-bit, TPO, concrete | MODELLED+SPLICED | Every dimension (NTS): curb, penetrations, fill crown, Flex field extent; curb set before or after priming (§5 #20) |
| Expansion joint (`ej`) — hospital: a 4-ft section at the hotspot; the rest of the run draws the same section in code | A-3-TYP | Gravel BUR, mod-bit, TPO, concrete | MODELLED+SPLICED | Curb mounting (the drawing lays the flanges on the roof); joint, curb, flange, bellow and fastener sizes; coats down the curbs; no 3D render (§5 #16, #23) |
| Silo walls (`silowall`) | W-7-TYP | Concrete | CODE-DRAWN | Sequence and coverage on a curved wall (§5 #17) |
| Gallery supports (`support`) — silo: the hotspot post; the other five draw the same wrap in code | P-5-C, P-7-C | Concrete | MODELLED+SPLICED | Post, gap, bead, backer-rod and old-mastic sizes (§5 #24); the wrap extents are from the sheet |
| Kitchen exhaust (`exhaust`) — restaurant | CS-1-TYP note 7 | TPO, mod-bit | MODELLED+SPLICED | Degreasing method (§5 #4); fan sizes; shared curb numbers (§5 #5) |
| Parapet / coping (`coping`) — big-box east run only | W-1-TYP | TPO, mod-bit, gravel BUR, concrete | MODELLED+SPLICED | Joint gap, fastener spacing, whole-coping primer (§5 #3) |
| Solar Post supports (toggle, not in `DETAILS`) | P-1-S-TYP, P-2-S-TYP, P-3-S-TYP | All | CODE-DRAWN | Geometry, no 3D render |

**Totals:** 19 MODELLED+SPLICED · 0 MODELLED · 9 CODE-DRAWN · 0 NOT STARTED.

---

## 2. Product features

**Built** — what `index.html` already does, each row checked against the code (2026-09-14; rechecked 2026-09-18).

| # | Feature | Status | Notes |
|---|---|---|---|
| B1 | Configurator | BUILT | 11 building types and 7 roof types (`BUILDINGS`, `ROOFS`). Each building offers only its own 1–4 roof types (silo: concrete only), so not every pairing exists. The detail checklist is set by the building (`BUILDINGS[].details`), not by roof type; the roof type swaps a detail's name and drawing through `byRoof` (e.g. vent → bin vent CS-12-CON on concrete) |
| B2 | Six-stage walkthrough | BUILT | Existing → Prep → Primer → RMI-Flex → RMI-Thane → Finished on every roof, with play, step and per-stage text. The stage timeline drives the layers: its progress shows each model's `existing` / `primer` / `flex` / `topcoat` collections and sweeps the clipped overlays across code-drawn roofs. The Finish toggle (RMI-Thane / RMI-White Plus) recolours the topcoat, swaps the system code, and renames stage 5 with its text and plate rates; the Finished text follows it (gravel BUR is Thane-only). Gravel removal is not a separate stage — it sweeps off during Prep on gravel BUR. No ballast removal in the code |
| B3 | Macro roof with click-to-zoom hotspots | BUILT | Whole-roof view with a marker per switched-on detail, labelled with its drawing number; click flies the camera to the detail, "Back to roof" returns. Photo pins (#1) use the same jump |
| B4 | Section-view toggle | BUILT | Detail view only: a cut plane through the detail, facing the camera, so the section follows the orbit |
| B5 | Material quantity estimate | BUILT | Gallons of primer, Flex and topcoat plus the system code, from the spec-plate rates in `ROOFS`. Metal takes off laps, end laps and fasteners; flat roofs full field +6% (ASSUMED); per-detail allowances ASSUMED; silo walls add their area. No pricing |
| B6 | glTF detail models (`mountModel`) | BUILT | Loads the `MODELS` `.glb` files, keeps only `<layer>__` meshes, scales metres to feet, skins parts to the roof's materials, and hides the code-drawn stand-in once loaded (kept if the load fails). Field cutouts (`applyCutouts`) open the membrane and coating sheets around flat-roof models; splices set 4-ft sections into parapet runs (coping, scupper), walls (W-11 reglet, W-13 penthouse), the office edge-metal run (F-1) and metal slopes (side lap, standing seam), plus the ridge cap; the hospital expansion-joint run (A-3) takes a 4-ft section that also opens a field cutout. A cutout can keep the gravel sheet whole over its model (`keepGravel`) and open the primer sheet wider than the Flex sheet (`primerGrow`) for a low detail camera |
| B7 | Environment map and bump textures | BUILT | Procedural, no image files: a gradient cube map as `scene.environment` for metal and Thane reflections; canvas-noise bump maps on mod-bit granules, SPF foam, concrete and felts. Image textures are still #4 |
| B8 | Solar Post visual toggle (`S.solar`) | BUILT | "Add Solar Post supports" under Finish shows code-drawn posts on all 11 buildings, adds an ASSUMED Flex allowance to the estimate and sets `solar_post: true` in `configuration()`. Geometry status in §1 |
| B9 | Lead-capture email modal | REMOVED 2026-09-14 | Obsolete under the desktop direction; it never sent anything. Button, modal, Copy/Close handlers and `__rmi.payload()` removed. The serialiser is kept as `configuration()` (`__rmi.configuration()`): building, roof and plate, system code, existing condition, checked details with drawing numbers, topcoat, sq ft, gallon estimate, photo file names and pins. No pricing. Needed by #9 and #11. The internal keys sit beside the labels so #11 can restore a prospect: `building_key`, `roof_key`, `topcoat_key`, and `detail_ids` (`{id, name}` per checked detail, same order as `details`). Both lists hold only the `DETAILS` checklist; the Solar Post toggle is its own field, `solar_post: true/false` |

**Numbered** — done items first, then the order of CLAUDE.md "What's left". Numbers are fixed: §3 and the weekly update cite them.

| # | Feature | Status | Notes |
|---|---|---|---|
| 0 | Desktop installer (Electron, Windows) | BUILT (v0.3.0) | `npm run dist` → `dist/RMI Roof Visualizer Setup 0.3.0.exe`; RMI crest as the app/taskbar icon (`build/icon.ico`, `build/icon.png`) and the RMI logo (`assets/rmi-logo.png`) in the header, on the PDF cover and in the PDF page header; runs offline, vendored libs; bundles `drawings/` (render it first) and `samples/` (the four sample roof photos, 2026-09-17). `RMI_SELFTEST=<png>` opens the big-box drain with the Drawing panel, prints its state and saves a screenshot; `RMI_SELFTEST_PDF=<pdf>` exports the big-box presentation with the sample photos to that path; `RMI_SELFTEST_PROSPECT=<folder>` runs the saved-prospect round trip in two launches (#11) (the build checks). Window title shows the version from package.json at runtime (`app.getVersion()`), e.g. "RMI Roof Visualizer 0.3.0". **v0.3.1 packages but the installer `.exe` cannot be produced on this machine:** Smart App Control blocks the unsigned NSIS uninstaller stub electron-builder has to run mid-build (`spawn UNKNOWN`; CodeIntegrity event 3077) — `dist/win-unpacked` builds and passes the checks, only the NSIS step fails (#12). Mac only if needed. Rollout to reps not yet recorded |
| 1 | Photo panel | DONE (v2, 2026-09-14) | v2 per Dennis: a thumbnail strip across the top of the 3D view (56 px, 4:3, pin-count badge, × to remove, "+" tile, drag-drop, "Clear photos", the orbit hint at its right end); click a thumbnail and the slider docks on the right at about 40 % (filename, i / n, prev/next, ← → keys, Esc). Pins unchanged from v1. Photos (blob), pins and the building/roof selection persist in IndexedDB on that machine (`rmi-visualizer` db); "Clear photos" wipes the photo store; nothing is uploaded. "Load sample photos" on the empty strip loads `samples/sample-01…04.jpg`, labelled "Sample roof"; a rep's own photos replace them. In the installed app they come through the desktop bridge (`rmiDesktop.samplePhotos` → main reads them out of the bundled `samples/`), because `fetch()` cannot read a file inside `app.asar` — it silently loaded nothing before (fixed 2026-09-17, `RMI_SELFTEST_PDF` now exports the photo pages from the packaged app); the browser build still fetches them. Native "Add photos" dialog in Electron kept. A saved prospect (#11) carries the photos and pins in its own file |
| 2 | Remaining detail models | IN PROGRESS | 9 CODE-DRAWN rows in §1, in the order the buildings need them |
| 3 | Fine-tuning | OPEN | Labels, camera pass, silo headhouse/shed (fastener size done 2026-09-14) |
| 4 | Textures | NOT STARTED | `textures/` folder (planned layout) |
| 5 | Catalog alignment with the 25 `DETAILS` entries | OPEN | Catalog rows ↔ the 25 `DETAILS` entries. The detail menu is a per-building checkbox list, not a dropdown (B1) |
| 6 | ASSUMED questions to RMI | OPEN | [Catalog §5](RMI_Library_Catalog.md#5-open-questions-for-rmi); each answer moves an item to VERIFIED |
| 7 | Repo private, Pages off, transfer to an RMI-owned GitHub organization | NOT STARTED | One step, so RMI controls collaborator access. Until then the repo stays under nihthauke for team review. Blocks committing `drawings/` (#8 reads it git-ignored) |
| 8 | Drawing panel | BUILT (2026-09-15) | "Drawing" button beside "Section view" in detail view docks a panel right of the 3D view (the view shrinks, the detail stays centred; with the photo slider open too the columns are 5 / 3.2 / 2.8, usable at 1366×768). Tabs: **2D drawing** (scroll-zoom, drag-pan, double-click 1:1, Fit), **How it's applied** (numbered steps per detail from the sheet notes — `STEPS` in index.html, ASSUMED rendered as a tag, byRoof variants carry their own), **3D concept** (where the library has one). Header shows the sheet number, title and issue/revision date from the sheet (`drawings/index.js`). Sheets are PNGs rendered at 150 dpi by `scripts/render_drawings.py` from the local library — 52 today, every referenced number found — into `drawings/`, git-ignored and bundled only by the installer; a missing sheet shows "not bundled with this build" instead of breaking. Sheet-number fixes found on the way: the SPF variants pointed one sheet off (now SPF-13 curb/hatch, SPF-4 penetration, SPF-3 ridge); the library has two different sheets numbered W-7-TYP |
| 9 | PDF export | BUILT (2026-09-15) | "Export PDF" in the header opens a dialog: prospect name and address, rep name, notes, and a checkbox per section (cover; building and roof configuration with a labelled whole-roof image; the six stages as captured images with the stage text; one page per selected detail — 3D view at the finished stage, existing / primer / Flex thumbnails, layer legend, "How it's applied" steps with ASSUMED tagged, then the 2D sheet on its own page where bundled; material estimate with coverage rates and per-detail allowances, no pricing; prospect photos with their pins drawn and listed; notes and every ASSUMED item; the Project Evaluation pre-fill as an appendix). Images come from the canvas at the default cameras (whole roof at each stage, details at four stages), composited on the view background. Desktop: Electron `printToPDF` (Letter, CSS page margins, running footer with page numbers) through `rmiDesktop.exportPdf`, save dialog defaulting to Documents and `<prospect>-<date>.pdf`, an Open button after; browser: the print dialog ("Save as PDF"). Big-box with four photos: 18–19 pages, ~3 MB. Verified from the installed 0.1.4 app |
| 10 | EagleView import | BUILT (2026-09-15) | "Import EagleView report" in the header (native dialog in the app, file input in a browser) reads the report XML from the rep's machine and adds "Prospect roof (report N)" to the building menu. Each ROOF facet becomes a polygon block at its measured elevation (main roof, penthouses, stair towers, canopies); PARAPET edges get the parapet + coping (W-1-TYP), EAVE edges edge metal (F-1-TYP), FLASHING edges the wall tie-in (W-11-TYP), a PARAPET edge against a higher facet the penthouse wall (W-13-TYP); every penetration sits at its polygon centroid with its footprint, typed by area as a best guess (under 1 sq ft soil stack; 1–4 small curb; 4–10 curb / hatch; 10–30 RTU / skylight; over 30 large equipment on a curb at its measured size) using the existing models. A "Penetrations" panel beside the roof lists each one by report number with a type dropdown and a confirm box; unconfirmed types stay ASSUMED and the roof is labelled "From EagleView report N, file dated D — penetration types confirmed by rep: n of m". The rep picks the roof type (flat plates: TPO, mod-bit, gravel, concrete, SPF). The estimate uses the report's measured totals — roof area less penetrations, parapet length × the parapet height the rep enters, penetration count and perimeter — instead of the square-footage field. Stages, hotspots (one per detail type present), photos, drawing panel and PDF (cover with report number and file date, penetration schedule, measured basis, ASSUMED notes) all work on it. The XML carries no report date (the file date is used) and no parapet height; a hatch or vent on a membrane roof takes CS-1-TYP note 7 (`FLAT_HATCH` / `FLAT_VENT` byRoof). Report files are client data: `*.xml` and `prospects/` are git-ignored; the sample report lives outside the repo. `snapshot.py --eagleview <xml>` and `RMI_SELFTEST_EV` are the checks |
| 11 | Saved prospects | BUILT (2026-09-16) | "Open prospect" and "Save prospect" in the header. One `.rmiproject` file per prospect, a zip written and read in the page (no library): `prospect.json` (format, version, id, saved date; prospect name, address, rep, notes; the restore keys — building, roof, finish, Solar Post, existing condition, sq ft, checked details, parapet height; the EagleView block — report id, file name and date, totals, every penetration's id, type, best guess and confirmation; each photo's file and pins; and the full `configuration()`), the original EagleView XML under `eagleview/` and the photos under `photos/`, byte for byte. No pricing. Save dialog: prospect, address, rep, notes (shared with the PDF dialog), a one-line summary of what is saved, and the folder. Desktop: written through `rmiDesktop.prospects` to a folder chosen once and remembered in the app's `settings.json` (default Documents\RMI Prospects, "Change folder…"); saving again updates the same file in place, and a name that belongs to another file gets " (2)" — nothing is overwritten. Browser: the file downloads. Open dialog: "Recent prospects" (desktop: files saved or opened on that machine that still exist; browser: copies in IndexedDB, last 8), × removes a row and leaves the file, Browse… for any file. Open checks the whole file first (zip, CRC, JSON, report parses) and changes nothing if it is damaged; then rebuilds the prospect roof from the embedded XML with the saved types and confirmations, the configuration, and the photos with their pins in one pass. Asks before replacing unsaved work; the header shows the prospect name. Checks: `scripts/check_prospect.py --eagleview <xml>` (browser: save, reopen from Recent and from Browse…, compare state, zip entries byte-identical) and `RMI_SELFTEST_PROSPECT` in the installed app. `*.rmiproject` is git-ignored; prospect files are client data |
| 12 | Bundled drawings, code signing, wide rollout | IN PROGRESS | Drawings already ship inside the installer from the local `drawings/` render (#8); left: code signing and the rollout to reps. **Code signing is now blocking, not just polish:** with Smart App Control on, Windows refuses to run the unsigned NSIS uninstaller stub during `npm run dist`, so no installer can be built on this machine until it is turned off (a one-way switch; re-enabling needs a Windows reinstall) or the build is signed — Heath's call |
| 13 | Project Evaluation pre-fill | BUILT as the #9 appendix (2026-09-15) | The PDF's last section mirrors RMI's Request for Project Evaluation (revised 11/15/13): project information (use, roof squares, RMI specification #, general overview written from the configuration), document profile (proprietary RMI products, warranty years from the system code), existing roof system (surface membrane, gutters / drains / skylights / mechanical / sheet metal from the checked details), the "Detail drawings — check all applicable" grid ticked from the details with their drawing numbers (`PE_ITEMS` in index.html), photo count, signature block. Unknown fields read "rep to complete". No standalone view or fillable form yet; numbered 13 so #0–#12 keep their cross-references |

---

## 3. Fine-tuning & housekeeping

- [x] Add `drawings/`, `prospects/` and `*.rmiproject` to `.gitignore` before any drawing or prospect record is copied in (nothing tracked under either)
- [ ] Before every `npm run dist`: `python scripts/render_drawings.py` (52 sheets, ~16 MB); `drawings/` stays uncommitted until §2 #7
- [ ] Check the SPF pipe wrap (SPF-4-TYP) code geometry against the dimensions the sheet gives (§5 #15); the P-5-C gallery-support wrap is drawn to its sheet
- [ ] Gravel BUR prep stage: white speckles on the felts round the hospital soil stacks, seen from the expansion-joint camera; in the build before the A-3-TYP model too, so not caused by it
- [ ] Decide where saved prospects live: rep laptop (the default, Documents\RMI Prospects) or a shared folder — "Change folder…" in the Save dialog sets either, per machine (§2 #11)
- [x] Keep a sample EagleView report outside the repo for testing EagleView import (§2 #10) — `../RMI-prospects/`, never copied in
- [ ] Decide how to get past Smart App Control for `npm run dist`: sign the build (§2 #12) or turn SAC off on the build machine
- [ ] Mac installer, only if needed
- [ ] Split `index.html` into `src/` JS modules (planned layout; `models/`, `scripts/`, `docs/` exist; textures are §2 #4)
- [x] Refresh CLAUDE.md "Current state" to match §1 and §2
- [ ] Extend spliced models to the instances still code-drawn: RTU curbs at other sizes (school, office, hotel, restaurant); coping on hospital, restaurant, hotel; ridge cap on manufacturing, airport, arena (confirm pitch vs. the 1:12 model)
- [ ] Next curb model: CS-15-MP fixed metal curb for the arena hatch (§5 #14)
- [ ] Ask RMI whether reps see ballasted single-ply roofs (Plate SPB) — candidate 8th roof type; ballast removal is not built
- Friday update (Heath): `git log --since="last friday"` → write the week's entry in §4 → update the title line → run contact sheets → `git push` → confirm Pages loads → tell Dennis the tracker is updated
- `samples/` photos — shared with client permission, EXIF stripped, no identifiers

---

## 4. Weekly update

Newest first, one entry per week, written on Fridays.

### 18 Sept 2026

Covers Fri 11 – Thu 17 Sept. Monday's work is already in the 14 Sept entry and gets one line here so the week reads whole.

- **Models: 9 this week, from 8 to 17 of 28 details modelled; 11 are still simple stand-in shapes.** Fri 11: roof hatch,
  curb-mounted skylight, kitchen exhaust fan and silo bin vent, all four on one shared curb (CS-1-TYP note 7), plus the metal
  ridge cap (F-21-M-TYP) on the warehouse. Mon 14 (see 14 Sept): sleeper supports (CS-8), pipe clusters on a Chem-Curb (P-8),
  penthouse walls (W-13), perimeter edge metal (F-1). Tue 15: edge metal rebuilt without tape or face fasteners to match its
  drawing; closer camera on the penthouse wall; seams and laps on flat roofs now stop short of every model.
- **App features:**
  - **Drawing panel** (Tue 15): a "Drawing" button in detail view shows RMI's 2D sheet (zoom and pan), "How it's applied" steps
    taken from the sheet notes with ASSUMED steps marked, and the 3D concept. 52 sheets, shipped only inside the installer.
  - **PDF export** (Tue 15): one click builds the presentation: cover, configuration, the six stages, a page per detail with its
    drawing, material estimate (no pricing), photos with pins and the ASSUMED notes. The Project Evaluation pre-fill is its
    appendix (#13). There is no standalone form yet.
  - **RMI logo** (Tue 15): app icon, header, PDF cover and PDF page header.
  - **EagleView import** (Tue 15): the rep opens a report file from their own computer and the tool builds that roof: roof areas at
    their heights, parapets, edges, wall tie-ins, and penetrations typed by size as a best guess the rep confirms. The estimate
    uses the report's measured totals.
  - **Saved prospects** (Wed 16): "Save prospect" / "Open prospect" keep one prospect's configuration, report, confirmed
    penetrations, photos and pins in a single file on the rep's computer, with a "Recent prospects" list.
  - **Sample photos** now load in the installed app, not only in the browser (Thu 17).
  - Mon 14 (see 14 Sept): photo panel v2, email form removed, topcoat choice carried through the stage text.
- **Installer and tooling:** Fri 11 brought a self-contained build and the desktop wrapper: three.js, the model loader, the photo
  converter and the fonts now live in the repo, so the app runs with no network. Installers 0.1.0 → 0.3.0 built (0.3.0 on
  Wed 16). 0.3.1 packages, but its installer file can't be produced on this machine because Windows Smart App Control blocks an
  unsigned step of the build (#12). New checks: the installed app can test itself (drawing panel, PDF export, EagleView import,
  save-and-reopen), browser checks cover the same, and a script renders the drawing sheets from the local library.
- **Docs:** this tracker created (Sat 12) and checked against the code. The catalog is now one row per detail, with every open
  question in one list (§5). CLAUDE.md kept in step. Rules added: making the repo private, turning the review link off and moving
  to an RMI-owned GitHub account happen as one step; RMI drawings are never committed while the repo is public; EagleView reports
  and saved prospects are client data and are never committed.
- **ASSUMED → VERIFIED this week** (full wording in each catalog §3c row and catalog §4):
  - Roof hatch, curb-mounted skylight, kitchen exhaust, bin vent: each is a curb-mounted unit on the RTU curb. Flex runs up the
    full curb and over the top, and the unit is lifted and reset. The hatch had been guessed as a fixed curb. Source: CS-1-TYP
    note 7 (for the bin vent on concrete, CS-12-CON).
  - Ridge cap: cap over the panel, metal closure set in sealant or tape, closure fasteners, Flex at the cap, Thane over all,
    closures recessed at least 6" under the cap. Source: F-21-M-TYP (note 12).
  - Sleeper supports: sleeper raised and reset, Flex and topcoat unbroken underneath (nothing wraps the block), walkpad after full
    cure. Source: CS-8-TYP.
  - Pipe clusters: Chem-Curb set in M-1 sealant, pocket filled with Flex tapered to shed water, Flex at least 4" and topcoat at
    least 2" up each penetration. Source: P-8-TYP.
  - Penthouse walls: counterflashing fixed and left in place, sealant bead at its top, Flex up to it, skirt metal at least 4" over
    the system. Source: W-13-TYP (note 7).
  - Edge metal: flange stripped in, Flex over the stripping and the field, topcoat over the Flex. No tape at the edge joint and no
    exposed face fasteners; the only fastener is the concealed cleat. Source: F-1-TYP, F1-34-FT-3D note 10.
  - Wrap extents read off the sheets. SPF pipe: Flex at least 1" above the collar flashing, topcoat 1" past it (SPF-4-TYP).
    Gallery support: tape 2" up and 4" out, Flex at least 6" past it, topcoat at least 2" past the Flex (P-5-C). The stand-in
    shapes haven't been checked against these yet (§3).
  - Sheet numbers corrected from the title blocks: SPF curb/hatch is SPF-13, SPF pipe SPF-4, SPF ridge SPF-3. The sleeper sheet is
    CS-8-TYP (two library file names are swapped). Two different sheets carry W-7-TYP (gutter seams, concrete wall).
- **Open questions for Dennis / RMI technical side:** [catalog §5](RMI_Library_Catalog.md#5-open-questions-for-rmi), 22 open.
  New this week: #20–22 (P-8, W-13 and F-1 sizes; #22 narrowed on 15 Sept once the drawing settled tape and fasteners). Also open
  (§3): do reps see ballasted single-ply roofs? For the team (§3): do saved prospects live on the laptop or in a shared folder?
- **Tracker check (18 Sept):** all 28 detail rows, B1–B9 and #0–#13 match the repo, and no status changed. Counts:
  17 MODELLED+SPLICED · 0 MODELLED · 11 CODE-DRAWN · 0 NOT STARTED.
- **Next** (CLAUDE.md "What's left" order): the remaining 11 details in the order the buildings need them, starting with the metal
  roof hatch curb (CS-15-MP, arena), then fine-tuning (labels, camera pass, silo headhouse/shed). Textures, catalog alignment
  and sending RMI the §5 questions come after, in that order. No new installer can be built until the code-signing / Smart App
  Control decision (#12).

### 14 Sept 2026

- **Four more details built from RMI drawings** and placed in the buildings: sleeper supports (CS-8), pipe clusters on a
  Chem-Curb (P-8), penthouse walls with fixed counterflashing (W-13) and perimeter edge metal (F-1). That makes 17 of 28 details
  modelled, up from 13; 11 are still simple stand-in shapes. Each one moved several points from ASSUMED to VERIFIED against its
  drawing; the sizes the drawings don't give are new questions for RMI (catalog §5 #20–22).
- **Photo panel v2:** prospect photos now sit in a strip across the top of the 3D view; click one and it opens large on the
  right, with arrows to step through. Pins on a photo still jump to the matching detail. Photos and pins stay on that computer
  after the app is closed, and nothing is uploaded. Four sample roof photos can be loaded for demos.
- **Desktop app 0.1.2:** installer rebuilt. The old website email form is gone, and the window title shows the version number.
- **Topcoat choice follows through:** picking RMI-White Plus now changes the stage name, the stage text and the coverage rates,
  not just the colour.
- **Smaller fixes:** metal roof fasteners drawn at true size; the configuration record behind the tool now carries everything
  PDF export and saved prospects will need to rebuild a presentation.
- **This tracker** was created and every "built" feature was checked against the app. That check found the Project Evaluation
  pre-fill isn't built yet; it is now on the list (#13).
- **Rules:** making the repo private, turning the review link off and moving the repo to an RMI-owned GitHub account happen
  together, just before the drawing panel. Webflow testing dropped (desktop app, nothing on roofrmi.com). The market is labelled
  "Hotel / senior living" and condominiums are never named. No prospect addresses or EagleView report numbers in the repo; the one
  exception is `samples/`, four client roof photos RMI may share, with location data stripped and signage blurred.
- **Process:** a short-lived "push on Fridays only" rule was reversed (14 Sept): work goes to the review link as it's done, and
  this tracker gets a weekly update every Friday.
- **Next:** the remaining 11 details in the order the buildings need them, starting with the metal roof hatch curb (CS-15-MP);
  then fine-tuning (labels, camera, silo) and sending RMI the open ASSUMED questions.
