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
| Edge metal (`edge`) | F-1-TYP | TPO, concrete, mod-bit | CODE-DRAWN | Flange width |
| Penthouse walls (`penthouse`) | W-13-TYP | TPO, mod-bit, gravel BUR, concrete | CODE-DRAWN | Flex height on the wall (§5 #15) |
| Sleeper supports (`sleeper`) | CS-8-TYP | TPO, mod-bit, concrete | CODE-DRAWN | Wrap height (§5 #15) |
| Pipe clusters / pitch pan (`pitchpan`) | P-8-TYP | Gravel BUR, mod-bit, TPO, concrete | CODE-DRAWN | Fill depth |
| Expansion joint (`ej`) | A-3-TYP | Gravel BUR, mod-bit, TPO, concrete | CODE-DRAWN | Geometry, no 3D render (§5 #16) |
| Silo walls (`silowall`) | W-7-TYP | Concrete | CODE-DRAWN | Sequence and coverage on a curved wall (§5 #17) |
| Gallery supports (`support`) | P-5-C, P-7-C | Concrete | CODE-DRAWN | Wrap height (§5 #15) |
| Kitchen exhaust (`exhaust`) — restaurant | CS-1-TYP note 7 | TPO, mod-bit | MODELLED+SPLICED | Degreasing method (§5 #4); fan sizes; shared curb numbers (§5 #5) |
| Parapet / coping (`coping`) — big-box east run only | W-1-TYP | TPO, mod-bit, gravel BUR, concrete | MODELLED+SPLICED | Joint gap, fastener spacing, whole-coping primer (§5 #3) |
| Solar Post supports (toggle, not in `DETAILS`) | P-1-S-TYP, P-2-S-TYP, P-3-S-TYP | All | CODE-DRAWN | Geometry, no 3D render |

**Totals:** 13 MODELLED+SPLICED · 0 MODELLED · 15 CODE-DRAWN · 0 NOT STARTED.

---

## 2. Product features

Done items first, then the order of CLAUDE.md "What's left".

| # | Feature | Status | Notes |
|---|---|---|---|
| 0 | Desktop installer (Electron, Windows) | BUILT | `npm run dist` → `dist/RMI Roof Visualizer Setup 0.1.0.exe`; runs offline, vendored libs. Mac only if needed. Rollout to reps not yet recorded |
| 1 | Photo panel | DONE (v1) | Photos from disk, pins that jump to details, native "Add photos" dialog in Electron. In memory only; saving comes with #11 |
| 2 | Remaining detail models | IN PROGRESS | 15 CODE-DRAWN rows in §1, in the order the buildings need them |
| 3 | Fine-tuning | OPEN | Labels, fastener size, camera pass, silo headhouse/shed |
| 4 | Textures | NOT STARTED | `textures/` folder (planned layout) |
| 5 | Catalog alignment and 25-item dropdown | OPEN | Catalog rows ↔ the 25 `DETAILS` entries |
| 6 | Transfer repo to an RMI-owned GitHub organization | OPEN | Do at the same time as going private, so RMI controls collaborator access. Until then the repo stays under nihthauke for team review |
| 7 | ASSUMED questions to RMI | OPEN | [Catalog §5](RMI_Library_Catalog.md#5-open-questions-for-rmi); each answer moves an item to VERIFIED |
| 8 | Drawing panel | NOT STARTED | 2D drawing (zoomable), plain-language steps (ASSUMED steps say so), 3D concept tab. Images rendered at build time from `drawings/` (git-ignored) |
| 9 | PDF export | NOT STARTED | Electron `printToPDF` + canvas captures; cover, config, six stages, one page per detail, estimate (no pricing), photos, ASSUMED notes, Project Evaluation appendix; per-section toggles |
| 10 | EagleView import | NOT STARTED | Parse report XML → facets, parapet/eave/flashing lines, penetrations classified by area for the rep to confirm; estimate from measured totals. Report files never committed |
| 11 | Saved prospects | NOT STARTED | Config + photos + report + confirmations as one local file per prospect under `prospects/` (git-ignored); location TBD |
| 12 | Bundled drawings, code signing, repo private, Pages off | NOT STARTED | Pages off once the first installer ships to reps |

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

---

## 4. Update log

Newest first, one line each.

- 2026-09-12 — Webflow re-test dropped (desktop program, nothing hosted on roofrmi.com); repo transfer reworded to an RMI-owned GitHub org at the same time as going private; stale #4 reference fixed
- 2026-09-12 — CLAUDE.md Blender conventions: rebuild order now points to the §1 details table (curb variants share the CS-1 pattern; gutter pairs with inlet)
- 2026-09-12 — `drawings/` and `prospects/` git-ignored (nothing was tracked); CLAUDE.md "Current state" synced to this tracker and a "What's left" order added; §2 features table reordered to match it
- 2026-09-12 — Tracker created: 28 details (13 MODELLED+SPLICED, 15 CODE-DRAWN) checked against index.html; features and housekeeping seeded from CLAUDE.md
