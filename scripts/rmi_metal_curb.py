"""
rmi_metal_curb.py — the metal-roof curb shared by the CS-13-MP (liftable) and CS-15-MP (fixed) units: a bay of sloped
R-panel or standing-seam roof with an exposed metal curb standing on it, spliced into buildGable's slope the same way the
F-8-TYP lap section is (index.html: `SLOPE_BAY`, `unitAt`, the slope-splice in makeSlope).

Derived from build_curb_mounted_unit_CS-1-TYP.py / rmi_curb.py: same apron figure, same "extend to interior" turn-down,
the same lift-and-seat convention for a liftable unit (built lifted, 14" here so it clears its own counterflashing). What changes on metal:

CS-13-MP (CURB MOUNTED UNITS – METAL ROOF PANEL, 11/05/24), VERIFIED, from the drawing:
  * (E) EXPOSED METAL CURB. No membrane flashing skirt (that is the CS-1-TYP flat-roof curb). Note 8: applies to all (E)
    exposed metal curbs regardless of configuration.
  * "CLEAN, REPAIR, PREPARE AND PRIME PER RMI SPECIFICATION GUIDE MANUAL FOR EACH TYPE OF SURFACE OR ROOF SYSTEM."
  * "RMI-FLEX VAPOR BARRIER-FLASHING COAT. EXTEND TO INTERIOR OF CURB." — up the curb, over the top, down inside.
  * "RMI-THANE / RMI WHITE" over the Flex, the same extent.
  * "(E) LIFT AND RESET UNIT AFTER RMI SYSTEM HAS FULLY CURED. FASTEN WITH STAINLESS STEEL SCREWS W/EPDM WASHERS." —
    the screw goes through the unit's downturned flange into the curb: that flange is the counterflashing CS13-1-8-3D
    labels ("REFERENCE ITEM 8. COUNTERFLASHING", with a kicked-out drip at its foot). It belongs to the unit, so it lifts
    with it (named existing__unit_*).
  * Note 7: applies to all curb-mounted units that can be lifted, INCLUDING VENTS, DUCTS, ... HVAC, ... ACCESS HATCH,
    SMOKE HATCH, SKYLIGHTS DOMES.
CS-15-MP (CURB MOUNTED UNITS (FIXED) – METAL ROOF PANEL, 11/05/24), VERIFIED, from the drawing:
  * The unit is not lifted. "REMOVE (E) FASTENERS AND FASTEN SKIRT METAL WITH STAINLESS STEEL SCREWS W/ EPDM WASHERS."
  * "24 GA. SKIRT METAL. EXTEND A MIN. 4" OVER RMI SYSTEM." — new skirt, kicked out at its foot like the counterflashing.
  * "RMI-FLEX VAPOR BARRIER-FLASHING COAT. EXTEND TO UNDERSIDE OF (E) VERTICAL METAL ENCAPSULATING (E) FLASHING." — the
    Flex stops under the unit's (E) vertical metal; it does not go over the top.
  * RMI-THANE, RMI WHITE over the Flex. Note 7 names ACCESS HATCH, SMOKE HATCH among the fixed units.

NOT ON EITHER SHEET — ASSUMED: neither 2D sheet nor any of the four CS13 concept renders draws the roof panel. How the curb
meets the panel is therefore ASSUMED, drawn the usual way on a metal building: the curb walls are notched over the ribs, so
the ribs run on UNDER the curb and on AROUND it up- and down-slope; the curb walls are plumb and its top level (the unit
has to sit level), so the curb is taller on its down-slope side; the Flex runs 18" out onto the panel (the CS-1 figure),
following every rib, and where that edge lands on a rib it carries on over it to 2" past its base (the F-8-TYP lap
figure). Also ASSUMED: every size — the curb (2" insulated double-skin wall, as CS13-1-8-3D draws it), its height, the 3"
turn-down inside, the 4" counterflashing drop and its 3/4" kick, screws at 12" o.c. 2" below the top, the coat thicknesses.

The panel patch is built in the PANEL frame (x across the ribs, y up-slope, z the panel normal — the loader maps Blender
+y to slope-local -z) from the SAME numbers as the app's slope (LAP / lapProfile, SEAM / SHELL, the rib topcoat trapezoid,
the 0.36" field topcoat, the purlin fastener rows), so the bay edges meet the slope flush. The curb and the unit are built
in the LEVEL frame (z plumb, y horizontal up-slope) and turned onto the slope at the end.

Usage from a unit script:

    from rmi_metal_curb import Variant, build
    V = Variant(surface="rpanel", pitch=1, ...)
    build(V, unit=lambda C: ...add the unit in the level frame at C.top...)
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Matrix, Vector
from rmi_blender import IN, M, box, cyl, link, helper, cut, reset_scene, finalize

M2FT = 3.28084

# ---------------------------------------------------------------- the slope this splices into (must match index.html)
RP_PITCH, RP_B, RP_T, RP_H = 12.0, 6.6, 3.0, 1.32     # R-panel: rib every 12", trap(0.55,0.25,0.11) ft  (LAP.B/T/H)
LAP_TP, LAP_TF, LAP_TT, LAP_FOOT = 0.08, 0.30, 0.36, 2.0   # LAP coats and the 2" foot past the rib base (lapProfile)
RIBO = (7.44, 3.84, 1.68)                              # topcoat over a plain rib: trap(0.62,0.32,0.14) ft (ribsO)
SS_PITCH = 24.0                                        # standing seam every 24"
SEAM = [(-0.07, 0), (-0.07, 0.2), (-0.13, 0.2), (-0.13, 0.26), (0.13, 0.26), (0.13, 0.2), (0.07, 0.2), (0.07, 0)]   # ft
SHELLS = [(0.03, 0.26), (0.06, 0.30), (0.10, 0.34)]    # SHELL(o, f) for primer / Flex / topcoat, ft
LIFT = [0.018, 0.024, 0.036]                           # the app floats its rib overlays 0.0015/0.002/0.003 ft off the pan
FIELD_TT = 0.36                                        # field topcoat = the app's 0.03-ft overlay plane
FAST = dict(r=0.312, h=0.48, z=1.56, fr=(0.75, 0.846), fz=1.62, tr=(0.846, 0.942), tz=1.68)   # purlin fastener + dabs (s.fast/fastF/fastO)
SHEET_T = 0.05                                         # pan thickness as drawn (24 ga. exaggerated, as the lap model)

# ---------------------------------------------------------------- the curb (inches; ASSUMED unless noted)
WT = 2.0                  # insulated double-skin metal curb wall (CS13-1-8-3D draws the insulation between the skins)
APRON_IN = 18.0           # Flex out onto the panel past the curb (the CS-1 figure) — then over any rib it lands on
RETURN_IN = 3.0           # "EXTEND TO INTERIOR OF CURB" (CS-13-MP, VERIFIED) — how far down inside is ASSUMED
CURB_COAT = [0.06, 0.26, 0.46]    # primer / Flex / topcoat outer offsets on the curb (visual)
APRON_T = [LAP_TP, LAP_TP + LAP_TF, LAP_TP + LAP_TF + LAP_TT]       # apron coat tops on a flat pan: 0.08 / 0.38 / 0.74"
CF_DROP, CF_KICK, CF_GAP, CF_T = 4.0, 0.75, 0.12, 0.06    # counterflashing: drop, kick-out, stand-off past the topcoat, sheet
SCREW_PITCH, SCREW_DOWN = 12.0, 2.0                       # SS screws w/ EPDM washers, o.c. and below the curb top
LIFT_IN = 14.0                                            # built lifted this far; the app seats it (SLOPE_BAY[kind].lift in index.html).
                                                          # 6" on the CS-1 curbs, but here the 4" counterflashing would hide the gap


class Variant:
    """One model: surface ('rpanel' | 'sseam'), pitch (rise per 12), the curb (CW across the ribs, CD along the slope,
    CH its height at the centre above the pan, all inches), the bay half-sizes (ft), where the laps and purlin rows fall.
    `lap_phase` (ft): a rib at offset o from the bay centre is an R-panel lap when (o + lap_phase) % 3 == 0 — that is
    (x + L/2 - 0.5) % 3 for the unit's slope x on a building L ft long. `rows` (inches, +up-slope): purlin fastener rows
    inside the bay (R-panel only). `liftable`: CS-13-MP (True) or CS-15-MP (False)."""
    def __init__(self, name, surface, pitch, CW, CD, CH, hx, hz, lap_phase=0.0, rows=(), liftable=True, rust=()):
        self.name, self.surface, self.pitch = name, surface, pitch
        self.CW, self.CD, self.CH, self.hx, self.hz = CW, CD, CH, hx, hz
        self.lap_phase, self.rows, self.liftable, self.rust = lap_phase, list(rows), liftable, list(rust)
        self.A = math.atan(pitch / 12.0)


# ---------------------------------------------------------------- mesh helpers
def _mesh(name, layer, verts, faces, mat):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.validate()
    o = bpy.data.objects.new(name, me); o.data.materials.append(mat)
    return link(o, layer, name)


def _ccw(poly):
    a = sum(p[0] * q[1] - q[0] * p[1] for p, q in zip(poly, poly[1:] + poly[:1]))
    return poly if a > 0 else poly[::-1]


def prism(name, layer, poly, y0, y1, mat, lift=0.0, caps=(True, True)):
    """Closed (x, z) polygon in INCHES extruded along Blender y from y0 to y1 (inches), lifted by `lift`. caps=(False, ...)
    leaves an end open: a rib or rib coat that butts the app's own run at the bay edge would show a hairline there."""
    poly = _ccw(poly); n = len(poly)
    v = [(x * IN, y0 * IN, (z + lift) * IN) for x, z in poly] + [(x * IN, y1 * IN, (z + lift) * IN) for x, z in poly]
    f = [(i, n + i, n + (i + 1) % n, (i + 1) % n) for i in range(n)]
    if caps[0]:
        f.append(tuple(range(n)))                       # faces -y
    if caps[1]:
        f.append(tuple(range(2 * n - 1, n - 1, -1)))    # faces +y
    return _mesh(name, layer, v, f, mat)


