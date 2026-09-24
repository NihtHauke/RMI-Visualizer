"""
build_roof_hatch_metal_CS-15-MP.py — roof access hatch on a metal roof panel per RMI detail CS-15-MP (CURB MOUNTED UNITS
(FIXED) – METAL ROOF PANEL, 11/05/24). Spliced into the arena's standing-seam / R-panel slope at the hatch hotspot.

    blender -b --python scripts/build_roof_hatch_metal_CS-15-MP.py

What the drawing says (VERIFIED):
  * Note 7: applies to all curb-mounted units that CANNOT be lifted, including ACCESS HATCH, SMOKE HATCH. The hatch stays
    where it is — nothing is named existing__unit_*, nothing lifts.
  * (E) exposed metal curb. Clean, repair, prepare and prime per the Spec Guide Manual for each surface.
  * "RMI-FLEX VAPOR BARRIER-FLASHING COAT. EXTEND TO UNDERSIDE OF (E) VERTICAL METAL ENCAPSULATING (E) FLASHING." — the
    Flex runs up the curb and stops under the hatch frame's downturned (E) vertical metal.
  * RMI-Thane / RMI White over the Flex.
  * "REMOVE (E) FASTENERS AND FASTEN SKIRT METAL WITH STAINLESS STEEL SCREWS W/ EPDM WASHERS." — the (E) fasteners go at
    prep (existing__fastener_before_*, hidden from mid-prep); the new screws go in with the skirt.
  * "24 GA. SKIRT METAL. EXTEND A MIN. 4" OVER RMI SYSTEM." — new skirt from the fastener line down over the coats, 4.5"
    past the (E) vertical metal here (min 4" VERIFIED), with a kicked-out foot as drawn. Named existing__skirt_*: the app
    shows it over the finished system only.
ASSUMED: that the skirt goes on after the topcoat (the sheet shows the finished assembly, not the order); every size — the
48" x 36" curb (4 ft across the ribs so both walls sit on pans), 15" of curb at its centre (10.5" up-slope, 19.5"
down-slope at 3:12), the 1" frame, the 3" (E) vertical metal standing 1/2" off the curb, the lid (2" over each side, 2"
thick, standing open 70 degrees on its up-slope hinge), hold-open arm, handle; and the shared numbers in rmi_metal_curb.py.

Two models, R-panel and standing seam, at the arena's 3:12:
    models/roof-hatch-{rpanel,sseam}-3in12-CS-15-MP.glb
Placement (must match buildArena / MCURB in index.html): right slope x = -94, z = 89 ft on a 220-ft building, so the
R-panel laps fall at (o + 0.5) % 3 == 0 ft and the purlin row z = 89 ft runs through the curb's centre.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rmi_blender import IN, M, box, cyl
from rmi_metal_curb import Variant, build, screws, CF_KICK, CF_T

CURB_W, CURB_D, CURB_H = 48.0, 36.0, 15.0
FRAME_T = 1.0           # hatch frame on the curb top
VM_DROP, VM_OFF = 3.0, 0.5      # (E) vertical metal: how far it comes down, how far it stands off the curb face
SKIRT_PAST = 4.5        # new 24 ga. skirt below the (E) vertical metal (min 4" — VERIFIED)
SCREW_DOWN = 1.5        # fastener line below the curb top, through the (E) vertical metal
LID_OVER, LID_T, OPEN_DEG = 2.0, 2.0, 70.0
RUST = [(0.0, 22.0, 1.0), (0.0, -24.0, 0.8)]


def unit(C):
    L = C.level; t = CF_T * IN; top = C.top
    vx, vy = C.hx + VM_OFF * IN, C.hy + VM_OFF * IN          # inside of the (E) vertical metal
    ftop = top + FRAME_T * IN
    L.append(C.ring_tube("hatch_frame", "existing", vx + t, vy + t, C.ix, C.iy, top, ftop, M("coping")))
    zv = top - VM_DROP * IN
    L.append(C.ring_tube("hatch_vertical_metal", "existing", vx + t, vy + t, vx, vy, zv, ftop, M("coping")))
    # Flex and topcoat up the curb to the underside of the (E) vertical metal
    C.coats(zv - 0.02 * IN)
    # (E) fasteners through the vertical metal — removed at prep
    L.extend(screws(C, (vx + t, vy + t), top - SCREW_DOWN * IN, "fastener_before", washer=False))
    # new 24 ga. skirt: from the fastener line down over the RMI system, kicked out at its foot; new SS screws w/ EPDM washers
    sx, sy = vx + t + 0.04 * IN, vy + t + 0.04 * IN
    z1 = top - (SCREW_DOWN - 0.75) * IN
    z0 = zv - SKIRT_PAST * IN
    L.append(C.ring_tube("skirt_metal", "existing", sx + t, sy + t, sx, sy, z0, z1, M("coping")))
    k = CF_KICK * IN
    L.append(C.rtube("skirt_metal_kick", "existing", (sx + t + k, sy + t + k, sx + k, sy + k), (sx + t, sy + t, sx, sy), z0 - k * 0.8, z0, M("coping")))
    L.extend(screws(C, (sx + t, sy + t), top - SCREW_DOWN * IN, "skirt_screw"))

    # the lid, hinged on the up-slope (+y) edge and standing open toward the down-slope side (the view up the roof looks into
    # the hatch); dark insulated liner on its underside, hold-open arm from the curb to the lid, grab handle near the free edge
    LW, LD, T = 2 * vx + 2 * LID_OVER * IN, 2 * vy + 2 * LID_OVER * IN, LID_T * IN
    a = math.radians(OPEN_DEG)
    hy, hz = vy + LID_OVER * IN, ftop
    d, n = (-math.cos(a), math.sin(a)), (math.sin(a), math.cos(a))      # along the lid from the hinge / its top-side normal, (y, z)
    at = lambda s, h: (hy + s * d[0] + h * n[0], hz + s * d[1] + h * n[1])
    cy, cz = at(LD / 2, T / 2)
    lid = box("hatch_lid", "existing", LW, LD, T, 0, cy, cz, M("coping")); lid.rotation_euler = (-a, 0, 0); L.append(lid)
    ly, lz = at(LD / 2, -0.25 * IN)
    liner = box("hatch_lid_liner", "existing", LW - 4 * IN, LD - 4 * IN, 0.5 * IN, 0, ly, lz, M("unitD")); liner.rotation_euler = (-a, 0, 0); L.append(liner)
    hg = cyl("hatch_hinge", "existing", 0.7 * IN, LW * 0.55, 0, hy, hz, M("unitD"), verts=16); hg.rotation_euler = (0, 1.5708, 0); L.append(hg)
    p0 = (C.iy * 0.1, ftop); p1 = at(LD * 0.55, -0.6 * IN)
    dy, dz = p1[0] - p0[0], p1[1] - p0[1]
    arm = cyl("hatch_arm", "existing", 0.28 * IN, math.hypot(dy, dz), C.ix - 2 * IN, (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, M("fast"), verts=12)
    arm.rotation_euler = (math.atan2(-dy, dz), 0, 0); L.append(arm)
    gy, gz = at(LD * 0.86, T + 1.2 * IN)
    gh = cyl("hatch_handle", "existing", 0.35 * IN, LW * 0.3, 0, gy, gz, M("fast"), verts=12); gh.rotation_euler = (0, 1.5708, 0); L.append(gh)
    for i, sx in enumerate((-1, 1)):
        ey, ez = at(LD * 0.86, T + 0.6 * IN)
        leg = box(f"hatch_handle_leg_{i}", "existing", 0.5 * IN, 0.5 * IN, 1.2 * IN, sx * LW * 0.14, ey, ez, M("fast")); leg.rotation_euler = (-a, 0, 0); L.append(leg)
    C.unit_top = hz + LD * math.sin(a)   # for the hotspot height


for surface, hx in (("rpanel", 5), ("sseam", 4)):
    V = Variant(f"roof-hatch-{surface}-3in12-CS-15-MP", surface, 3, CURB_W, CURB_D, CURB_H, hx=hx, hz=4,
                lap_phase=0.5, rows=(0.0,), liftable=False, rust=RUST)
    build(V, unit)
