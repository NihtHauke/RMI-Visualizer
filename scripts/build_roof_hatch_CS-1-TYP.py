"""
build_roof_hatch_CS-1-TYP.py — roof access / smoke hatch on the standard RMI curb.

    blender -b --python scripts/build_roof_hatch_CS-1-TYP.py

The curb, the coatings and every dimension they carry come from rmi_curb.py — read its docstring for
what CS-1-TYP says and what is ASSUMED. CS-1-TYP note 7 names "ACCESS HATCH, SMOKE HATCH" in the list
of curb-mounted units the detail applies to, so the hatch IS the RTU assembly with a lid on top.

ASSUMED here (no hatch drawing in the library carries dimensions): the 3.2-ft curb footprint and 14.4"
height (they match the footprint index.html already draws at the hatch hotspots), the lid size and its
2" thickness, the 22 degrees it stands open, the hinge barrel, the hold-open arm and the grab handle.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import math
from rmi_blender import IN, M, box, cyl, reset_scene, finalize
from rmi_curb import curb_core, report

CURB_W_IN, CURB_H_IN = 38.4, 14.4      # 3.2 ft x 1.2 ft — the footprint the app draws at the hatch hotspot
LID_OVER_IN = 2.0                      # lid overhangs the curb each side
LID_T_IN = 2.0
OPEN_DEG = 22.0                        # how far the lid stands open
HINGE_R_IN = 0.7

reset_scene()
C = curb_core(CURB_W_IN, CURB_H_IN)
top = C["top"]
CW = CURB_W_IN * IN

# hatch frame sitting on the nailer (the hatch's own curb cap)
box("unit_frame", "existing", CW + 1.2 * IN, CW + 1.2 * IN, 1.0 * IN, 0, 0, top + 0.5 * IN, M("coping"))

# lid, hinged along the -y edge and standing open
LID = CW + 2 * LID_OVER_IN * IN
T = LID_T_IN * IN
a = math.radians(OPEN_DEG)
hy, hz = -CW / 2, top + 1.0 * IN
cy = hy + (LID / 2) * math.cos(a) - (T / 2) * math.sin(a)
cz = hz + (LID / 2) * math.sin(a) + (T / 2) * math.cos(a)
lid = box("unit_lid", "existing", LID, LID, T, 0, cy, cz, M("coping"))
lid.rotation_euler = (a, 0, 0)
cap = box("unit_lid_cap", "existing", LID - 3 * IN, LID - 3 * IN, 0.5 * IN,
          0, cy - (T / 2 + 0.25 * IN) * math.sin(a), cz + (T / 2 + 0.25 * IN) * math.cos(a), M("unitD"))
cap.rotation_euler = (a, 0, 0)

# hinge barrel along x at the back edge
hg = cyl("unit_hinge", "existing", HINGE_R_IN * IN, LID * 0.55, 0, hy, hz, M("unitD"), verts=16)
hg.rotation_euler = (0, 1.5708, 0)

# hold-open arm from the curb side up to the lid
arm = cyl("unit_arm", "existing", 0.28 * IN, LID * 0.52, CW / 2 - 2 * IN, -1.5 * IN, top + LID * 0.24, M("fast"), verts=12)
arm.rotation_euler = (math.radians(58), 0, 0)

# grab handle near the free edge of the open lid
gy = hy + LID * 0.84 * math.cos(a)
gz = hz + LID * 0.84 * math.sin(a)
gh = cyl("unit_handle", "existing", 0.35 * IN, CW * 0.34, 0, gy, gz + 2.2 * IN, M("fast"), verts=12)
gh.rotation_euler = (0, 1.5708, 0)
for i, sx in enumerate((-1, 1)):
    box(f"unit_handle_leg_{i}", "existing", 0.5 * IN, 0.5 * IN, 2.4 * IN,
        sx * CW * 0.15, gy, gz + 1.1 * IN, M("fast"))

report("roof hatch", C)
finalize("roof-hatch-CS-1-TYP")
