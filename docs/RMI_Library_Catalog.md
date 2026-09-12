# RMI Master Library → Roof Visualizer Catalog

Source: `2024_Master_RMI_Library.zip` (296 files, read 2026-09-04). Status tags: **VERIFIED** = taken directly from an RMI document in the library. **ASSUMED** = my inference, correct me.

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

## 3. MICRO table — detail assemblies (VERIFIED drawing index)

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
| Non-circular / cluster penetration — chem curb / pitch pan | P-8-TYP | PP-1-FT-3D, PP-1-1-3D, PP-1-6-3D, PP-5-6-3D | BUR, mod-bit, single-ply, concrete |
| **Solar post support flashing** | P-1-S-TYP, P-2-S-TYP, P-3-S-TYP (site screen pitch pan) | — (no 3D yet) | All solar post supports |

### Curbs & supports
| Detail | 2D | 3D | Applies to |
|---|---|---|---|
| Curb-mounted unit, cap can be lifted — **model** `models/curb-mounted-unit-CS-1-TYP.glb` (`scripts/build_curb_mounted_unit_CS-1-TYP.py`), assembly VERIFIED; curb/unit sizes ASSUMED. Four more units are derived from the same curb (rows below) | CS-1-TYP | CS1-18-3D, CS1-2-3D, CS1-4-3D + 18 variants | BUR, mod-bit, single-ply |
| **Roof hatch** — **model** `models/roof-hatch-CS-1-TYP.glb` (`scripts/build_roof_hatch_CS-1-TYP.py`), a 3.2-ft curb with the lid standing open, mounted at all four hatch positions on the silo cap. Note 7 names "ACCESS HATCH, SMOKE HATCH" — VERIFIED, the hatch is a curb-mounted unit, not the fixed curb it was guessed to be. The curb, the coatings and every dimension they carry come from the shared core `scripts/rmi_curb.py`. CS-1-TYP note 7 is VERIFIED and quoted there: "DETAIL EQUALLY APPLIES TO ALL CURB MOUNTED UNITS THAT CAN BE LIFTED INCLUDING VENTS, DUCTS, SOIL STACKS, CONDUIT PENETRATIONS, HVAC, REFRIGERATION PENETRATIONS, ACCESS HATCH, SMOKE HATCH, SKYLIGHTS DOMES" — so these four units and the RTU are one assembly with a different unit on top. Coating sequence VERIFIED: clean/prepare/prime, RMI-Flex flashing coat up the curb, over the top and turned down to the interior of the curb encapsulating the (E) flashing, RMI-Thane or RMI-White over all, unit lifted and reset on stainless screws with EPDM washers. The drawing is NOT TO SCALE and carries no dimensions, so every number is ASSUMED: curb footprint and height (taken from the footprint the app already drew at that hotspot), wall/skirt thickness, skirt start, nailer, fastener size and 12" o.c. spacing, sealant bead, the 18" Flex apron onto the field (the same figure the RTU and D-1-TYP drain models use), the 3" turn-down inside the curb, and all coat thicknesses. SUBSTRATE: the silo is exposed concrete, where CS-14-CON (fixed) / CS-12-CON (liftable) govern rather than CS-1-TYP — note 8 scopes CS-1-TYP to BUR / mod-bit / EPDM / PVC / TPO. The app skins the curb, skirt, nailer and roof patch to concrete there; the sheet-metal skirt geometry remains and is ASSUMED. Lid size, 2" thickness, the 22° it stands open, hinge, hold-open arm and handle are ASSUMED | CS-1-TYP note 7; CS-14-CON / CS-12-CON on concrete; CS-15-MP on metal | — | All curb-mounted hatches |
| **Curb-mounted skylight** — **model** `models/curb-skylight-CS-1-TYP.glb` (`scripts/build_curb_skylight_CS-1-TYP.py`), a 6-ft curb with an acrylic dome, mounted at all five skylight positions on the school. Note 7 names "SKYLIGHTS DOMES" — VERIFIED. The school is mod-bit or TPO, so CS-1-TYP governs directly (note 8). The curb, the coatings and every dimension they carry come from the shared core `scripts/rmi_curb.py`. CS-1-TYP note 7 is VERIFIED and quoted there: "DETAIL EQUALLY APPLIES TO ALL CURB MOUNTED UNITS THAT CAN BE LIFTED INCLUDING VENTS, DUCTS, SOIL STACKS, CONDUIT PENETRATIONS, HVAC, REFRIGERATION PENETRATIONS, ACCESS HATCH, SMOKE HATCH, SKYLIGHTS DOMES" — so these four units and the RTU are one assembly with a different unit on top. Coating sequence VERIFIED: clean/prepare/prime, RMI-Flex flashing coat up the curb, over the top and turned down to the interior of the curb encapsulating the (E) flashing, RMI-Thane or RMI-White over all, unit lifted and reset on stainless screws with EPDM washers. The drawing is NOT TO SCALE and carries no dimensions, so every number is ASSUMED: curb footprint and height (taken from the footprint the app already drew at that hotspot), wall/skirt thickness, skirt start, nailer, fastener size and 12" o.c. spacing, sealant bead, the 18" Flex apron onto the field (the same figure the RTU and D-1-TYP drain models use), the 3" turn-down inside the curb, and all coat thicknesses. Dome rise, retainer frame and condensation gutter are ASSUMED | CS-1-TYP | CS1-18-3D | BUR, mod-bit, single-ply |
| **Kitchen exhaust fan** — **model** `models/kitchen-exhaust-fan-CS-1-TYP.glb` (`scripts/build_kitchen_exhaust_CS-1-TYP.py`), a 4-ft curb with an upblast fan and a grease containment tray, mounted at both exhaust positions on the restaurant. Note 7 names "VENTS, DUCTS" and "HVAC" — VERIFIED. The restaurant is TPO or mod-bit, so CS-1-TYP governs directly (note 8). The curb, the coatings and every dimension they carry come from the shared core `scripts/rmi_curb.py`. CS-1-TYP note 7 is VERIFIED and quoted there: "DETAIL EQUALLY APPLIES TO ALL CURB MOUNTED UNITS THAT CAN BE LIFTED INCLUDING VENTS, DUCTS, SOIL STACKS, CONDUIT PENETRATIONS, HVAC, REFRIGERATION PENETRATIONS, ACCESS HATCH, SMOKE HATCH, SKYLIGHTS DOMES" — so these four units and the RTU are one assembly with a different unit on top. Coating sequence VERIFIED: clean/prepare/prime, RMI-Flex flashing coat up the curb, over the top and turned down to the interior of the curb encapsulating the (E) flashing, RMI-Thane or RMI-White over all, unit lifted and reset on stainless screws with EPDM washers. The drawing is NOT TO SCALE and carries no dimensions, so every number is ASSUMED: curb footprint and height (taken from the footprint the app already drew at that hotspot), wall/skirt thickness, skirt start, nailer, fastener size and 12" o.c. spacing, sealant bead, the 18" Flex apron onto the field (the same figure the RTU and D-1-TYP drain models use), the 3" turn-down inside the curb, and all coat thicknesses. Grease must come off before priming — no RMI material goes over a contaminant — but the degreasing method is ASSUMED. Fan housing, cowl, tray and motor housing sizes are ASSUMED | CS-1-TYP | CS1-18-3D | BUR, mod-bit, single-ply |
| **Bin vent** — **model** `models/bin-vent-CS-1-TYP.glb` (`scripts/build_bin_vent_CS-1-TYP.py`), a 2.4-ft curb with a vent neck and conical rain cap, mounted at all four vent positions on the silo cap. Note 7 opens its list with "VENTS, DUCTS" — VERIFIED. The curb, the coatings and every dimension they carry come from the shared core `scripts/rmi_curb.py`. CS-1-TYP note 7 is VERIFIED and quoted there: "DETAIL EQUALLY APPLIES TO ALL CURB MOUNTED UNITS THAT CAN BE LIFTED INCLUDING VENTS, DUCTS, SOIL STACKS, CONDUIT PENETRATIONS, HVAC, REFRIGERATION PENETRATIONS, ACCESS HATCH, SMOKE HATCH, SKYLIGHTS DOMES" — so these four units and the RTU are one assembly with a different unit on top. Coating sequence VERIFIED: clean/prepare/prime, RMI-Flex flashing coat up the curb, over the top and turned down to the interior of the curb encapsulating the (E) flashing, RMI-Thane or RMI-White over all, unit lifted and reset on stainless screws with EPDM washers. The drawing is NOT TO SCALE and carries no dimensions, so every number is ASSUMED: curb footprint and height (taken from the footprint the app already drew at that hotspot), wall/skirt thickness, skirt start, nailer, fastener size and 12" o.c. spacing, sealant bead, the 18" Flex apron onto the field (the same figure the RTU and D-1-TYP drain models use), the 3" turn-down inside the curb, and all coat thicknesses. SUBSTRATE: exposed concrete, so CS-12-CON governs rather than CS-1-TYP; both carry the same note 7 list and the same coating sequence, and CS-12-CON has no (E) sheet-metal flashing to encapsulate. The app skins the curb and patch to concrete; the skirt geometry remains and is ASSUMED. Neck, rain cap, its three standoffs and the bird screen are ASSUMED | CS-12-CON; CS-1-TYP note 7 | — | Exposed concrete (silo) |
| Curb-mounted unit, fixed (cannot lift) | CS-2-TYP, CS-3-TYP | CS1-1-18-3D, CS1-2-18-3D | BUR, mod-bit, single-ply |
| Support curb w/ skirt, BUR | CS-4-BUR, CS-6-BUR | — | BUR, mod-bit |
| Support curb, single-ply | CS-5-SP, CS-7-SP | — | PVC, EPDM, TPO |
| Sleeper support | CS-8-TYP | CS8-2-19-3D, CS8-6-19-3D | All flat systems + concrete |
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
| Surface / fixed counterflashing | W-12, W-13, W-14-TYP | W-11-24-FT-3D + 4 variants | All flat systems |
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
| **Metal ridge cap** | F-21-M-TYP | — | Metal panels |

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

