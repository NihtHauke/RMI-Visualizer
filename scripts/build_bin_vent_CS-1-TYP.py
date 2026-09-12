"""
build_bin_vent_CS-1-TYP.py — bin / roof vent with a rain cap, on the standard RMI curb.

    blender -b --python scripts/build_bin_vent_CS-1-TYP.py

Curb and coatings from rmi_curb.py (CS-1-TYP) — read its docstring for what the drawing says and what
is ASSUMED. CS-1-TYP note 7 opens its list with "VENTS, DUCTS" — VERIFIED; the vent is the RTU
assembly with a vent neck and rain cap on top.

SUBSTRATE: on the silo the roof is exposed concrete, where CS-12-CON (curb mounted units, concrete,
liftable) governs rather than CS-1-TYP — note 8 of CS-1-TYP scopes it to BUR / modified bitumen /
EPDM / PVC / TPO. Both drawings carry the same note 7 list and the same coating sequence (clean,
prepare and prime; RMI-Flex flashing coat extended to the interior of the curb; RMI-Thane / RMI-White
over all); CS-12-CON has no (E) sheet-metal flashing to encapsulate. The app skins this model's curb
and roof patch to concrete at the silo, which is ASSUMED and flagged in the catalog.

ASSUMED: the 2.4-ft curb footprint and 12" height (matching what index.html draws at the vent
hotspot), the neck diameter, the rain cap, its three standoffs and the bird screen band.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import math
from rmi_blender import IN, M, box, cyl, reset_scene, finalize
from rmi_curb import curb_core, report

CURB_W_IN, CURB_H_IN = 28.8, 12.0      # 2.4 ft x 1.0 ft — the footprint the app draws at the vent hotspot
NECK_R_IN = 9.0
NECK_H_IN = 20.0
CAP_R_IN = 15.0
CAP_H_IN = 7.0
STAND_N = 3

reset_scene()
C = curb_core(CURB_W_IN, CURB_H_IN)
top = C["top"]
CW = CURB_W_IN * IN

# collar on the nailer, then the vent neck
box("unit_collar", "existing", CW + 1.0 * IN, CW + 1.0 * IN, 1.0 * IN, 0, 0, top + 0.5 * IN, M("coping"))
z0 = top + 1.0 * IN
cyl("unit_neck", "existing", NECK_R_IN * IN, NECK_H_IN * IN, 0, 0, z0 + NECK_H_IN * IN / 2, M("coping"), verts=24)

# bird screen band just under the cap
cyl("unit_screen", "existing", (NECK_R_IN + 0.3) * IN, 4.0 * IN, 0, 0, z0 + NECK_H_IN * IN - 2.5 * IN, M("unitD"), verts=24)

# conical rain cap on three standoffs
zc = z0 + NECK_H_IN * IN + 3.0 * IN
cyl("unit_cap", "existing", CAP_R_IN * IN, CAP_H_IN * IN, 0, 0, zc + CAP_H_IN * IN / 2, M("coping"), verts=24, r2=1.2 * IN)
for i in range(STAND_N):
    a = 2 * math.pi * i / STAND_N
    box(f"unit_standoff_{i}", "existing", 0.6 * IN, 0.6 * IN, 4.0 * IN,
        math.cos(a) * (NECK_R_IN - 0.6) * IN, math.sin(a) * (NECK_R_IN - 0.6) * IN,
        z0 + NECK_H_IN * IN + 1.0 * IN, M("fast"))

report("bin vent", C)
finalize("bin-vent-CS-1-TYP")