def rtube(name, layer, bot, top, z0, z1, mat):
    """Rectangular hollow tube (or a sloped band when the rings differ): bot/top = (ox, oy, ix, iy) half-sizes of the
    outer and inner rectangles at z0 and z1 (metres). A counterflashing kick is a tube whose bottom ring is wider."""
    def ring(hx, hy, z):
        return [(-hx, -hy, z), (hx, -hy, z), (hx, hy, z), (-hx, hy, z)]
    v = ring(bot[0], bot[1], z0) + ring(top[0], top[1], z1) + ring(bot[2], bot[3], z0) + ring(top[2], top[3], z1)
    O0, O1, I0, I1 = 0, 4, 8, 12; f = []
    for i in range(4):
        j = (i + 1) % 4
        f += [(O0 + i, O0 + j, O1 + j, O1 + i), (I0 + j, I0 + i, I1 + i, I1 + j),
              (O1 + i, O1 + j, I1 + j, I1 + i), (O0 + i, I0 + i, I0 + j, O0 + j)]
    return _mesh(name, layer, v, f, mat)


def ring_tube(name, layer, ox, oy, ix, iy, z0, z1, mat):
    return rtube(name, layer, (ox, oy, ix, iy), (ox, oy, ix, iy), z0, z1, mat)


def half_torus(name, layer, R, r, x0, z0, mat, seg=24, rings=16):
    """A 180-degree bend in the x-z plane: from the top of a vertical duct at (x0, z0) over to (x0 + 2R, z0), open ends."""
    v, f = [], []
    for i in range(seg + 1):
        p = math.pi * i / seg
        c = (x0 + R - R * math.cos(p), 0.0, z0 + R * math.sin(p)); n1 = (math.cos(p), 0.0, -math.sin(p))
        for k in range(rings):
            t = 2 * math.pi * k / rings
            v.append((c[0] + r * math.cos(t) * n1[0], r * math.sin(t), c[2] + r * math.cos(t) * n1[2]))
    for i in range(seg):
        for k in range(rings):
            l = (k + 1) % rings
            f.append((i * rings + k, i * rings + l, (i + 1) * rings + l, (i + 1) * rings + k))
    o = _mesh(name, layer, v, f, mat)
    for p in o.data.polygons:
        p.use_smooth = True
    return o


