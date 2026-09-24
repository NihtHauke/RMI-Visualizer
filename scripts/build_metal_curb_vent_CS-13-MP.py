"""
build_metal_curb_vent_CS-13-MP.py — roof exhaust vent on a metal roof panel: a gooseneck vent hood on the CS-13-MP curb
(CURB MOUNTED UNITS – METAL ROOF PANEL, 11/05/24). Spliced into the manufacturing and arena slopes at every vent.

    blender -b --python scripts/build_metal_curb_vent_CS-13-MP.py

THERE IS NO VENT SHEET FOR METAL ROOFS in the RMI library. What the drawings do give (VERIFIED):
  * CS-13-MP note 7: "DETAIL EQUALLY APPLIES TO ALL CURB MOUNTED UNITS THAT CAN BE LIFTED INCLUDING VENTS, DUCTS, ..."
    — so a curb-mounted vent on a metal roof takes the CS-13-MP curb assembly (Flex up the curb, over the top and into
    the interior; topcoat over; the vent lifted, reset after cure, fastened with SS screws with EPDM washers).
  * Plate D (metal ducts / vents) covers the vent's own metal: seal, prime and Flex all joints, connections and fasteners;
    Thane or White, minimum two coats. The hood is drawn bare here — that work is not modelled.
ASSUMED: that this vent sits on a curb and can be lifted (a fixed one would be CS-15-MP), the gooseneck hood and every
size — 24" curb, 12" of curb at its centre, 12" neck 14" tall, 8" bend radius, bird screen — and the shared curb numbers
in rmi_metal_curb.py.

Four models: R-panel and standing seam, each at the manufacturing building's 1:12 and the arena's 3:12 pitch:
    models/metal-curb-vent-{rpanel,sseam}-{1in12,3in12}-CS-13-MP.glb
Placement (must match buildManufacturing / buildArena / SLOPE_BAY in index.html): vents at odd x on 60-ft (manufacturing,
-69/-9/51) and 42-ft (arena, -83/-41/1/43/85) spacing so every vent sees the same R-panel lap phase ((o + 2.5) % 3 == 0)
and the same purlin row through its centre (z = 14 ft on the manufacturing building, 19 ft on the arena).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rmi_blender import IN, M, cyl
from rmi_metal_curb import Variant, build, counterflashing, screws, half_torus, SCREW_DOWN

CURB_W, CURB_H = 24.0, 12.0
NECK_R, NECK_H = 6.0, 14.0
BEND_R = 8.0
OUTLET_H = 4.0
RUST = [(12.0, 17.0, 0.9), (-12.0, -18.0, 0.7)]


def unit(C):
    z0, face = counterflashing(C, solid_top=True)
    C.unit_objs.extend(screws(C, face, C.top - SCREW_DOWN * IN, "unit_screw"))
    zn = z0 + NECK_H * IN
    # the hood turns down-slope (-y): the neck, a 180-degree bend, a short outlet with a bird screen
    C.unit_objs.append(cyl("unit_neck", "existing", NECK_R * IN, NECK_H * IN, 0, 0, z0 + NECK_H / 2 * IN, M("coping"), verts=32))
    b = half_torus("unit_bend", "existing", BEND_R * IN, NECK_R * IN, 0, zn, M("coping"))
    b.rotation_euler = (0, 0, -math.pi / 2); C.unit_objs.append(b)
    oy = -2 * BEND_R * IN
    C.unit_objs.append(cyl("unit_outlet", "existing", NECK_R * IN, OUTLET_H * IN, 0, oy, zn - OUTLET_H / 2 * IN, M("coping"), verts=32))
    C.unit_objs.append(cyl("unit_screen", "existing", (NECK_R - 0.3) * IN, 0.2 * IN, 0, oy, zn - (OUTLET_H - 0.3) * IN, M("unitD"), verts=32))
    C.unit_top = zn + (BEND_R + NECK_R) * IN


for pitch, tag in ((1, "1in12"), (3, "3in12")):
    for surface, hx in (("rpanel", 4), ("sseam", 3)):
        V = Variant(f"metal-curb-vent-{surface}-{tag}-CS-13-MP", surface, pitch, CURB_W, CURB_W, CURB_H, hx=hx, hz=3,
                    lap_phase=2.5, rows=(0.0,), liftable=True, rust=RUST)
        build(V, unit)
