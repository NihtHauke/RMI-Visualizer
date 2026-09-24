"""
build_metal_curb_unit_CS-13-MP.py — curb-mounted HVAC unit on a metal roof panel per RMI detail CS-13-MP (CURB MOUNTED
UNITS – METAL ROOF PANEL, 11/05/24), with CS13-1-8-3D as the 3D reference. Derived from build_curb_mounted_unit_CS-1-TYP.py
(same 8-ft curb and unit, same 18" apron, same 6" lift), spliced into the warehouse's sloped roof at the HVAC hotspot.

    blender -b --python scripts/build_metal_curb_unit_CS-13-MP.py

Two models, one per metal roof the warehouse offers, both at the warehouse's 1:12 pitch:
    models/metal-curb-unit-rpanel-1in12-CS-13-MP.glb     (R-panel, the warehouse default)
    models/metal-curb-unit-sseam-1in12-CS-13-MP.glb      (standing seam)
The shared curb, the panel patch and what the sheet does / does not say are in rmi_metal_curb.py.

What CS-13-MP adds over CS-1-TYP (VERIFIED): an (E) EXPOSED metal curb — no membrane flashing skirt; the Flex up the curb,
over the top and into its interior; the topcoat over it; the unit lifted, reset after full cure and fastened with
stainless steel screws with EPDM washers through its own downturned flange, the counterflashing CS13-1-8-3D draws with a
kicked-out drip. ASSUMED here: the 96" curb and the unit body/top/fan (the CS-1 RTU's), 18" of curb at its centre (so
14" up-slope and 22" down-slope at 1:12), and the placement numbers below, which come from index.html.

Placement (must match buildWarehouse / MCURB in index.html): right slope x = 18, z = 27 ft on a 120-ft building, so the
R-panel laps fall at bay offsets (o + 2.5) % 3 == 0 ft and the purlin fastener rows (z = 4, 9, 14, ... ft) cross the bay
at z = 24 and 29 ft — 36" up-slope and 24" down-slope of the curb's centre.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rmi_blender import IN, M, box, cyl
from rmi_metal_curb import Variant, build, counterflashing, screws, SCREW_DOWN

CURB_W, CURB_H = 96.0, 18.0           # 8-ft curb (the CS-1 RTU's); height at the curb centre above the pan
UNIT_H, TOP_OVER, TOP_H = 43.2, 1.0, 4.0     # unit body (CS-1: 1.0973 m), its dark top 1" over each side, 4" thick
FAN_R, FAN_H = 31.7, 3.0
RUST = [(24.0, 57.0, 1.4), (-24.0, -60.0, 1.1), (0.0, 55.0, 0.9)]    # on pans at the curb base (x on a pan for both roofs)


def unit(C):
    z0, face = counterflashing(C)
    C.unit_objs.extend(screws(C, face, C.top - SCREW_DOWN * IN, "unit_screw"))
    w, d = 2 * face[0], 2 * face[1]
    C.unit_objs.append(box("unit_body", "existing", w, d, UNIT_H * IN, 0, 0, z0 + UNIT_H / 2 * IN, M("unit"), bevel=0.02))
    zt = z0 + UNIT_H * IN
    C.unit_objs.append(box("unit_top", "existing", w + 2 * TOP_OVER * IN, d + 2 * TOP_OVER * IN, TOP_H * IN, 0, 0, zt + TOP_H / 2 * IN, M("unitD")))
    C.unit_objs.append(cyl("unit_fan", "existing", FAN_R * IN, FAN_H * IN, 0, 0, zt + (TOP_H + FAN_H / 2) * IN, M("unitD")))
    C.unit_top = zt + (TOP_H + FAN_H) * IN


for surface, hx in (("rpanel", 7), ("sseam", 6)):
    V = Variant(f"metal-curb-unit-{surface}-1in12-CS-13-MP", surface, 1, CURB_W, CURB_W, CURB_H, hx=hx, hz=6,
                lap_phase=2.5, rows=(36.0, -24.0), liftable=True, rust=RUST)
    build(V, unit)