# ---------------------------------------------------------------- the panel and its coats (panel frame, inches)
def rib_xs(off):
    """x of the +x R-panel rib side offset outward by `off`, as a function of height (lapProfile in index.html)."""
    hw, tw, H = RP_B / 2, RP_T / 2, RP_H
    ln = math.hypot(tw - hw, H); nx, ny = H / ln, (hw - tw) / ln
    p0 = (hw + off * nx, off * ny); p1 = (tw + off * nx, H + off * ny)
    return lambda y: p0[0] + (y - p0[1]) * (p1[0] - p0[0]) / (p1[1] - p0[1])


def lap_profile(off, foot):
    """LP(off, foot) — the coat over an R-panel lap rib (index.html lapProfile), closed along z=0, inches."""
    xs = rib_xs(off); H = RP_H
    right = [(foot, 0.0), (foot, off), (xs(off), off), (xs(H + off), H + off)]
    return [(-x, y) for x, y in reversed(right)] + right


def shell_outline(o, f):
    """Top outline of SHELL(o, f) — the coat over a standing seam (index.html) — from the left foot to the right, inches."""
    r = [(0.16 + f, 0.03 + o), (0.12 + o, 0.03 + o), (0.12 + o, 0.20), (0.18 + o, 0.20), (0.18 + o, 0.31 + o)]
    return [(-x * 12, z * 12) for x, z in r] + [(x * 12, z * 12) for x, z in reversed(r)]


