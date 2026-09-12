"""
build_kitchen_exhaust_CS-1-TYP.py — upblast kitchen exhaust fan with a grease containment tray,
on the standard RMI curb.

    blender -b --python scripts/build_kitchen_exhaust_CS-1-TYP.py

Curb and coatings from rmi_curb.py (CS-1-TYP) — read its docstring for what the drawing says and what
is ASSUMED. CS-1-TYP note 7 opens its list with "VENTS, DUCTS" and also names "HVAC" — VERIFIED; the
exhaust fan is the RTU assembly with an upblast fan on top. Grease must be removed before priming (the
plates allow no RMI material over contaminants); the degreasing method is ASSUMED and the app says so.

ASSUMED: the 4-ft curb footprint and 16.8" height (matching what index.html draws at the restaurant's
exhaust hotspots), the fan housing and cowl sizes, the grease tray and its lip, and the motor housing.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rmi_blender import IN, M, box, cyl, reset_scene, finalize
from rmi_curb import curb_core, report

CURB_W_IN, CURB_H_IN = 48.0, 16.8      # 4 ft x 1.4 ft — the footprint the app draws at the exhaust hotspot
TRAY_OVER_IN = 7.0                     # grease tray oversails the curb
TRAY_T_IN = 1.2
HOUSE_R_IN = 15.0                      # fan housing
HOUSE_H_IN = 12.0
COWL_H_IN = 11.0

reset_scene()
C = curb_core(CURB_W_IN, CURB_H_IN)
top = C["top"]
CW = CURB_W_IN * IN

# grease containment tray over the curb, with a raised lip all round
TW = CW + 2 * TRAY_OVER_IN * IN
box("unit_tray", "existing", TW, TW, TRAY_T_IN * IN, 0, 0, top + TRAY_T_IN * IN / 2, M("unitD"))
for i, (x, y, sx, sy) in enumerate([(0, TW / 2, TW, 0.5 * IN), (0, -TW / 2, TW, 0.5 * IN),
                                    (TW / 2, 0, 0.5 * IN, TW), (-TW / 2, 0, 0.5 * IN, TW)]):
    box(f"unit_tray_lip_{i}", "existing", sx, sy, 1.6 * IN, x, y, top + TRAY_T_IN * IN + 0.8 * IN, M("unitD"))

# fan housing and upblast cowl — the discharge leaves the gap between them, up and out
z0 = top + TRAY_T_IN * IN
cyl("unit_housing", "existing", HOUSE_R_IN * IN, HOUSE_H_IN * IN, 0, 0, z0 + HOUSE_H_IN * IN / 2, M("unit"), verts=28)
cyl("unit_cowl_rim", "existing", (HOUSE_R_IN + 5.4) * IN, 1.0 * IN, 0, 0, z0 + HOUSE_H_IN * IN - 1.0 * IN, M("unitD"), verts=28)
cyl("unit_cowl", "existing", (HOUSE_R_IN + 5) * IN, COWL_H_IN * IN, 0, 0,
    z0 + HOUSE_H_IN * IN + COWL_H_IN * IN / 2 - 1.5 * IN, M("unitD"), verts=28, r2=(HOUSE_R_IN - 6) * IN)
box("unit_motor", "existing", 9 * IN, 9 * IN, 6 * IN, 0, 0,
    z0 + HOUSE_H_IN * IN + COWL_H_IN * IN + 1.5 * IN, M("unit"))

report("kitchen exhaust fan", C)
finalize("kitchen-exhaust-fan-CS-1-TYP")
