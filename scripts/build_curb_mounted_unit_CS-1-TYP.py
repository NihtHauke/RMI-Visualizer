"""
build_curb_mounted_unit_CS-1-TYP.py — curb-mounted HVAC unit per RMI detail CS-1-TYP (cap can be lifted),
with CS1-18-3D as the 3D reference. VERIFIED against the drawing in an earlier session; this script
reproduces the model that shipped in models/curb-mounted-unit-CS-1-TYP.glb so it can be regenerated.

    blender -b --python scripts/build_curb_mounted_unit_CS-1-TYP.py

What the drawing says (VERIFIED):
  * (E) curb with (E) flashing skirt and fasteners near the top; unit lifted (the app seats it 6" down
    and lifts it via existing__unit_* names) and reset.
  * Flex from the field up the full curb wall and over the top; sealant bead at the base; topcoat over all.
Curb size (8 ft × 18"), nailer, skirt height, unit size and the (E) roof build-up are ASSUMED (generic RTU).

One thing in the shipped .glb was wrong and is corrected here: the fasteners on the ±x faces had a
vertical axis (they read as flat coins edge-on); they now point into the curb like the ±y ones.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rmi_blender import IN, M, box, cyl, helper, cut, reset_scene, finalize

# ---------------------------------------------------------------- dimensions (metres; ASSUMED unless noted)
PATCH    = 156.0 * IN           # 13-ft square roof patch (the app's hMem hole sits just inside)
DECK_Z0, DECK_Z1 = -0.0787, -0.0635
MEM_T    = 0.0025

CW       = 96.0 * IN            # curb outside, 8 ft square
CH       = 18.0 * IN            # curb height
WT       = 0.0152               # curb wall (sheet-metal curb box)
SKIRT_Z0 = 0.1829               # (E) flashing skirt from here up to the curb top
SKIRT_T  = 0.0051
NAILER_T = 1.5 * IN             # wood nailer on the curb top
FAST_R, FAST_H, FAST_Z = 0.0056, 0.003, 15.5 * IN   # fasteners through the skirt near the top, 12" o.c.
FAST_S   = [0, 0.3048, -0.3048, 0.6096, -0.6096, 0.9144, -0.9144]

UNIT_W, UNIT_H, UNIT_Z0 = 2.8956, 1.0973, 0.6477     # unit body sits 6" above the curb (lifted); app seats it
TOP_W, TOP_H = 2.9464, 0.1016
FAN_R, FAN_H = 0.8047, 0.0762

WRAP_OUT = {"primer": 1.2276, "flex": 1.2291, "topcoat": 1.2306}   # half-width of the wrap up the curb wall
WRAP_TOP = {"primer": 0.4961, "flex": 0.4976, "topcoat": 0.4991}   # wrap rises just over the nailer
APRON    = {"primer": (3.3543, 0.0038), "flex": (3.3574, 0.0053), "topcoat": (3.3604, 0.0069)}   # (width, centre z) on the field
BEAD     = 0.0089                                                    # sealant bead at the curb base

reset_scene()

# (E) roof assembly (no hole under the curb — the curb sits on the membrane)
box("steel_deck", "existing", PATCH, PATCH, DECK_Z1 - DECK_Z0, 0, 0, (DECK_Z0 + DECK_Z1) / 2, M("deck"))
box("insulation", "existing", PATCH, PATCH, -DECK_Z1, 0, 0, DECK_Z1 / 2, M("insulation"))
box("membrane", "existing", PATCH, PATCH, MEM_T, 0, 0, MEM_T / 2, M("membrane"))

# (E) curb: four walls, flashing skirt (hollow square tube), wood nailer
for i, (x, y, sx, sy) in enumerate([(0, CW / 2 - WT / 2, CW, WT), (0, -(CW / 2 - WT / 2), CW, WT),
                                    (CW / 2 - WT / 2, 0, WT, CW), (-(CW / 2 - WT / 2), 0, WT, CW)]):
    box(f"curb_wall_{i}", "existing", sx, sy, CH, x, y, CH / 2, M("curb"))
skirt = box("flashing_skirt", "existing", CW + 2 * SKIRT_T, CW + 2 * SKIRT_T, CH - SKIRT_Z0, 0, 0, (SKIRT_Z0 + CH) / 2, M("coping"))
cut(skirt, helper(box("skirt_cutter", "existing", CW, CW, 2, 0, 0, CH / 2, M("coping"))))
box("nailer", "existing", CW, CW, NAILER_T, 0, 0, CH + NAILER_T / 2, M("wood"))

# Fasteners through the skirt, 12" o.c. on each face, pointing into the curb
face = CW / 2 + SKIRT_T + 0.0015
for s in FAST_S:
    for side, (x, y, rot) in enumerate([(s, face, (1.5708, 0, 0)), (face, -s, (0, 1.5708, 0)),
                                        (-s, -face, (-1.5708, 0, 0)), (-face, s, (0, -1.5708, 0))]):
        f = cyl(f"fastener_{side}_{round(s / IN)}", "existing", FAST_R, FAST_H, x, y, FAST_Z, M("fast"), verts=32); f.rotation_euler = rot

# (E) unit — named existing__unit_* so the app can seat/lift it
box("unit_body", "existing", UNIT_W, UNIT_W, UNIT_H, 0, 0, UNIT_Z0 + UNIT_H / 2, M("unit"), bevel=0.02)
box("unit_top", "existing", TOP_W, TOP_W, TOP_H, 0, 0, UNIT_Z0 + UNIT_H + TOP_H / 2, M("unitD"))
cyl("unit_fan", "existing", FAN_R, FAN_H, 0, 0, UNIT_Z0 + UNIT_H + TOP_H + FAN_H / 2, M("unitD"))

# Sealant bead at the base of the curb — prep/prime stage work
bo = CW / 2 + 0.0114
for i, (x, y, sx, sy) in enumerate([(0, bo, CW + 0.0229, BEAD), (0, -bo, CW + 0.0229, BEAD), (bo, 0, BEAD, CW + 0.0229), (-bo, 0, BEAD, CW + 0.0229)]):
    box(f"sealant_bead_{i}", "primer", sx, sy, BEAD, x, y, 0.0071, M("seal"))

# Coatings: apron on the field + wrap up the curb wall and over the top (hollow square tube)
inner = CW / 2
for layer, mat in (("primer", "primer"), ("flex", "flex"), ("topcoat", "thane")):
    w, z = APRON[layer]; box("field_apron", layer, w, w, 0.0013, 0, 0, z, M(mat))
    o, top = WRAP_OUT[layer], WRAP_TOP[layer]
    wrap = box("curb_wrap", layer, 2 * o, 2 * o, top, 0, 0, top / 2, M(mat))
    cut(wrap, helper(box("wrap_cutter", layer, 2 * inner, 2 * inner, 2, 0, 0, top / 2, M(mat))))
    inner = o

finalize("curb-mounted-unit-CS-1-TYP")