def shell(o, f):
    """SHELL(o, f) as a closed polygon, closed along z=0, inches."""
    out = shell_outline(o, f)
    return [(out[0][0], 0.0)] + out + [(out[-1][0], 0.0)]


def rib_coat(V, k, lap):
    """Closed (x, z) polygon of coat k (0 primer, 1 Flex, 2 topcoat) over one rib, centred on it; None where the app draws
    nothing (primer and Flex on a plain R-panel rib — only laps carry them)."""
    if V.surface == "sseam":
        return shell(*SHELLS[k])
    if lap:
        off = APRON_T[k]; foot = RP_B / 2 + LAP_FOOT + (LAP_TF if k >= 1 else 0) + (LAP_TT if k >= 2 else 0)
        return lap_profile(off, foot)
    if k == 2:
        b, t, h = RIBO; return [(-b / 2, 0), (-t / 2, h), (t / 2, h), (b / 2, 0)]
    return None


def rib_foot(V, k):
    """Half-width of coat k's footprint over one rib (inches)."""
    if V.surface == "sseam":
        return (0.16 + SHELLS[k][1]) * 12
    return RP_B / 2 + LAP_FOOT + (LAP_TF if k >= 1 else 0) + (LAP_TT if k >= 2 else 0)


def rib_offsets(V):
    """Rib (R-panel) or seam (standing seam) centres inside the bay, inches from its centre."""
    X = V.hx * 12; p = RP_PITCH if V.surface == "rpanel" else SS_PITCH
    # R-panel ribs sit on the half-foot (unit at a whole-foot x); seams sit on odd feet: at the centre when the
    # bay is an odd number of feet wide each side (x odd), 12" off it when even
    o0 = 6.0 if V.surface == "rpanel" else (0.0 if V.hx % 2 == 1 else 12.0)
    out, o = [], o0
    while o < X:
        out.append(o); o += p
    o = o0 - p
    while o > -X:
        out.append(o); o -= p
    return sorted(out)


