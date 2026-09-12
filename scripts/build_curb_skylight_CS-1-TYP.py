"""
build_curb_skylight_CS-1-TYP.py — curb-mounted skylight dome on the standard RMI curb.

    blender -b --python scripts/build_curb_skylight_CS-1-TYP.py

Curb and coatings from rmi_curb.py (CS-1-TYP) — read its docstring for what the drawing says and what
is ASSUMED. CS-1-TYP note 7 names "SKYLIGHTS DOMES" in the list of curb-mounted units the detail
applies to — VERIFIED; the skylight is the RTU assembly with a dome on top.

ASSUMED: the 6-ft curb footprint and 14.4" height (matching what index.html draws at the school's
skylight hotspots), the dome rise, the aluminium retainer frame and the condensation gutter.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rmi_blender import IN, M, box, hemisphere, reset_scene, finalize
from rmi_curb import curb_core, report

CURB_W_IN, CURB_H_IN = 72.0, 14.4      # 6 ft x 1.2 ft — the footprint the app draws at the skylight hotspot
FRAME_IN = 1.6                         # aluminium retainer frame on the nailer
DOME_RISE = 0.42                       # dome height as a fraction of its radius

reset_scene()
C = curb_core(CURB_W_IN, CURB_H_IN)
top = C["top"]
CW = CURB_W_IN * IN

# retainer frame and condensation gutter on the nailer
box("unit_frame", "existing", CW + 1.6 * IN, CW + 1.6 * IN, FRAME_IN * IN, 0, 0, top + FRAME_IN * IN / 2, M("coping"))
box("unit_gutter", "existing", CW - 3 * IN, CW - 3 * IN, 0.6 * IN, 0, 0, top + FRAME_IN * IN - 0.3 * IN, M("unitD"))

# acrylic dome on an aluminium base band
R = CW / 2 * 0.94
box("unit_dome_base", "existing", 2 * R + 0.8 * IN, 2 * R + 0.8 * IN, 0.9 * IN, 0, 0, top + FRAME_IN * IN + 0.45 * IN, M("coping"))
d = hemisphere("unit_dome", "existing", R, 0, 0, top + FRAME_IN * IN + 0.9 * IN, M("glazing"), segments=28, rings=16)
d.scale = (1, 1, DOME_RISE)

report("curb-mounted skylight", C)
finalize("curb-skylight-CS-1-TYP")
