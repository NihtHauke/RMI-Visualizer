"""
build_gutter_seam_W-7-TYP.py — a lapped, riveted gutter seam per RMI detail W-7-TYP (GUTTER SEAMS – TYPICAL, 11/05/24;
the sheet filed under Drains — a different sheet under Walls carries the same number) with D-7-FT-24-3D (TYPICAL METAL
GUTTER – CONCEPT DRAWING, 9/1/21) as reference.

    blender -b --python scripts/build_gutter_seam_W-7-TYP.py

A 4-ft SECTION of the eave-hung gutter (scripts/rmi_gutter.py has the frame and every gutter size) with the seam at its
centre: the up-run section ends at x = 0 and the next section's end is nested 1" inside it, riveted through. The app
splices it into the code-drawn gutter run at the arena's and the hangar's gutter hotspot (gutterRun in index.html).

What the drawing says (VERIFIED):
  * (E) gutter (notes 11, 12): check for damaged components, replace damaged or broken ones; confirm seam / lap
    integrity, repair as needed; rust must not have pin holes or compromise integrity — patch or replace where it does.
  * Clean, prepare and prime per the Spec Guide Manual for each type of (E) gutter (note 12); adhesion test first (note 9).
  * "INSTALL TAPE OR 3 COURSE POLYESTER/RMI-FLEX A MIN. OF 2" EQUALLY SPACED OVER EACH SIDE OF JOINTS. INSURE NO VOIDS" —
    the band runs up the back wall, across the floor and up the front, following the seam (the yellow band on the sheet).
  * Note 8: the detail applies to all laps, joints, corners and transitions.
  * "RMI-THANE. ENCAPSULATE INTERIOR OF GUTTER" — the whole interior, not a band. Vertical interior surfaces may need
    multiple coats to prevent running and sagging.
  * "(OPTIONAL) RMI-FLEX VAPOR BARRIER-BASE COAT ENCAPSULATING INTERIOR OF GUTTER" — optional, so not modelled.
  * Note 7: the gutter must meet code and SMACNA for wind uplift, expansion and section lengths or it is excluded from
    warranty; note 10: plastic / ABS gutters are excluded. The sheet shows rivets through the lap (the circles on the
    back wall and floor) and no sealant, so none is drawn.

ASSUMED (the sheet is not to scale and carries no dimensions): every gutter size (rmi_gutter.py); a 1" lap with the
down-run section nested inside the up-run one; seven 5/16" rivets through the lap (three up the back, two across the
floor, two up the front); the Flex band drawn 2" past each edge of the 1" lap (5" wide) with the primer 1/2" past it;
the coat thicknesses; the topcoat stopping 1/2" below each wall's top edge.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rmi_blender import reset_scene, finalize
from rmi_gutter import (X0, X1, MT, W, D, COATS, BAND_TOP, trough, straps, coat_u, rivet)

LAP        = 1.0                        # the next section nests this far inside the up-run one (ASSUMED)
FLEX_SIDE  = 2.0                        # VERIFIED: min 2" each side of the joint
PRIMER_PAST = 0.5                       # primer past the Flex band (ASSUMED)
TOP_PAST   = 0.26                       # topcoat past the primer where it rises over the band (ASSUMED)
RIVET_X    = -LAP / 2                   # rivets through the middle of the lap
RIVETS_BACK, RIVETS_FLOOR, RIVETS_FRONT = (-1.5, -4.0, -6.5), (-3.0, -9.0), (-2.0, -5.5)   # heights on the walls, u across the floor

reset_scene()

# (E) gutter: the up-run section ends at the joint, the next section runs on from it with a 1" tab nested inside
trough("gutter_a", X0, 0.0)
trough("gutter_b", 0.0, X1)
trough("tab", -LAP, 0.0, inset=MT)
straps()
for i, v in enumerate(RIVETS_BACK):
    rivet(f"rivet_back_{i}", RIVET_X, -MT - 0.03, v, "u")
for i, u in enumerate(RIVETS_FLOOR):
    rivet(f"rivet_floor_{i}", RIVET_X, u, -D + MT + 0.03, "v")
for i, v in enumerate(RIVETS_FRONT):
    rivet(f"rivet_front_{i}", RIVET_X, -(W - MT) + 0.03, v, "u")

# Coats at the seam: primer and Flex bands over the joint, following the interior; topcoat over the whole interior,
# rising over the band to enclose it (VERIFIED extents, ASSUMED thicknesses)
fx0, fx1 = -LAP - FLEX_SIDE, FLEX_SIDE
px0, px1 = fx0 - PRIMER_PAST, fx1 + PRIMER_PAST
coat_u("primer", "primer_band", px0, px1, *COATS["primer"])
coat_u("flex", "flex_band", fx0, fx1, *COATS["flex"])
tx0, tx1 = px0 - TOP_PAST, px1 + TOP_PAST
coat_u("topcoat", "topcoat_run_a", X0, tx0, *COATS["topcoat"], caps=False)
coat_u("topcoat", "topcoat_run_b", tx1, X1, *COATS["topcoat"], caps=False)
coat_u("topcoat", "topcoat_band", tx0, tx1, COATS["topcoat"][0], BAND_TOP)

finalize("gutter-seam-W-7-TYP")