def is_lap(V, o):
    """Standing seam: every seam is a lap. R-panel: every third rib (index.html s.laps)."""
    if V.surface == "sseam":
        return True
    m = (o / 12 + V.lap_phase) % 3
    return min(m, 3 - m) < 1e-6


def apron_top(V, k, x0, x1, ribs):
    """Closed (x, z) section of apron coat k from x0 to x1 (inches): flat on the pans, over every rib in between."""
    top = [(x0, APRON_T[k])]
    for r in ribs:
        if not (x0 < r < x1):
            continue
        if V.surface == "rpanel":
            off = APRON_T[k]; xs = rib_xs(off)
            top += [(r - xs(off), off), (r - xs(RP_H + off), RP_H + off), (r + xs(RP_H + off), RP_H + off), (r + xs(off), off)]
        else:
            pts = shell_outline(*SHELLS[k]); t = APRON_T[k]
            top += [(r + pts[0][0], t)] + [(r + x, z) for x, z in pts] + [(r + pts[-1][0], t)]
    top.append((x1, APRON_T[k]))
    return top + [(x1, 0.0), (x0, 0.0)]


def panel_top(V, x0, x1, ribs):
    """Top outline of the bare panel from x0 to x1 — the cutter that notches the curb walls over the ribs."""
    pts = [(x0, 0.0)]
    for r in ribs:
        if V.surface == "rpanel":
            pts += [(r - RP_B / 2, 0.0), (r - RP_T / 2, RP_H), (r + RP_T / 2, RP_H), (r + RP_B / 2, 0.0)]
        else:
            w, h = 0.13 * 12 + 0.05, 0.26 * 12 + 0.02          # the seam's outer silhouette (cap width, full height)
            pts += [(r - w, 0.0), (r - w, h), (r + w, h), (r + w, 0.0)]
    pts.append((x1, 0.0))
    return pts


LAYERS3 = [("primer", "primer"), ("flex", "flex"), ("topcoat", "thane")]


def apron_extents(V, ribs, ax_nom, ay_nom):
    """Per-coat half-extents of an apron (inches): nominal, carried over a rib the x-edge lands on (to 2" past the rib
    base, as at a lap), each coat nesting outside the last."""
    ax0 = ax_nom
    for r in ribs:
        if abs(ax0 - abs(r)) < rib_foot(V, 0):
            ax0 = max(ax0, abs(r) + rib_foot(V, 0) + 0.05)
    grow = [0.0, LAP_TF, LAP_TF + LAP_TT]
    AX, AY = [ax0 + g for g in grow], [ay_nom + g for g in grow]
    X, Y = V.hx * 12, V.hz * 12
    assert AX[2] < X - 0.02 and AY[2] < Y - 0.02, f"apron {AX[2]:.2f} x {AY[2]:.2f} in does not fit the bay {X} x {Y}"
    return AX, AY


