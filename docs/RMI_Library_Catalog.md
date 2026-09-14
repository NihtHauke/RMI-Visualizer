# RMI Master Library → Roof Visualizer Catalog

Source: `2024_Master_RMI_Library.zip` (296 files, read 2026-09-04). Status tags: **VERIFIED** = taken directly from an RMI document in the library. **ASSUMED** = my inference, correct me.
§3c is the per-detail sync table against the tool; §5 collects every open question in one place.

---

## 1. What's in the library and what each part feeds

| Folder | Files | What it is | Feeds |
|---|---|---|---|
| 2024 Specifications / Master Specification Plates | 17 | One plate per substrate: system codes, warranty tiers, primer/Flex/Thane rates, application notes | **MACRO table** (this is the field-application source I said we'd need — it already exists) |
| 2024 Specifications / Spec Guide Manual (US + Canada) | 2 | Full guide manual, ~1.7 MB each | Rates of application, prep, testing |
| 2024 Specifications / Data Sheets, Web Data Sheets | 7 | Product data: Flex, Thane, White Plus, below-grade, equivalencies | Product panel text, coverage math |
| 2024 Detail Drawings | 106 | 2D section drawings with notes — the "logic" for each detail. 9 categories: Penetrations (P), Drains (D), Curbs & Supports (CS), Walls (W), Field (F), Accessories/Ducts (A), SPF, Concrete repairs (CON), Solar (P-S) | **MICRO table** — governs how each detail is built |
| 2024 3D Details | 116 | 3D exploded concept renders of the same details, already color-coded Flex = gold, Thane = silver, with a "field" (FT) view for each family | **MICRO visuals** — these are near-direct references for the Three.js detail views |
| 3D Web System Comparisons | 8 | 2020 brochures per roof type (Metal, BUR, SPF, Single Ply, Concrete/LIC, BUR new construction, RV) + reference chart | Customer-facing copy per roof type; macro-view marketing text |
| 2024 Technical Bulletins | 10 | Bulletins 1001–1800 (granules, cold weather, etc.) | Edge cases; not needed for mockup |
| Roof Design Checklist | 1 | Sample project evaluation | Later: "email me my configuration" could mirror this |

Note: `2024PDF Concrete.zip` inside the Concrete folder is a duplicate of the five concrete PDFs beside it — safe to ignore.

---

## 2. MACRO table — field application per roof type (VERIFIED from spec plates)

Every RMI system reads the same way: **Prep → Primer → Flex → Topcoat (Thane or White Plus)**. The only thing that changes per roof type is *where* Flex goes and the mil thickness. Plate codes are RMI's own (e.g. `MP-10-33-FF-F16-T17` = Metal Panel, 10-yr, 33 finished mils, factory finish, Flex 16 mil field, Thane 17 mil).

| Roof type (plate) | Prep stage | Primer | Flex — where | Flex mils (10-yr / 15-yr) | Topcoat | Visualizer pattern | 3D concept ref |
|---|---|---|---|---|---|---|---|
| **Metal panels** — standing seam, R-panel, trapezoid, corrugated (MP) | Clean; treat rust; replace defective panels/fasteners | Yes — required under all Flex | **Seams, laps, fasteners, curbs, transitions, penetrations only.** Field Flex is *optional* (F16 variant) for pitted panels | FL48 flashings; F16 if field | Thane 17/22 or White 23/30 | **Seam-trace, then full-field spray** | B-1-F10-22-3D, B-1-F6-19-3D, B-2-F10-3D |
| **BUR / Mod-bit, smooth** (A-S) | Repair voids/splits; optional leveling coat; moisture scan | Yes | **Full field** + all flashings, laps, penetrations, curbs, drains | 48 | Thane 17/22 or White 23/30 | Full-field roll ×3 | B-1-F4-10-3D, B-1-F4-23-3D |
| **BUR / Mod-bit, granule** (A-G) | Same + fog coat to lock granules | Yes | Full field | 48 | Same | Full-field | B-1-F4-23-3D |
| **BUR, gravel** (MA-GR) | **Remove gravel to felts**; leveling coat | Yes | Full field, 64 mil | 64 | Thane 17 | Full-field (add gravel-removal stage) | F4-1C-3D |
| **Mod-bit new construction** (ANC) | New MB ply over insulation | — (MB is the base) | Full field | 48 | Thane/White up to 20-yr tier | Full-field | — |
| **Single-ply PVC/TPO/EPDM** (SP) | Repair seams/rips/tears; moisture scan | Yes | Full field + all seams, flashings | 48 | Thane 17/22 or White 23/30 | Full-field | F4-*-24-3D family |
| **Single-ply, ballasted** (SPB) | **Remove ballast**; repairs | Yes | Full field | 48 / 64 | Thane 17 (fog coat) | Full-field (add ballast-removal stage) | — |
| **SPF spray foam** (SPF) | Repair/scarf foam; min 3.0 lb density | Yes | Full field to encapsulate foam | 48 | Thane 17/22 or White 23/30 | Full-field | B-1-SPF-1-3D |
| **Concrete / LIC** (C) | Clean; bead-blast if needed; moisture test; cure new concrete | Yes | Full field + flashings | 48 | Thane 17/22 or White 23/30 | Full-field | B-1-C-LIC 1-3D |
| **Garden roof (concrete)** (GAC) | — | Yes | Full field 64/80 | 64 / 80 | Thane 28 | Full-field, heavy | — |
| **Pavers / decking** (PD) | Lift pavers; treat substrate per its own plate | Yes | Per substrate | per substrate | Thane | Substrate pattern + re-set pavers | — |
| **Metal ducts / vents / curbs** (D) | Clean galvanized (xylene) | Yes | All seams/laps; field optional | 48 | Thane 22 / White 30 | Detail-level only | — |
| **Hail-resistant / cold-climate** (HRS / CCS) | Any substrate | Yes | Full field, 64/80 | 64 / 80 | Thane 22–28 | Modifier on any roof type (thicker) | — |

**What this settles for the build:** there are exactly **two field patterns** (seam-trace vs. full-field) and **two pre-stages** that only some roofs have (gravel removal, ballast removal). Everything else is a mil-thickness number and a topcoat color choice (silver vs. white).

---

## 3a. User-facing detail menu (VERIFIED — RMI Project Evaluation form, p.5)

The "Detail Drawings — check all applicable" list on RMI's own intake form is the finite menu the UI shows. Each item maps to a drawing family below; the UI filters the menu to the selected roof type.

| Menu item (as on RMI form) | Drawing family | Shown for |
|---|---|---|
| HVAC | CS-1/2/3 (flat), CS-13/15 (metal), CS-12/14 (concrete), CS-17 (new curb) | All |
| Curbs | Same as HVAC | All |
| Platform / Platforms | CS-8 sleeper, CS-9 wood block, CS-10 rubber block | Flat, concrete |
| Vent | SPF-15/16; P-6 (pipe vents) | All |
| Mechanical exhaust | CS curb family | All |
| Support blocks | CS-9, CS-10 | Flat, concrete |
| Walkpads | F-15, F-16 | Flat |
| Drain | D-1, D-2 cast iron; D-3 inlet | Flat, concrete |
| Scupper | D-4 overflow, D-5/D-6 wall | Flat, concrete |
| Gutter | W-7 seams, D-8 inlet/downspout, D-9 insert | All |
| Interior gutter | D-10, D-11 | Metal |
| Penetration / Penetrations | P-1 to P-10 by substrate; P-8 chem curb for clusters | All |
| Soil stack | P-6 | All |
| Site screen | P-5/P-7 (concrete), P-3-S, SPF-9 | All |
| Antenna | P-5/P-7 circular support; P-8 chem curb | All |
| Exp. joint | A-3 | Flat |
| Ducts | A-1, A-2; CS-11 support | All |
| Coping | W-1 to W-6 | Flat |
| Edge metal | F-1, F-2, F-3, SPF-6 | Flat, SPF |
| Counterflashing (×2 on form) | W-11 reglet; W-12/13/14 fixed | Flat |
| Wall metal | W-7/8/9 walls, W-10 conduit, W-15/16 stucco | Flat, concrete |
| Roof hatch | CS-1-TYP note 7 names ACCESS HATCH and SMOKE HATCH among the curb-mounted units — VERIFIED; CS-14-CON on concrete, CS-15-MP on metal | All |
| Typ. system config. | B-1-* concept drawings — this is the macro view itself | All |
| Skylight (not on form, in drawings) | F-12 | Metal |
| Solar Post (not on form, in drawings) | P-1-S, P-2-S, P-3-S | All |
| Ridge cap (not on form, in drawings) | F-21-M | Metal |

## 3b. Material takeoff (VERIFIED rates, estimate only — no pricing)

If the user enters approximate roof size, the configuration can carry a quantity estimate using the plate rates. Every plate says surface condition may require increased mils, so label it "estimate from spec coverage rates, not a bid."

| Stage | Rate (from plates) |
|---|---|
| Primer | 1 gal per 1,000 sq ft (min) |
| Flex 48 mil (flat systems) | 3 gal/sq |
| Flex 64 mil (gravel, ballast 15-yr, HRS, CCS) | 4 gal/sq |
| Flex 80 mil (garden 20-yr, HRS 15-yr, CCS 20-yr) | 5 gal/sq |
| Flex, metal flashings only (FL48) | seams/laps/fasteners/curbs — linear takeoff, ASSUMED allowance per detail until RMI gives a per-detail figure |
| Thane 17 / 22 / 28 mil | 1.5 / 2 / 2.5 gal/sq |
| White Plus 23 / 30 / 38 mil | 1.5 / 2 / 2.5 gal/sq |

Dollar figures never appear in the tool; they come from an RMI sales rep or contractor.

## 3c. The details in the tool (one row per entry in `DETAILS`)

This is the sync table: every clickable detail in `index.html`, in source order. **Menu label** is what the rep
sees; the id in brackets is the key in `DETAILS` and in each building's `details` list. **Drawings** gives the
detail's own drawing and 3D concept plus any `byRoof` override the tool swaps in when the roof type changes.
**Status** and **ASSUMED** are copied from that detail's own `src` text in the code — nothing in those two
columns is a new judgement. "No VERIFIED tag" means the tool cites the drawing but has not claimed the
assembly is verified against it.

**The shared curb core.** CS-1-TYP note 7, quoted from the drawing and VERIFIED: "DETAIL EQUALLY APPLIES TO ALL
CURB MOUNTED UNITS THAT CAN BE LIFTED INCLUDING VENTS, DUCTS, SOIL STACKS, CONDUIT PENETRATIONS, HVAC,
REFRIGERATION PENETRATIONS, ACCESS HATCH, SMOKE HATCH, SKYLIGHTS DOMES." The RTU, roof hatch, curb-mounted
skylight, kitchen exhaust fan and bin vent are therefore one assembly with a different unit on top, and they
share one build core, `scripts/rmi_curb.py`. Coating sequence VERIFIED for all five: clean, prepare and prime;
RMI-Flex flashing coat up the curb, over the top and turned down to the interior of the curb, encapsulating the
(E) flashing; RMI-Thane or RMI-White over all; unit lifted and reset on stainless screws with EPDM washers after
full cure. Note 8 scopes CS-1-TYP to BUR, modified bitumen, EPDM, PVC and TPO — exposed concrete is CS-12-CON
(liftable) / CS-14-CON (fixed), exposed metal curbs are CS-13-MP / CS-15-MP. The drawing is NOT TO SCALE and
carries no dimensions, so every number in every curb model is ASSUMED and every one is a named constant in
`scripts/rmi_curb.py`: curb footprint and height (taken from the footprint the app already drew at that
hotspot), wall and skirt thickness, where the skirt starts, the nailer, fastener size and 12" o.c. spacing, the
sealant bead, the 18" Flex apron onto the field (the same figure the RTU and D-1-TYP drain models use), the 3"
turn-down inside the curb, and all coat thicknesses.

`DETAILS` carries **25** entries. CLAUDE.md says 28. The difference looks like the two `byRoof` variants that
show the rep a different name (Bin vent, Manway / bin hatch) plus the Solar Post toggle, which is not in
`DETAILS` — worth confirming before that number is quoted to anyone.

| Menu label (id) | Drawings — incl. by-roof overrides | Model | Status | ASSUMED, per the tool's own text |
|---|---|---|---|---|
| HVAC curb (`curb`) | CS-13-MP · 3D CS13-1-8-3D · SPF → SPF-12-TYP, 3D B-1-SPF-1-3D | — code geometry | **VERIFIED** assembly: Flex up the full curb wall and over the top to the interior, counterflashing above, unit lifted and reset after cure | Wrap height on the SPF variant |
| Side laps (`lap`) | F-8-TYP · 3D F8-2-FT-3D | `rpanel-side-lap-F-8-TYP.glb` | **VERIFIED**: two panels lapped at a major rib, fastened through the crest, sealant at the voids, Flex encapsulating lap and fasteners crest to flat both sides, topcoat over all, field Flex optional | Rib profile; 24 ga. drawn at 0.05"; the 1" / 3/4" lap lips; lap fasteners at 12" o.c.; Flex 2" past the rib base; coat thicknesses |
| Standing seams (`sseam`) | F-9-TYP, F-20-TYP for seam laps · 3D B-1-F10-22-3D | `standing-seam-F-9-TYP.glb` | **VERIFIED**: crimped double-lock seam, vertical legs under a folded cap, clips concealed, Flex a shell over the cap, down both legs and onto the flat, topcoat over all. Note 11 re-crimping shown as a prep step | Drawing is NTS with no dimensions: seam silhouette (1.68" legs 2.4" tall under a 3.12" cap); 0.05" sheet; which cap laps over which; the interlocking plies inside the cap; concealed clip at 24" o.c.; Flex extent onto the flat; coat thicknesses |
| Skylight panels (`mskylight`) | F-12-TYP · no 3D render · SPF → no drawing, treated as a curb per SPF-12-TYP | — code geometry | Per F-12-TYP; no VERIFIED tag | The geometry itself (no 3D concept render); the SPF treatment |
| Vents (`vent`) | Plate D · no 3D render · SPF → SPF-16-TYP · concrete → **Bin vent**, CS-12-CON | `bin-vent-CS-1-TYP.glb` on the silo | **ASSUMED** on metal: no dedicated vent drawing for metal roofs in the library | The whole metal assembly; wrap height on SPF; the concrete case treated as a curb per CS-12-CON |
| Pipes (`mpipe`) | P-9-MP, EPDM boot; P-10-MP is the metal-jack alternative · no 3D render · SPF → SPF-3-TYP | — code geometry | Per P-9-MP; no VERIFIED tag | Wrap height on the SPF variant |
| Gutters (`gutter`) | W-7-TYP · 3D D-7-FT-24-3D | — code geometry | Per W-7-TYP; no VERIFIED tag. Standard exterior gutters carry a material-only warranty per Plate MP | — |
| Downspout inlets (`gutterinlet`) | D-8-TYP · 3D D8-9-FT-3D | — code geometry | Per D-8-TYP; no VERIFIED tag | — |
| Roof hatch (`hatch`) | CS-15-MP on metal · CS-1-TYP note 7 on flat · SPF → SPF-12-TYP · concrete → **Manway / bin hatch**, CS-14-CON | `roof-hatch-CS-1-TYP.glb` on the silo | **VERIFIED** that access and smoke hatches are curb-mounted units, named in CS-1-TYP note 7; on metal it is the CS-15-MP fixed curb | Hatch-specific wrap on SPF; lid size and 2" thickness, the 22° it stands open, hinge, hold-open arm, handle; the concrete skinning of the CS-1-TYP curb; plus the shared curb numbers above |
| Ridge cap (`ridge`) | F-21-M-TYP · no 3D render · SPF → SPF-2-TYP | `metal-ridge-cap-F-21-M-TYP.glb` on the warehouse | **VERIFIED**: (E) ridge cap over the (E) metal panel, metal closure at the panel end set in sealant or tape with a ribbon of sealant at any voids, closure fasteners, RMI-Flex at the cap, RMI-Thane over all. Note 12 is the only dimension the drawing gives: closures recessed a minimum 6" under the cap or flashing metal, else add flat stock — the model recesses 7.8". Note 11: closures tight fitting, edges sealed before the Flex. Note 13: no foam closures without written approval | No 3D concept render exists, so everything else: the 4-ft section; the 6" cap lap and its joggled end; the closure 18" from the ridge, its 3" width and the rectangular notches where the ribs pass; fasteners at 12" o.c.; how far the Flex turns over the cap edge and runs onto the panel; all coat thicknesses. Built for a 1:12 gable — the warehouse — so a different pitch needs a rebuild |
| HVAC curbs (`rtu`) | CS-1-TYP · 3D CS1-18-3D | `curb-mounted-unit-CS-1-TYP.glb` | **VERIFIED**. Note 7: the same detail covers vents, ducts, soil stacks, conduit, refrigeration lines, access and smoke hatches, skylight domes | Curb and unit sizes; nailer; skirt height; the (E) roof build-up |
| Drains (`drain`) | D-1-TYP · 3D CID-1-21-FT3D | `cast-iron-drain-D-1-TYP.glb` | **VERIFIED**, including the 18" out / 3" down / 1" topcoat extents. Water-test after install; plastic and ABS drains excluded from warranty | Bowl, clamping-ring and dish sizes |
| Scuppers (`scupper`) | D-4-TYP · 3D D4-1-FT-3D | `overflow-scupper-D-4-TYP.glb` | **VERIFIED**: tube above the (E) cant, Flex encapsulating the tube interior and min 12" onto the field, base coat up the (E) wall flashing, topcoat over all, sealant bead at the exterior termination | 16" x 5" tube; exterior collar with the bead run all round; the tube bottom bent down over the cant; 6" cant; flashing height; coat thicknesses |
| Wall tie-in (`wall`) | W-11-TYP · 3D W13-FT-26-3D | `reglet-counterflashing-W-11-TYP.glb` | **VERIFIED**: Flex the full height of the (E) flashing up to the reglet receiver, not a fixed band; term bar 12" o.c.; counterflashing removed and reset. Note 7 applies to Fry-type reglets | Flashing height, 24" used here; reglet height; cant; counterflashing lap; coat extents |
| Pipes / soil stacks (`pipe`) | P-6-TYP · 3D P3SP-11-FT-3D | `lead-soil-stack-P-6-TYP.glb` | **VERIFIED**: lead up the stack and turned into the bore, sealant bead at the base, Flex encapsulating the lead and extending inside the stack, topcoat past the Flex. Note 7 covers conduit, HVAC and refrigeration penetrations | Drawing is NTS with no dimensions: 4" stack; 24" height; 14" lead flange; Flex 6" past the flange and 6" down the bore; topcoat 1" past the Flex |
| Skylights (`skylight`) | CS-1-TYP, note 7 names skylight domes · 3D CS1-18-3D | `curb-skylight-CS-1-TYP.glb` | **VERIFIED**: Flex up the full curb and over the top to the interior; dome lifted and reset | Dome rise; retainer frame; condensation gutter; plus the shared curb numbers above |
| Edge metal (`edge`) | F-1-TYP · 3D F1-34-FT-3D | — code geometry | Per F-1-TYP; no VERIFIED tag | Flange width |
| Penthouse walls (`penthouse`) | W-13-TYP, fixed counterflashing · 3D W-11-24-FT-3D | `wall-counterflashing-fixed-W-13-TYP.glb`: a 4-ft section spliced into the office penthouse west face at the hotspot. Every penthouse draws the same cross-section in code (`PW13`), mitred at the corners | **VERIFIED**: counterflashing fixed, cannot be removed or lifted, stays in place (note 7), damaged metal replaced; bead of RMI approved sealant at its top edge; clean, prepare and prime; Flex encapsulates the (E) flashing up to the counterflashing; RMI-Thane / White encapsulates the Flex; 24 ga. skirt metal extends min 4" over the RMI system. Coating the counterflashing assembly is optional (not shown). The drawing has no term bar: the counterflashing's own top flange carries the bead. Note 9: all (E) BUR, mod-bit, EPDM, PVC, TPO regardless of wall type | Drawing is NTS: counterflashing top 24", 6" deep, 1" off the wall, 1/2" hem; the (E) flashing running up behind it to its top; 6" cant and 10" foot (not drawn); coats 1/2" up behind the hem; skirt 21" to 13.5" (5" lap); skirt fasteners 12" o.c.; skirt fitted after the topcoat; coat thicknesses (§5 #21) |
| Sleeper supports (`sleeper`) | CS-8-TYP · 3D CS8-2-19-3D | `sleeper-support-CS-8-TYP.glb` at the office hotspot sleeper and under both sleepers of the hotel hotspot condenser; the rest code-drawn to the same sizes | **VERIFIED**: wood sleeper raised and reset; Flex base coat and topcoat run continuous across the field under the support — nothing wraps the block; loose-laid walkpad set after the RMI materials have completely cured; damaged or rotted sleepers replaced. Note 7: all (E) BUR, mod-bit, EPDM, PVC, TPO and concrete deck systems. (The 2024 library file is named "CS 7 TYP Sleeper Support"; its title block reads CS-8-TYP.) | Drawing is NTS with no dimensions: 6x10 x 30" sleeper; 3/8" synthetic rubber pad 2.5" past the sleeper; the 6" raise; the 22" x 48" roof patch; coat thicknesses. Whether the (E) condition already has a pad |
| Pipe clusters (`pitchpan`) | P-8-TYP, Chem-Curb / pitch pan · 3D PP-1-FT-3D | `chem-curb-P-8-TYP.glb` on all three hospital pans | **VERIFIED**: Chem-Curb fabricated and installed per the manufacturer (Chem-Link), set in RMI M-1 sealant; clean, prepare and prime (note 10); interior pocket filled with RMI-Flex tapered from the penetration outward to shed water; Flex flashing coat over the curb onto the field and min 4" up each penetration past the curb (5" modelled); RMI-Thane / White min 2" up past the Flex (2.5" modelled). The drawing has no metal flange and no pourable sealer: the pocket fill is Flex. Note 7: any non-circular penetration, or where jacks or boots are not feasible. Note 8: all (E) BUR, mod-bit, EPDM, PVC, TPO and concrete deck systems | Drawing is NTS: 30" x 16" x 4" curb with a 1/2" wall; the four penetrations (3" vent, 2" line, two 1-1/2" conduits); 3/8" beads; fill 3/4" higher at a penetration, tapering over 4"; Flex 6" and topcoat 7" onto the field; coat thicknesses; curb set before priming (§5 #20) |
| Expansion joint (`ej`) | A-3-TYP, EPDM/PVC/TPO · no 3D render | — code geometry | Per A-3-TYP; geometry **ASSUMED** | The geometry itself (no 3D concept render) |
| Silo walls (`silowall`) | W-7-TYP, concrete and CMU walls · no 3D render | — code geometry | Per W-7-TYP, with vertical field application on silos per the Longview grain terminal project | Sequence and coverage on curved walls |
| Gallery supports (`support`) | P-5-C / P-7-C, circular supports on concrete · no 3D render | — code geometry | Per P-5-C / P-7-C; no VERIFIED tag | Wrap height |
| Kitchen exhaust (`exhaust`) | CS-1-TYP, note 7 names vents and ducts · 3D CS1-18-3D | `kitchen-exhaust-fan-CS-1-TYP.glb` | **VERIFIED** curb. Grease must be removed before priming — the plates allow no RMI material over contaminants | The degreasing method; fan housing, cowl, grease tray and motor sizes; plus the shared curb numbers above |
| Parapet / coping (`coping`) | W-1-TYP · 3D W1-11-FT3D | `metal-coping-joint-W-1-TYP.glb` | **VERIFIED**, including the 4" tape / 2" Flex / 2" topcoat extents. Note 7: coping must meet code and SMACNA for wind uplift or it is excluded from warranty | Open-joint gap; fastener spacing; coat thicknesses. The topcoat shows the entire-coping (system warranty) option |

**Not in `DETAILS`:** Solar Post supports is a separate toggle (`S.solar`) — drawings P-1-S-TYP, P-2-S-TYP and
P-3-S-TYP, no 3D render, code geometry. It appears in the emailed configuration as "Solar Post supports
(P-1-S-TYP)".

**14 of the 25 carry a Blender model**; the other 11 are generic code geometry pending the same treatment.

## 3d. MICRO table — the library's own drawing index

Each row = one detail the user can click into. 2D = the logic drawing (section + notes). 3D = the concept render to model from. "Applies to" is quoted from the drawing notes.

### Penetrations
| Detail | 2D logic drawing | 3D concept | Applies to |
|---|---|---|---|
| Pipe / soil stack / conduit (lead flashing) — **model** `models/lead-soil-stack-P-6-TYP.glb` (`scripts/build_lead_soil_stack_P-6-TYP.py`). Assembly VERIFIED to P-6-TYP; every dimension ASSUMED (drawing is NTS with no dimensions) | P-6-TYP | P3SP-11-FT-3D, P3SP-2-FT-3D, P3SP-14-FT-3D | BUR, mod-bit (notes say equally applies to conduit, HVAC, refrigeration lines) |
| Pipe penetration, BUR | P-1-BUR | P1BUR-1-FT-3D (roof jack) | BUR, mod-bit |
| Pipe penetration, single-ply | P-2-SP, P-3-SP | P3SP-3-2-FT-3D | PVC, EPDM, TPO |
| Pipe penetration, concrete deck | P-4-C, P-5-C, P-7-C | — | Direct over concrete; P-5/P-7 cover circular supports (site screen, solar, mechanical) |
| Pipe penetration, metal roof — EPDM boot | P-9-MP | — | All metal panel systems |
| Pipe penetration, metal roof — metal jack | P-10-MP | P1BUR-11-FT-3D | All metal panel systems |
| Non-circular / cluster penetration — chem curb / pitch pan — **model** `models/chem-curb-P-8-TYP.glb` (`scripts/build_chem_curb_P-8-TYP.py`). Assembly VERIFIED to P-8-TYP (curb in M-1, Flex-filled pocket tapered to shed water, Flex min 4" / topcoat min 2" up the penetrations); every dimension ASSUMED | P-8-TYP | PP-1-FT-3D, PP-1-1-3D, PP-1-6-3D, PP-5-6-3D | BUR, mod-bit, single-ply, concrete |
| **Solar post support flashing** | P-1-S-TYP, P-2-S-TYP, P-3-S-TYP (site screen pitch pan) | — (no 3D yet) | All solar post supports |

### Curbs & supports
| Detail | 2D | 3D | Applies to |
|---|---|---|---|
| Curb-mounted unit, cap can be lifted — **model** `models/curb-mounted-unit-CS-1-TYP.glb` (`scripts/build_curb_mounted_unit_CS-1-TYP.py`), assembly VERIFIED; curb/unit sizes ASSUMED. Four more units are derived from the same curb (rows below) | CS-1-TYP | CS1-18-3D, CS1-2-3D, CS1-4-3D + 18 variants | BUR, mod-bit, single-ply |
| **Roof hatch** — **model** `models/roof-hatch-CS-1-TYP.glb` (`scripts/build_roof_hatch_CS-1-TYP.py`), a 3.2-ft curb with the lid standing open, at all four hatch positions on the silo cap. Shared curb core and its ASSUMED numbers in §3c. On the silo's exposed concrete CS-14-CON / CS-12-CON govern, and the app skins the curb and patch to concrete — ASSUMED | CS-1-TYP note 7; CS-14-CON / CS-12-CON on concrete; CS-15-MP on metal | — | All curb-mounted hatches |
| **Curb-mounted skylight** — **model** `models/curb-skylight-CS-1-TYP.glb` (`scripts/build_curb_skylight_CS-1-TYP.py`), a 6-ft curb with an acrylic dome, at all five skylight positions on the school. Note 7 names SKYLIGHTS DOMES — VERIFIED. The school is mod-bit or TPO, so CS-1-TYP governs directly per note 8. Shared curb core and its ASSUMED numbers in §3c | CS-1-TYP | CS1-18-3D | BUR, mod-bit, single-ply |
| **Kitchen exhaust fan** — **model** `models/kitchen-exhaust-fan-CS-1-TYP.glb` (`scripts/build_kitchen_exhaust_CS-1-TYP.py`), a 4-ft curb with an upblast fan and a grease containment tray, at both exhaust positions on the restaurant. Note 7 names VENTS, DUCTS and HVAC — VERIFIED. TPO or mod-bit, so CS-1-TYP governs directly per note 8. Shared curb core and its ASSUMED numbers in §3c | CS-1-TYP | CS1-18-3D | BUR, mod-bit, single-ply |
| **Bin vent** — **model** `models/bin-vent-CS-1-TYP.glb` (`scripts/build_bin_vent_CS-1-TYP.py`), a 2.4-ft curb with a vent neck and conical rain cap, at all four vent positions on the silo cap. Note 7 opens its list with VENTS, DUCTS — VERIFIED. Exposed concrete, so CS-12-CON governs: same note 7 list and same coating sequence, but no (E) sheet-metal flashing to encapsulate. The app skins the curb and patch to concrete — ASSUMED. Shared curb core and its ASSUMED numbers in §3c | CS-12-CON; CS-1-TYP note 7 | — | Exposed concrete (silo) |
| Curb-mounted unit, fixed (cannot lift) | CS-2-TYP, CS-3-TYP | CS1-1-18-3D, CS1-2-18-3D | BUR, mod-bit, single-ply |
| Support curb w/ skirt, BUR | CS-4-BUR, CS-6-BUR | — | BUR, mod-bit |
| Support curb, single-ply | CS-5-SP, CS-7-SP | — | PVC, EPDM, TPO |
| Sleeper support — **model** `models/sleeper-support-CS-8-TYP.glb` (`scripts/build_sleeper_support_CS-8-TYP.py`). Assembly VERIFIED to CS-8-TYP (coats continuous under the raised sleeper, walkpad after cure); every dimension ASSUMED | CS-8-TYP | CS8-2-19-3D, CS8-6-19-3D | All flat systems + concrete |
| Wood support block | CS-9-TYP | — | All flat systems + concrete |
| Rubber support block | CS-10-TYP | CS10-1-16-3D, CS10-16-2-3D, CS10-16-6-3D | All flat systems + concrete |
| Duct support | CS-11-TYP | — | All flat systems |
| Curb on concrete (lift / fixed) | CS-12-CON, CS-14-CON | — | Exposed concrete |
| **Curb on metal panel (lift / fixed)** | CS-13-MP, CS-15-MP | CS13-1-4-3D, CS13-1-8-3D, CS13-1-9-3D, CS13-1-16-3D | Metal panel systems |
| Low-profile support curb, BUR | CS-16-BUR | — | BUR, mod-bit |
| New HVAC pre-fab metal curb tie-in | CS-17-MC | — | BUR, mod-bit |

### Drains & water
| Detail | 2D | 3D | Applies to |
|---|---|---|---|
| Cast-iron roof drain — **model** `models/cast-iron-drain-D-1-TYP.glb` (`scripts/build_cast_iron_drain_D-1-TYP.py`), assembly + 18"/3"/1" extents VERIFIED; bowl/ring/dish sizes ASSUMED | D-1-TYP, D-2-TYP | CID-1-21-FT3D, CID-2-21-FT3D, CID-6-21-FT3D | All flat systems |
| Inlet drain | D-3-TYP | — | All flat systems |
| Overflow / thru-wall scupper — **model** `models/overflow-scupper-D-4-TYP.glb` (`scripts/build_overflow_scupper_D-4-TYP.py`), a 4-ft parapet section spliced into the big-box north parapet (both scuppers). VERIFIED: tube above the (E) cant, Flex encapsulates the tube interior and extends min 12" onto the field, base coat up the (E) wall flashing, topcoat over all, sealant bead at the exterior termination. ASSUMED: 16" x 5" tube, 1" exterior projection, 2" collar with the bead run all round, bottom bent 3" over the cant, 6" cant, full-height flashing, coat thicknesses | D-4-TYP | D4-1-FT-3D, D4-4-FT-3D, D4-5-FT-3D, D4-11-FT-3D | All flat systems + metal |
| Wall scupper | D-5-TYP, D-6-TYP (interior wall) | — | All flat systems |
| Metal gutter seams | W-7-TYP (filed under drains) | D-7-FT-24-3D, D-7-2-24-3D, D-7-11-24-3D | Metal gutters |
| Gutter inlet / downspout | D-8-TYP | D8-9-FT-3D, D8-FT-13-3D | BUR through metal |
| Gutter insert | D-9-TYP | — | Gutters |
| **Interior gutter, metal roof** | D-10-MP, D-11-MP | — | Metal panel systems |

### Walls & perimeter
| Detail | 2D | 3D | Applies to |
|---|---|---|---|
| Metal coping joints — **model** `models/metal-coping-joint-W-1-TYP.glb` (`scripts/build_metal_coping_joint_W-1-TYP.py`), a 4-ft parapet section spliced into the big-box east run; 4" tape / 8" Flex / entire-coping topcoat VERIFIED; joint gap, fastener spacing, primer extent ASSUMED | W-1-TYP, W-2-TYP | W1-11-FT3D, W1-5-6-FT3D, W1-20-3D | All coping laps/corners |
| Metal coping reset / fixed | W-3-TYP, W-4/5/6-TYP | W1-2-20-3D | All flat systems |
| Concrete wall / block wall / concrete cap | W-7, W-8, W-9-TYP | — | Concrete, CMU (not brick) |
| Wall-mounted conduit | W-10-TYP | — | All flat systems |
| Reglet counterflashing — **model** `models/reglet-counterflashing-W-11-TYP.glb` (`scripts/build_reglet_counterflashing_W-11-TYP.py`), a 4-ft section spliced into the school's gym-wall tie-in. Assembly VERIFIED (Flex to the reglet receiver, term bar 12" o.c., counterflashing removed/reset); flashing height 24" and all other sizes ASSUMED | W-11-TYP | W13-FT-26-3D + 4 variants | All flat systems; 3D notes include metal |
| Surface / fixed counterflashing — **model** `models/wall-counterflashing-fixed-W-13-TYP.glb` (`scripts/build_wall_counterflashing_fixed_W-13-TYP.py`), a 4-ft section spliced into the office penthouse west face. Assembly VERIFIED to W-13-TYP (fixed counterflashing left in place, sealant bead at its top, Flex up to the counterflashing, 24 ga. skirt min 4" over the system); every dimension ASSUMED | W-12, W-13, W-14-TYP | W-11-24-FT-3D + 4 variants | All flat systems |
| Stucco weep screed | W-15, W-16-TYP | — | Stucco walls |
| Perimeter edge metal | F-1-TYP | F1-34-FT-3D, F1-FT-8-3D + 4 variants | All flat systems |
| Perimeter edge, raised stop | F-2-TYP | — | All flat systems |
| Gravel guard | F-3-TYP | — | All flat systems |

### Field / seams (these are the macro-view seam patterns, seen up close)
| Detail | 2D | 3D | Applies to |
|---|---|---|---|
| Lap seam (BUR/single-ply) | F-4-TYP | F4-1-24-3D, F4-2-24-3D, F4-4-24-3D, F4-8-24-3D, F4-10-24-3D | All flat systems |
| Tape seam | F-5-TYP | — | All flat systems |
| **Metal end lap** | F-6-TYP, F-7-TYP | F6-10-23-3D, F6-19-23-3D, F6-19-28-3D | Metal panels |
| **R-panel side lap** — **model** `models/rpanel-side-lap-F-8-TYP.glb` (`scripts/build_rpanel_side_lap_F-8-TYP.py`), a 16" x 6-ft panel section spliced into the warehouse's right slope at the lap hotspot (the first model on a sloped metal roof). Assembly VERIFIED: two panels lapped at a major rib, fastened through the crest, sealant at the voids, Flex encapsulating lap and fasteners crest to flat both sides, topcoat over all; rib profile, lap lips, fastener spacing (12" o.c.), Flex extent past the rib base (2") and coat thicknesses ASSUMED | F-8-TYP | F8-2-FT-3D, F8-10-FT-3D + 6 variants | Metal panels |
| **Standing seam (S-seam)** — **model** `models/standing-seam-F-9-TYP.glb` (`scripts/build_standing_seam_F-9-TYP.py`), a 24" x 6-ft roof section spliced into the manufacturing building's right slope at the sseam hotspot. Assembly VERIFIED: a crimped double-lock seam (vertical legs under a folded cap) with the clips concealed, Flex as a shell fully encapsulating the seam — over the cap, down both legs and onto the flat both sides — and topcoat over all; note 11 (loose or improper crimping leaves voids and voids the warranty) is shown as a re-crimping PREP step, the loose cap standing proud until prep. The drawing is not to scale and gives no dimensions, so the seam silhouette (1.68" legs 2.4" tall under a 3.12" cap), sheet thickness drawn at 0.05", which cap laps over which, the interlocking plies inside the cap, the concealed clip and its 24" o.c. spacing, the Flex extent onto the flat and all coat thicknesses are ASSUMED | F-9-TYP, F-20-TYP | B-1-F10-22-3D | Metal panels |
| **Trapezoid panel** | F-10-TYP | F10-FT-22-3D, F10-FT-3-3D, F10-FT-6-3D, F10-FT-18-3D | Metal panels |
| Metal overlay panel | F-11-TYP | — | Metal panels |
| **Skylight (flush-mounted)** | F-12-TYP | — | Metal panels |
| Stone ballast field | F-13-TYP | — | Single-ply |
| Pavers field | F-14-TYP | — | Non-penetrating pavers |
| Walk pads | F-15, F-16-TYP | — | All flat systems |
| SPF field repair | F-17-TYP | — | SPF |
| Polyester-reinforced lap | F-18-TYP | — | All flat + concrete |
| Metal lap, stiffener bare | F-19-TYP | — | Metal |
| **Metal ridge cap** — **model** `models/metal-ridge-cap-F-21-M-TYP.glb` (`scripts/build_metal_ridge_cap_F-21-M-TYP.py`), a 4-ft section of ridge spliced into the code-drawn cap on the warehouse, the way the F-8-TYP lap splices into the slope. Cap over the panel, metal closure at the panel end set in sealant, closure fasteners, Flex over the cap lap and turned over both cap edges onto the panel, topcoat over all — VERIFIED, with note 12's 6" minimum closure recess the only dimension on the drawing. No 3D concept render exists, so the rest is ASSUMED; see §3c | F-21-M-TYP | — (none in the library) | Metal panels |

### Accessories, SPF-specific, concrete repairs
| Detail | 2D | 3D | Applies to |
|---|---|---|---|
| Duct joint / flexible connector / expansion joint | A-1, A-2, A-3-TYP | — | Metal ductwork; EPDM/PVC/TPO expansion joints |
| SPF: configuration, ridge, penetration, support block, edge metal, scupper, drain, site screen, HVAC duct, interior gutter, window base flashing, HVAC curb, inlet drain, curb vent, roof vent | SPF-1 … SPF-16-TYP | B-1-SPF-1-3D | SPF only |
| Concrete: crack repair, control joint, joints, spalling, perimeter edge band | F-21-CON, F-21-CON-CJ, F-22/23/24-CON | — | Concrete decks |

---

## 4. Changed from ASSUMED → VERIFIED

| Was ASSUMED in scope | Now VERIFIED | Source |
|---|---|---|
| Metal: Flex seams/laps only, then full-field Thane | Correct — **plus** fasteners, curbs, transitions, penetrations get Flex; field Flex is an *option* for pitted panels; primer is required under all Flex | Plate MP |
| Flat: full-field primer, Flex, Thane | Correct — Flex at 48 mil (3 gal/sq) standard, 64–80 on gravel/garden/HRS/CCS | Plates A, SP, SPF, C |
| Whether primer goes on before Flex on metal | Yes, always | Plate MP note 2 |
| Detail assemblies would need a "generic ASSUMED" placeholder | Not needed — every category has a 2D logic drawing and most have a 3D concept render | Detail + 3D folders |
| Solar Post would be a placeholder | Has three 2D details (P-1/2/3-S-TYP); no 3D render yet | Solar folder |

## 5. Open questions for RMI

Everything the tool had to decide without a document behind it, in one place. Each item says what the tool
currently does and where the number lives, so an answer is a one-line change. Nothing here is customer-facing
as RMI spec — the UI tags all of it ASSUMED.

### Sequencing and process

1. **Application order within a detail.** Does the pipe get Flex before or after the field around it? The
   drawings show the finished assembly, not the sequence. The tool simulates prep → primer → Flex on the
   penetration or flashing → Flex field (if a full-field roof) → topcoat everything.
2. **Wet and dry times between stages.** Used only to pace the animation, from the plate cure notes
   (Thane about 4 hr, White about 3 hr). Not presented as spec.
3. **W-1-TYP coping: is the whole coping primed** when the topcoat covers the entire coping under the system
   warranty? The tool primes only the 8" Flex band at each joint, matching the drawing's band logic, but
   topcoats the whole run.
4. **Degreasing method before priming a kitchen exhaust curb.** The plates are clear that no RMI material goes
   over a contaminant, but not how the grease comes off.

### Dimensions the drawings do not give

5. **How far Flex runs onto the field from a curb, and how far it turns down inside.** CS-1-TYP says only
   "EXTEND TO INTERIOR OF CURB", with no dimension. Every curb model uses 18" onto the field and a 3"
   turn-down. Both are single constants in `scripts/rmi_curb.py`, so both change in one place.
6. **W-11-TYP wall flashing height.** The drawing runs Flex the full height of the (E) base flashing to the
   reglet but does not dimension the flashing. The tool uses 24", with the reglet 2" above it and the
   counterflashing lapping 4". A typical height or a range would settle the model and the code run together.
7. **Parapet base flashing height.** D-4-TYP draws the Flex base coat the full height of the (E) wall flashing
   up to the coping, so every parapet now shows a 6" cant, base flashing, and Flex and topcoat to the coping.
   Cant size and flashing height are assumed (`PB` in index.html).
8. **D-4-TYP scupper sizes and exterior termination.** The drawing is NTS. The tool uses a 16" x 5" sheet-metal
   tube with a 2" exterior collar and runs the sealant bead round the whole collar, where the drawing shows the
   bead only at the bottom. Also: is the 12" field extent measured from the cant toe, as modelled, or from the
   wall? All named constants in `scripts/build_overflow_scupper_D-4-TYP.py`.
9. **P-6-TYP soil stack dimensions.** Not to scale, no dimensions. The model uses a 4" stack 24" above the roof,
   1/16" lead with a 14" base flange turned 1" into the bore, a 3/8" sealant bead, Flex 6" past the flange and
   6" down the bore, and topcoat 1" past the Flex. All named constants in
   `scripts/build_lead_soil_stack_P-6-TYP.py`.
10. **F-8-TYP side lap sizes.** NTS and dimensions nothing. The model uses a 6.6" x 1.32" rib with a 3" crest,
    lap fasteners at 12" o.c. through the crest, Flex 2" past the rib base onto the flat with primer on the same
    band, and sealant beads at both lap edges. Does RMI specify a minimum Flex extent past the rib, and a
    lap-fastener spacing? Constants in `scripts/build_rpanel_side_lap_F-8-TYP.py` and `LAP` in index.html.
11. **F-9-TYP standing seam sizes.** The drawing is explicitly not to scale and carries no dimensions, and says
    the seam configuration may vary. The model uses a generic 24" o.c. double lock: 1.68" legs 2.4" tall under a
    3.12" cap, sheet drawn at 0.05", concealed clips at 24" o.c. Constants in
    `scripts/build_standing_seam_F-9-TYP.py` and `SEAM` in index.html.

### Details with no drawing behind them

12. **Roof vents on metal roofs.** No dedicated vent drawing in the library; the tool falls back to Plate D for
    metal ducts, vents and curbs, and the assembly is assumed. SPF has SPF-16-TYP; exposed concrete is treated
    as a curb per CS-12-CON.
13. **Flush-mounted skylight panels on SPF.** No SPF skylight drawing; treated as a curb per SPF-12-TYP.
14. **The arena's roof hatch sits on a metal roof slope**, where CS-15-MP (fixed metal) governs. That is a
    different assembly from the CS-1-TYP curb: the (E) fasteners come out and new 24 ga. skirt metal extends a
    minimum 4" over the RMI system, with Flex to the underside of the (E) vertical metal. It is the next curb
    model; the arena hatch is code geometry until then.
15. **Wrap heights on the SPF variants** of the HVAC curb (SPF-12-TYP), pipe penetration (SPF-3-TYP) and roof
    hatch (SPF-12-TYP), and on the gallery support (P-5-C / P-7-C). Each is a single number in the builder. (The penthouse wall, W-13-TYP,
    is off this list: Flex runs up to the fixed counterflashing, VERIFIED 2026-09-14; its sizes are #21.) (The sleeper support, CS-8-TYP, is off this list:
    the drawing has no wrap — the coats run continuous under the raised sleeper. VERIFIED 2026-09-14.)
16. **Ridge cap and expansion joint: no 3D concept render.** A-3-TYP still has none, so the expansion joint
    shape is assumed. F-21-M-TYP is now modelled to its 2D drawing, but with no render to check the massing
    against, these are open: is a 6" cap lap right, and is the closure typically nearer the ridge than the
    18" the model uses? Note 12 only sets the minimum recess, not the position. Constants in
    `scripts/build_metal_ridge_cap_F-21-M-TYP.py`.
17. **Vertical application on silo walls.** W-7-TYP covers concrete and CMU walls, but sequence and coverage on
    a curved silo wall come from the Longview grain terminal project rather than a drawing.

### Takeoff

18. **Per-detail Flex allowance for the material estimate**, especially on metal roofs: how many gallons a curb,
    or a run of side lap, actually consumes. The plates give field rates only, so the tool's per-detail
    allowances are assumed and labelled as such in the UI.
19. **Building type to roof type pairing** (which roof types to offer for a school versus a warehouse). Not an
    RMI question; drafted from public building-stock data and tagged.
20. **P-8-TYP Chem-Curb sizes and order.** NTS, no dimensions beyond the 4" Flex and 2" topcoat minimums up the
    penetration. The model uses a 30" x 16" x 4" curb with a 1/2" wall around four penetrations, 3/8" M-1 beads
    inside and outside the curb and at each penetration, fill 3/4" higher at a penetration tapering over 4", and
    Flex 6" / topcoat 7" onto the field. Open: is the curb set before or after priming (modelled before), how far
    does the Flex run onto the field, and how high should the fill crown at the penetration? Constants in
    `scripts/build_chem_curb_P-8-TYP.py`.
21. **W-13-TYP fixed counterflashing sizes and the skirt.** NTS, no dimensions beyond the skirt's min 4" over the
    RMI system. The model puts the counterflashing top 24" above the roof, 6" deep, standing 1" off the wall with a
    1/2" hem; the (E) flashing runs up behind it; Flex and topcoat tuck 1/2" up behind the hem; the skirt runs 21" to
    13.5" (5" lap) with fasteners 12" o.c. through the counterflashing. Open: a typical counterflashing height; is the
    skirt fitted after the topcoat (modelled) or before it; is the skirt required every time or only where the
    counterflashing doesn't reach 4" over the system? The drawing shows no term bar — confirm none is wanted.
    Constants in `scripts/build_wall_counterflashing_fixed_W-13-TYP.py` and `PW13` in index.html.

---

## 6. Recommended first vertical slice

**Warehouse × R-panel metal roof × one curb-mounted HVAC unit.**

Why: metal is RMI's most distinctive application (seam-trace), the R-panel side-lap family has the most 3D references (8), the metal curb detail has 4 concept renders (CS13-1-*), and it exercises both stages the demo needs to sell — "Flex only where the roof leaks, Thane over everything."

Stage sequence for that slice (VERIFIED pattern, ASSUMED ordering):
1. Existing roof — rust at laps, fastener heads
2. Prep — rust treated, fasteners replaced
3. Primer — seams, laps, fasteners, curb
4. Flex (gold) — traces every side lap, end lap, fastener head, and wraps the curb base
5. Thane (silver) — full-field spray, everything goes uniform
6. Optional: swap topcoat to White Plus; add Solar Post supports (P-1-S-TYP)

Zoom target: the curb (CS-13-MP / CS13-1-8-3D) and one side lap (F-8-TYP / F8-2-FT-3D).

---

## 7. What to put in the project's Files (not all 296)

- All 17 spec plates (macro source of truth)
- The 2D logic drawing + one "FT" 3D render for each detail in the first slice, then add per detail as we build
- Flex / Thane / White Plus web data sheets
- This catalog
