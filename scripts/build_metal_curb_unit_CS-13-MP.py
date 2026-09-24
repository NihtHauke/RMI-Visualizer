"""
build_metal_curb_unit_CS-13-MP.py — curb-mounted HVAC unit on a metal roof panel per RMI detail CS-13-MP (CURB MOUNTED
UNITS – METAL ROOF PANEL, 11/05/24), with CS13-1-8-3D as the 3D reference. Derived from build_curb_mounted_unit_CS-1-TYP.py
(same curb, unit and 18" apron), spliced into the warehouse, manufacturing and arena slopes at every HVAC curb.

    blender -b --python scripts/build_metal_curb_unit_CS-13-MP.py

Four models, one per metal roof the buildings offer and per pitch — no HVAC curb on a metal roof is code-drawn:
    models/metal-curb-unit-{rpanel,sseam}-1in12-CS-13-MP.glb     warehouse and manufacturing (1:12, 8-ft curb)
    models/metal-curb-unit-{rpanel,sseam}-3in12-CS-13-MP.glb     arena (3:12, 10-ft curb)
The shared curb, the panel patch and what the sheet does / does not say are in rmi_metal_curb.py.

What CS-13-MP adds over CS-1-TYP (VERIFIED): an (E) EXPOSED metal curb — no membrane flashing skirt; the Flex up the curb,
over the top and into its interior; the topcoat over it; the unit lifted, reset after full cure and fastened with
stainless steel screws with EPDM washers through its own downturned flange, the counterflashing CS13-1-8-3D draws with a
kicked-out drip. ASSUMED here: the curbs (96" at 1:12 — the CS-1 RTU's — and 120" at 3:12, the size the arena already
drew), their heights at the centre (18" and 27", so 14"/22" and 12"/42" up-/down-slope), the units, and the placement
numbers below, which come from index.html.

Placement (must match buildWarehouse / buildManufacturing / buildArena / SLOPE_BAY in index.html): every curb sits where
the R-panel laps fall at bay offsets (o + 2.5) % 3 == 0 ft and at the same place relative to the purlin fastener rows
(z = 4, 9, 14, ... ft) — warehouse (18, 27) and manufacturing (90, 17) share one model; the arena curbs at (61, 30) and
(-59, 30) share the other.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rmi_blender import IN, M, box, cyl
from rmi_metal_curb import Variant, build, counterflashing, screws, SCREW_DOWN

# The unit script derives from the CS-1 RTU: its curb and unit, scaled per building (sizes ASSUMED).
RUST = [(24.0, 57.0, 1.4), (-24.0, -60.0, 1.1), (0.0, 55.0, 0.9)]    # on pans at the curb base (x on a pan for both roofs)
RUST_10 = [(36.0, 70.0, 1.4), (-12.0, -68.0, 1.1), (12.0, 68.0, 0.9)]


def make_unit(unit_h, top_over, top_h, fan_r, fan_h):
    def unit(C):
        z0, face = counterflashing(C)
        C.unit_objs.extend(screws(C, face, C.top - SCREW_DOWN * IN, "unit_screw"))
        w, d = 2 * face[0], 2 * face[1]
        C.unit_objs.append(box("unit_body", "existing", w, d, unit_h * IN, 0, 0, z0 + unit_h / 2 * IN, M("unit"), bevel=0.02))
        zt = z0 + unit_h * IN
        C.unit_objs.append(box("unit_top", "existing", w + 2 * top_over * IN, d + 2 * top_over * IN, top_h * IN, 0, 0, zt + top_h / 2 * IN, M("unitD")))
        C.unit_objs.append(cyl("unit_fan", "existing", fan_r * IN, fan_h * IN, 0, 0, zt + (top_h + fan_h / 2) * IN, M("unitD")))
        C.unit_top = zt + (top_h + fan_h) * IN
    return unit


# (tag, pitch, curb W, curb H at its centre, bay half-width per roof, bay half-length, R-panel lap phase, purlin rows, rust, unit)
VARIANTS = [
    # warehouse (18, 27) and manufacturing (90, 17): 1:12, 8-ft curb (the CS-1 RTU's); rows 3 ft up-slope and 2 ft down-slope
    ("1in12", 1, 96.0, 18.0, {"rpanel": 7, "sseam": 6}, 6, 2.5, (36.0, -24.0), RUST, make_unit(43.2, 1.0, 4.0, 31.7, 3.0)),
    # arena (61, 30) and (-59, 30): 3:12, the 10-ft curb the arena already drew, 27" at its centre (12" up-slope, 42" down-slope);
    # odd x so both 10-ft walls land on pans; rows 6 ft up-slope, 1 ft up-slope and 4 ft down-slope
    ("3in12", 3, 120.0, 27.0, {"rpanel": 8, "sseam": 7}, 7, 2.5, (72.0, 12.0, -48.0), RUST_10, make_unit(48.0, 1.0, 4.0, 36.0, 3.0)),
]

for tag, pitch, cw, ch, hxs, hz, phase, rows, rust, unit in VARIANTS:
    for surface in ("rpanel", "sseam"):
        V = Variant(f"metal-curb-unit-{surface}-{tag}-CS-13-MP", surface, pitch, cw, cw, ch, hx=hxs[surface], hz=hz,
                    lap_phase=phase, rows=rows, liftable=True, rust=rust)
        build(V, unit)