def panel_patch(V, ribs, AX, AY, cx_in=0.0, cy_in=0.0, keep_out=lambda x, y: False):
    """The bay of panel in the PANEL frame (inches in, metres out): pan, ribs, purlin fasteners with their Flex / topcoat
    dabs (R-panel rows, except where keep_out(x, y)), rust, the 0.36" field topcoat, the rib coats from the bay edges in
    to the apron, and the apron itself — four strips round an inner rectangle (cx_in, cy_in) whose edges are buried in
    whatever stands there, or one sheet when there is none."""
    X, Y = V.hx * 12, V.hz * 12
    box("panel", "existing", 2 * X * IN, 2 * Y * IN, SHEET_T * IN, 0, 0, -SHEET_T / 2 * IN, M("panel"))
    for i, r in enumerate(ribs):
        prof = ([(r - RP_B / 2, 0), (r - RP_T / 2, RP_H), (r + RP_T / 2, RP_H), (r + RP_B / 2, 0)] if V.surface == "rpanel"
                else [(r + x * 12, z * 12) for x, z in SEAM])
        prism(f"rib_{i}", "existing", prof, -Y, Y, M("panel"), caps=(False, False))
    if V.surface == "rpanel":
        for j, y in enumerate(V.rows):
            for i, r in enumerate(ribs):
                if keep_out(r, y):
                    continue
                cyl(f"fastener_{j}_{i}", "existing", FAST["r"] * IN, FAST["h"] * IN, r * IN, y * IN, FAST["z"] * IN, M("fast"), verts=10)
                cyl(f"flex_dab_{j}_{i}", "flex", FAST["fr"][1] * IN, FAST["h"] * IN, r * IN, y * IN, FAST["fz"] * IN, M("flex"), verts=14, r2=FAST["fr"][0] * IN)
                cyl(f"topcoat_dab_{j}_{i}", "topcoat", FAST["tr"][1] * IN, FAST["h"] * IN, r * IN, y * IN, FAST["tz"] * IN, M("thane"), verts=14, r2=FAST["tr"][0] * IN)
    for i, (x, y, rr) in enumerate(V.rust):
        cyl(f"rust_{i}", "existing", rr * IN, 0.01 * IN, x * IN, y * IN, 0.006 * IN, M("rust"), verts=20)
    t = FIELD_TT
    fields = ({"up": (-X, X, cy_in, Y), "dn": (-X, X, -Y, -cy_in), "l": (-X, -cx_in, -cy_in, cy_in), "r": (cx_in, X, -cy_in, cy_in)}
              if cy_in > 0 else {"all": (-X, X, -Y, Y)})
    for nm, (x0, x1, y0, y1) in fields.items():
        box(f"topcoat_field_{nm}", "topcoat", (x1 - x0) * IN, (y1 - y0) * IN, t * IN, (x0 + x1) / 2 * IN, (y0 + y1) / 2 * IN, t / 2 * IN, M("thane"))
    for i, r in enumerate(ribs):
        lap = is_lap(V, r)
        for k, (layer, mat) in enumerate(LAYERS3):
            poly = rib_coat(V, k, lap)
            if poly is None:
                continue
            poly = [(r + x, z) for x, z in poly]
            if abs(r) + rib_foot(V, k) < AX[k] - 0.01:
                prism(f"{layer}_rib_{i}_up", layer, poly, AY[k], Y, M(mat), LIFT[k], caps=(False, False))
                prism(f"{layer}_rib_{i}_dn", layer, poly, -Y, -AY[k], M(mat), LIFT[k], caps=(False, False))
            else:
                prism(f"{layer}_rib_{i}", layer, poly, -Y, Y, M(mat), LIFT[k], caps=(False, False))
    for k, (layer, mat) in enumerate(LAYERS3):
        full = apron_top(V, k, -AX[k], AX[k], ribs)
        if cy_in <= 0:
            prism(f"{layer}_apron", layer, full, -AY[k], AY[k], M(mat), LIFT[k])
            continue
        prism(f"{layer}_apron_up", layer, full, cy_in, AY[k], M(mat), LIFT[k])
        prism(f"{layer}_apron_dn", layer, full, -AY[k], -cy_in, M(mat), LIFT[k])
        prism(f"{layer}_apron_r", layer, apron_top(V, k, cx_in, AX[k], ribs), -cy_in, cy_in, M(mat), LIFT[k])
        prism(f"{layer}_apron_l", layer, apron_top(V, k, -AX[k], -cx_in, ribs), -cy_in, cy_in, M(mat), LIFT[k])


def panel_cutter(V, ribs, lift=0.0, name="wall_cutter"):
    """Helper: everything below the panel's top surface (raised by `lift`) — plumb parts cut by it stop ON the panel,
    notched over the ribs."""
    X, Y = V.hx * 12, V.hz * 12
    under = [(x, z + lift) for x, z in panel_top(V, -X - 12, X + 12, ribs)] + [(X + 12, -80.0), (-X - 12, -80.0)]
    return helper(prism(name, "existing", under, -Y - 12, Y + 12, M("panel")))


