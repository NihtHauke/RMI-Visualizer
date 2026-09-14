"""
build_sleeper_support_CS-8-TYP.py — wood sleeper support on a loose-laid walkpad, per RMI detail CS-8-TYP
(SLEEPER SUPPORT – TYPICAL, 11/05/24) with CS8-2-19-3D (SLEEPER SUPPORT – CONCEPT DRAWING, 9/1/21) as the
3D reference. (In the 2024 library the 2D file is named "CS 7 TYP Sleeper Support"; its title block reads CS-8-TYP.)

    blender -b --python scripts/build_sleeper_support_CS-8-TYP.py

What the 2D drawing says (this is the logic the model follows):
  * WOOD SLEEPER SUPPORT. RAISE AND RESET SUPPORT BLOCK. REPLACE DAMAGED OR ROTTED SLEEPERS.
  * CLEAN, REPAIR, PREPARE AND PRIME the (E) roof system per the Specification Guide Manual.
  * RMI-FLEX VAPOR BARRIER-BASE COAT and RMI-THANE / RMI WHITE run as continuous lines across the field,
    UNDER the support — nothing wraps the block. The 3D concept shows the same stack: deck/roof, Flex,
    topcoat, then the synthetic rubber pad, then the support.
  * SET LOOSE LAID WALKPAD AFTER RMI MATERIALS HAVE COMPLETELY CURED; the sleeper sits on that pad.
  * Note 7: applies to all (E) BUR, mod-bit, EPDM, PVC, TPO and concrete deck systems.

What the drawing does NOT say: it is NOT TO SCALE and carries no dimensions. Every number below is ASSUMED.
The section box reads roughly 0.6 wide : 1 tall and the pad about 1.9x the sleeper width — the sizes keep
those proportions. The (E) roof build-up matches curb-mounted-unit-CS-1-TYP so the two read alike on one roof.

App behaviour: the sleeper is named existing__unit_sleeper and modelled 6" above its reset position; the app
seats it at the existing, prep and done stages and leaves it raised while the coats go on. The pad is
existing__walkpad; the app shows it only while the sleeper is seated (removed with the raise, set after cure).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rmi_blender import IN, M, box, bevel, reset_scene, finalize

# ---------------------------------------------------------------- dimensions (all ASSUMED — see docstring)
PATCH_W  = 22.0 * IN            # roof patch across the sleeper (the app's membrane hole sits 1.2" inside)
PATCH_L  = 48.0 * IN            # roof patch along the sleeper
DECK_Z0, DECK_Z1 = -0.0787, -0.0635   # steel deck, as the CS-1-TYP curb model
MEM_T    = 0.0025               # (E) membrane top = the roof surface the app sees at y=0

SL_W     = 5.5  * IN            # 6x10 nominal timber on edge — drawing proportion ~0.6 : 1
SL_H     = 9.25 * IN
SL_LEN   = 30.0 * IN            # along the sleeper (model +y → app -z)
LIFT     = 6.0  * IN            # raised this far while the coats go on; the app's seat offset is 6"

PAD_T    = 0.375 * IN           # loose-laid synthetic rubber walkpad
PAD_OVER = 2.5  * IN            # pad past the sleeper on every side (drawing: pad ~1.9x the sleeper width)

# Coatings: continuous flat coats across the patch, under the pad (VERIFIED direction; extents ASSUMED).
COAT     = 0.001                # visual thickness per layer (1 mm), same as the drain and soil-stack models
COAT_W   = {"primer": 20.0 * IN, "flex": 20.0 * IN, "topcoat": 20.2 * IN}   # 1" inside the patch each side
COAT_L   = {"primer": 46.0 * IN, "flex": 46.0 * IN, "topcoat": 46.2 * IN}

# ---------------------------------------------------------------- derived
COAT_TOP = MEM_T + 3 * COAT
PAD_W, PAD_L = SL_W + 2 * PAD_OVER, SL_LEN + 2 * PAD_OVER
SL_Z0    = COAT_TOP + PAD_T + LIFT    # sleeper bottom as modelled (raised)

reset_scene()

# (E) roof assembly — generic, per note 7
box("steel_deck", "existing", PATCH_W, PATCH_L, DECK_Z1 - DECK_Z0, 0, 0, (DECK_Z0 + DECK_Z1) / 2, M("deck"))
box("insulation", "existing", PATCH_W, PATCH_L, -DECK_Z1, 0, 0, DECK_Z1 / 2, M("insulation"))
box("membrane", "existing", PATCH_W, PATCH_L, MEM_T, 0, 0, MEM_T / 2, M("membrane"))

# Clean, repair, prepare and prime — then Flex base coat, then topcoat: each continuous under the support
for i, (layer, mat) in enumerate((("primer", "primer"), ("flex", "flex"), ("topcoat", "thane"))):
    box("field_coat", layer, COAT_W[layer], COAT_L[layer], COAT, 0, 0, MEM_T + (i + 0.5) * COAT, M(mat))

# Loose-laid walkpad, set after full cure, on top of the topcoat
box("walkpad", "existing", PAD_W, PAD_L, PAD_T, 0, 0, COAT_TOP + PAD_T / 2, M("rubber"))

# (E) wood sleeper — raised; the app seats it on the pad
bevel(box("unit_sleeper", "existing", SL_W, SL_LEN, SL_H, 0, 0, SL_Z0 + SL_H / 2, M("wood")), 0.25 * IN)

finalize("sleeper-support-CS-8-TYP")