Still ASSUMED (no document in the library):
- Application **order within a detail** (e.g. does the pipe get Flex before or after the field around it). Drawings show the finished assembly, not the sequence. I'll simulate: prep → primer → Flex on the penetration/flashing → Flex field (if full-field roof) → topcoat everything.
- Wet/dry times between stages for the animation timing — will use the plate cure notes (Thane ~4 hr, White ~3 hr) as pacing cues only.
- Building-type ↔ roof-type pairing (which roof types to offer for "school" vs "warehouse"). Not an RMI question; I'll draft from public building-stock data and tag it.
- ~~Roof hatch detail — no drawing in the library.~~ RESOLVED: CS-1-TYP note 7 names ACCESS HATCH and SMOKE HATCH in the list of curb-mounted units the detail applies to, so the hatch is the standard curb assembly with a lid. Still open: the **arena's hatch sits on a metal roof slope**, where CS-15-MP (fixed metal) governs — a different assembly, with the (E) fasteners removed and new 24 ga. skirt metal extending a min. 4" over the RMI system, Flex to the underside of the (E) vertical metal. That is the next curb model; the arena hatch is code geometry until then.
- **W-1-TYP coping: is the whole coping primed** when the topcoat covers the entire coping under the system warranty? The tool primes only the 8" Flex band at each joint (matching the drawing's band logic) but topcoats the whole run.
- **W-11-TYP wall flashing height.** The drawing runs Flex the full height of the (E) base flashing to the reglet but does not dimension the flashing. The tool uses 24" (reglet 2" above it, counterflashing lapping 4"). If RMI has a typical height or a range, the model and the code run both take it from one constant.
- **How far the Flex runs onto the field from a curb, and how far it turns down inside.** CS-1-TYP says only "EXTEND TO INTERIOR OF CURB" with no dimension. Every curb model uses 18" onto the field and a 3" turn-down, both ASSUMED, both single constants in `scripts/rmi_curb.py`.
- **D-4-TYP scupper sizes and exterior termination.** The drawing is NTS: the tool uses a 16" x 5" sheet-metal tube with a 2" exterior collar and runs the sealant bead round the whole collar (the drawing shows the bead only at the bottom). Is the 12" field extent measured from the cant toe (as modelled) or from the wall? All in `scripts/build_overflow_scupper_D-4-TYP.py` as named constants.
- **Parapet base flashing height.** D-4-TYP draws the Flex base coat the full height of the (E) wall flashing up to the coping, so every parapet in the tool now shows a 6" cant, base flashing and Flex/topcoat to the coping (previously an 18" band). Cant size and flashing height are ASSUMED (`PB` in index.html).
- **P-6-TYP soil stack dimensions.** The drawing is not to scale and carries no dimensions. The model uses a 4" stack 24" above the roof, 1/16" lead with a 14" base flange turned 1" into the bore, a 3/8" sealant bead, Flex 6" past the flange and 6" down the bore, topcoat 1" past the Flex. All in `scripts/build_lead_soil_stack_P-6-TYP.py` as named constants — correct any of them and rebuild.
- **F-8-TYP side lap sizes.** The drawing is NTS and dimensions nothing. The model uses a 6.6" x 1.32" rib with a 3" crest, lap fasteners at 12" o.c. through the crest, Flex 2" past the rib base onto the flat (primer the same band) and sealant beads at both lap edges. Does RMI specify a minimum Flex extent past the rib and a lap-fastener spacing? All in `scripts/build_rpanel_side_lap_F-8-TYP.py` and `LAP` in index.html as named constants.
- Per-detail Flex allowance for the material takeoff on metal roofs (how many gallons a curb or a run of side lap consumes). Plates give field rates only.

---

## 5. Recommended first vertical slice

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

## 6. What to put in the project's Files (not all 296)

- All 17 spec plates (macro source of truth)
- The 2D logic drawing + one "FT" 3D render for each detail in the first slice, then add per detail as we build
- Flex / Thane / White Plus web data sheets
- This catalog