def level_to_panel(A, objs):
    """Turn objects built in the LEVEL frame (z plumb, y horizontal up-slope) onto the panel (rotate -A about x)."""
    bpy.context.view_layer.update()
    R = Matrix.Rotation(-A, 4, 'X')
    for o in objs:
        o.matrix_world = R @ o.matrix_world


class Curb:
    """What a unit script gets: numbers in the LEVEL frame (metres) plus the angle."""
    pass


def build(V, unit, finalize_name=None):
    reset_scene()
    A = V.A; tanA, cosA = math.tan(A), math.cos(A)
    ribs = rib_offsets(V)
    level = []                                        # objects built in the level frame, turned onto the slope at the end
    unit_objs = []

    # the curb's footprint on the panel (plumb walls meet a pan at y = a / cos A)
    cy_out = V.CD / 2 / cosA                         # outer face, along the slope
    cy_in = (V.CD / 2 - WT / 2) / cosA               # mid-wall: coat and slab edges stop here, buried in the wall
    cx_in = V.CW / 2 - WT / 2
    # apron: 18" past the curb, carried over a rib it lands on; purlin fasteners on the crests, not under the curb
    AX, AY = apron_extents(V, ribs, V.CW / 2 + APRON_IN, cy_out + APRON_IN)
    panel_patch(V, ribs, AX, AY, cx_in, cy_in, keep_out=lambda x, y: abs(x) < V.CW / 2 + 3 and abs(y) < cy_out + 3)
    cutter = panel_cutter(V, ribs)
    LAYER = LAYERS3

    # ================================================================ the curb (level frame, metres)
    C = Curb()
    C.A, C.top = A, V.CH * IN
    C.hx, C.hy = V.CW / 2 * IN, V.CD / 2 * IN
    C.ix, C.iy = (V.CW / 2 - WT) * IN, (V.CD / 2 - WT) * IN
    z_low = -(V.CD / 2 + 4) * tanA * IN - 4 * IN        # below the panel everywhere under the curb; the cutter trims it
    C.z_low = z_low
    wall = ring_tube("curb_wall", "existing", C.hx, C.hy, C.ix, C.iy, z_low, C.top, M("curb")); cut(wall, cutter); level.append(wall)
    plate = box("curb_interior", "existing", 2 * C.ix, 2 * C.iy, 0.2 * IN, 0, 0, C.top - (RETURN_IN + 1.0) * IN, M("unitD")); level.append(plate)

    # coats on the curb: up the outside from the panel; CS-13-MP over the top and down inside, CS-15-MP only to the
    # underside of the (E) vertical metal (the unit script says where that is: C.coat_top)
    C.coat_top = C.top if V.liftable else None
    C.cut, C.level, C.unit_objs, C.ring_tube, C.rtube = cutter, level, unit_objs, ring_tube, rtube
    C.coat = [c * IN for c in CURB_COAT]

    def coats(coat_top):
        inner = (C.hx, C.hy)
        for k, (layer, mat) in enumerate(LAYER):
            o = C.coat[k]
            w = ring_tube(f"{layer}_curb_wrap", layer, C.hx + o, C.hy + o, inner[0], inner[1], z_low, coat_top, M(mat))
            cut(w, cutter); level.append(w); inner = (C.hx + o, C.hy + o)
            if V.liftable:   # over the top and RETURN_IN down inside — "EXTEND TO INTERIOR OF CURB"
                level.append(ring_tube(f"{layer}_curb_cap", layer, C.hx + o, C.hy + o, C.ix - o, C.iy - o,
                                       C.top - RETURN_IN * IN, C.top + o, M(mat)))
    C.coats = coats
    if V.liftable:
        coats(C.top)

    # ================================================================ the unit (the script's own)
    unit(C)

    # ================================================================ onto the slope
    level_to_panel(A, level + unit_objs)
    if V.liftable:                                   # build seated, ship lifted: the app seats it LIFT_IN along the panel normal
        for o in unit_objs:
            o.location += Vector((0, 0, LIFT_IN * IN))
    report(V, C, AX, AY)
    return finalize(finalize_name or V.name)


def counterflashing(C, name="unit_counterflashing", solid_top=False):
    """CS-13-MP / CS13-1-8-3D counterflashing: top leg over the coated curb top, a 4" drop down the outside and a kick-out
    at the foot. It is the unit's own flange, so it is named existing__unit_* and lifts with the unit. Returns the top of
    its top leg (where the unit body sits) and the outside face (where the screws go)."""
    tc = C.coat[2]
    ox, oy = C.hx + tc + CF_GAP * IN, C.hy + tc + CF_GAP * IN      # inside of the drop
    t = CF_T * IN
    z_top = C.top + tc                                             # on the topcoat cap
    objs = []
    ix, iy = (C.ix - tc, C.iy - tc) if not solid_top else (0.001, 0.001)
    if solid_top:
        objs.append(box(f"{name}_top", "existing", 2 * (ox + t), 2 * (oy + t), t, 0, 0, z_top + t / 2, M("coping")))
    else:
        objs.append(C.ring_tube(f"{name}_top", "existing", ox + t, oy + t, ix, iy, z_top, z_top + t, M("coping")))
    z0 = C.top - CF_DROP * IN
    objs.append(C.ring_tube(f"{name}_drop", "existing", ox + t, oy + t, ox, oy, z0, z_top + t, M("coping")))
    k = CF_KICK * IN
    objs.append(C.rtube(f"{name}_kick", "existing", (ox + t + k, oy + t + k, ox + k, oy + k), (ox + t, oy + t, ox, oy),
                        z0 - k * 0.8, z0, M("coping")))
    C.unit_objs.extend(objs)
    return z_top + t, (ox + t, oy + t)


def screws(C, face, z, name, layer="existing", pitch=SCREW_PITCH, washer=True):
    """Stainless screws with EPDM washers through a flange at height z, `pitch` o.c. along every face, pointing into the
    curb. face = (hx, hy) of the flange's outside. Returns the objects (the caller files them as unit / level)."""
    objs = []
    fx, fy = face
    parts = ([("washer", 0.3125, 0.08, 0.04, "rubber", 16)] if washer else []) + [("head", 0.19, 0.2, 0.18, "fast", 6)]
    for side, (nx, ny) in enumerate(((0, 1), (1, 0), (0, -1), (-1, 0))):
        half = fx if ny else fy                      # the run along this face
        n = max(0, int((2 * half / IN - 8) // pitch))
        rot = (1.5708, 0, 0) if ny else (0, 1.5708, 0)
        for i in range(n + 1):
            s = (i - n / 2) * pitch * IN
            for part, r, h, off, mat, verts in parts:
                px = nx * (fx + off * IN) + (s if ny else 0)
                py = ny * (fy + off * IN) + (s if nx else 0)
                o = cyl(f"{name}_{part}_{side}_{i}", layer, r * IN, h * IN, px, py, z, M(mat), verts=verts)
                o.rotation_euler = rot; objs.append(o)
    return objs


def report(V, C, AX, AY):
    print(f"\n{V.name}: {V.surface}, {V.pitch}:12, curb {V.CW:.0f} x {V.CD:.0f} in, {V.CH:.1f} in high at the centre "
          f"({V.CH - V.CD / 2 * math.tan(V.A):.1f} up-slope / {V.CH + V.CD / 2 * math.tan(V.A):.1f} down-slope)")
    print(f"  bay {2 * V.hx} x {2 * V.hz} ft (SLOPE_BAY hx {V.hx}, hz {V.hz}); Flex apron to {AX[1] / 12:.2f} x {AY[1] / 12:.2f} ft")
