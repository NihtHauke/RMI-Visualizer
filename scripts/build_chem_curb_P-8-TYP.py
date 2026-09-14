"""
build_chem_curb_P-8-TYP.py — chem-curb (pitch pan) around a cluster of penetrations, per RMI detail P-8-TYP
(CHEM-CURB – TYPICAL, 11/05/24) with PP-1-FT-3D (PITCH PANS – CONCEPT DRAWING, 9/1/21) as the 3D reference.

    blender -b --python scripts/build_chem_curb_P-8-TYP.py

What the 2D drawing says (this is the logic the model follows):
  * (E) multiple penetrations through the (E) roof system, "shown for illustration only". Note 7: applies wherever a
    penetration is not circular or a roof jack / single-ply boot is not desired or feasible. Note 8: all (E) BUR,
    mod-bit, EPDM, PVC, TPO and concrete deck systems regardless of deck and insulation.
  * Specified Chem-Curb, fabricated per the manufacturer for overall size and distance from the penetration, installed
    per Chem-Link instructions, set in RMI M-1 sealant (the beads at the base of the curb and of the penetrations).
  * Note 10: clean, prepare and prime per the RMI Specification Guide Manual.
  * Interior pocket filled with RMI-Flex, TAPERED from the penetration outward to shed water.
  * RMI-Flex vapor barrier-flashing coat over the fill and the curb and onto the field, extending a MIN. 4" UP the
    penetration past the Chem-Curb.
  * RMI-Thane / RMI-White extending a MIN. 2" UP the penetration past the RMI-Flex.
PP-1-FT-3D shows an open pan with Flex on the rim and the field and the coating over all — same logic, reference only.
There is no metal flange in either document: the curb sits on the roof in sealant and the Flex runs over it.

What the drawing does NOT say (NOT TO SCALE, no other dimensions), so ASSUMED: curb size, wall and height; the
penetrations themselves; the bead size; how far Flex and topcoat run onto the field; how high the fill rises at a
penetration and how far the taper runs; and the order of curb vs. primer (modelled: curb set in sealant at the prep
stage, primer over it). The (E) roof build-up matches the drain and soil-stack models so they read alike on one roof.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from rmi_blender import IN, M, Shell, helper, cut, link, reset_scene, finalize

# ---------------------------------------------------------------- dimensions (ASSUMED unless marked VERIFIED)
# (E) roof assembly — same heights as lead-soil-stack-P-6-TYP
DECK_Z0, DECK_Z1 = -0.079, -0.064   # steel deck
INSUL_Z1   = 0.000                  # insulation up to the underside of the membrane
MEM_TOP    = 0.003                  # (E) membrane top = the roof surface the app sees at y=0

# Chem-Curb — "fabricated per mfg. requirements for overall size and distance from penetration"
CURB_HX, CURB_HY = 15.0 * IN, 8.0 * IN   # outside half-sizes: 30" x 16"
CURB_T     = 0.5 * IN               # wall
CURB_H     = 4.0 * IN               # height above the roof

# (E) penetrations — "shown for illustration only". (x, y, OD, ID, height above roof, material); ID 0 = solid.
# Every one sits on or near y=0 so a section through the curb's long axis cuts them, as the drawing's section does.
PIPES = [
    (-9.0,  0.0, 3.5,   3.0, 30.0, "castiron"),   # 3" vent
    (-2.5,  3.5, 1.9,   0.0, 24.0, "curb"),       # 1-1/2" conduit
    ( 3.5,  0.0, 2.375, 0.0, 26.0, "curb"),       # 2" line
    ( 9.5, -3.0, 1.9,   0.0, 24.0, "curb"),       # 1-1/2" conduit
]
PIPE_DOWN  = 10.0 * IN              # below the deck, so the section view shows them passing through

BEAD       = 0.375 * IN             # RMI M-1 sealant bead at the base of the curb (inside and out) and of each penetration

# Flex fill: level with the curb top at the wall, rising toward each penetration — "tapered from penetration outward"
FILL_RISE  = 0.75 * IN              # extra height at the face of a penetration
FILL_TAPER = 4.0 * IN               # distance over which it falls back to the wall level
GRID       = 0.5 * IN               # fill surface mesh spacing

COAT       = 0.001                  # visual thickness per layer (1 mm), same as the drain and soil stack
FLEX_UP    = 5.0 * IN               # VERIFIED P-8-TYP: Flex min 4" up the penetration past the curb (5" modelled)
TOP_UP     = 2.5 * IN               # VERIFIED P-8-TYP: topcoat min 2" up past the Flex (2.5" modelled)
FIELD      = {"primer": 6.0 * IN, "flex": 6.0 * IN, "topcoat": 7.0 * IN}   # out onto the field from the curb face
PATCH_X    = CURB_HX + FIELD["topcoat"] + 2.0 * IN     # roof patch half-sizes: 48" x 34"
PATCH_Y    = CURB_HY + FIELD["topcoat"] + 2.0 * IN

# ---------------------------------------------------------------- derived
CURB_TOP   = MEM_TOP + CURB_H
IX, IY     = CURB_HX - CURB_T, CURB_HY - CURB_T      # inside face of the curb
FLEX_TOP   = CURB_TOP + FLEX_UP
TOP_TOP    = FLEX_TOP + TOP_UP
PIPES      = [(x * IN, y * IN, od * IN / 2, idia * IN / 2, up * IN, m) for (x, y, od, idia, up, m) in PIPES]   # → metres, radii


def rect(hx, hy):
    return [(hx, -hy), (hx, hy), (-hx, hy), (-hx, -hy)]          # counter-clockwise from above


def ring(s, ox, oy, ix, iy, z0, z1):
    """Rectangular annular prism (ix=0 → solid box) into Shell s. Same winding as Shell.tube."""
    n = len(s.v); O, k = rect(ox, oy), 4
    s.v += [(x, y, z0) for x, y in O] + [(x, y, z1) for x, y in O]
    O0, O1 = n, n + k
    if ix <= 0:
        C0, C1 = n + 2 * k, n + 2 * k + 1; s.v += [(0, 0, z0), (0, 0, z1)]
    else:
        I = rect(ix, iy); I0, I1 = n + 2 * k, n + 3 * k
        s.v += [(x, y, z0) for x, y in I] + [(x, y, z1) for x, y in I]
    for i in range(k):
        j = (i + 1) % k
        s.f.append((O0 + i, O0 + j, O1 + j, O1 + i))
        if ix <= 0:
            s.f.append((C1, O1 + i, O1 + j)); s.f.append((C0, O0 + j, O0 + i))
        else:
            s.f.append((I0 + j, I0 + i, I1 + i, I1 + j))
            s.f.append((O1 + i, O1 + j, I1 + j, I1 + i))
            s.f.append((O0 + i, I0 + i, I0 + j, O0 + j))
    return s


def shifted(s, x, y, build):
    """Run a Shell builder at the origin, then move what it added to (x, y)."""
    n = len(s.v); build(s)
    s.v[n:] = [(vx + x, vy + y, vz) for vx, vy, vz in s.v[n:]]
    return s


_cutters = {}
def cutter(x, y, r):
    key = (round(x, 5), round(y, 5), round(r, 5))
    if key not in _cutters:
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=1.0, location=(x, y, 0), vertices=64)
        _cutters[key] = helper(bpy.context.object)       # no material: it would paint the hole faces
    return _cutters[key]


def punch(o, dr):
    """Cut every penetration out of o, at the pipe radius + dr."""
    for (x, y, r, _, _, _) in PIPES:
        cut(o, cutter(x, y, r + dr))
    return o


def fill_height(x, y):
    t = 0.0
    for (px, py, r, _, _, _) in PIPES:
        u = min(1.0, max(0.0, 1.0 - (math.hypot(x - px, y - py) - r) / FILL_TAPER))
        t = max(t, u * u * (3 - 2 * u))
    return CURB_TOP + COAT + FILL_RISE * t


def slab(layer, name, material, hx, hy, zb, zt):
    """Closed slab over the pocket whose bottom and top follow zb(x, y) / zt(x, y)."""
    nx, ny = max(2, round(2 * hx / GRID)), max(2, round(2 * hy / GRID))
    xs = [-hx + 2 * hx * i / nx for i in range(nx + 1)]; ys = [-hy + 2 * hy * j / ny for j in range(ny + 1)]
    W = nx + 1; off = W * (ny + 1)
    T = lambda i, j: j * W + i
    B = lambda i, j: off + j * W + i
    v = [(x, y, zt(x, y)) for y in ys for x in xs] + [(x, y, zb(x, y)) for y in ys for x in xs]
    f = []
    for j in range(ny):
        for i in range(nx):
            f.append((T(i, j), T(i + 1, j), T(i + 1, j + 1), T(i, j + 1)))
            f.append((B(i, j), B(i, j + 1), B(i + 1, j + 1), B(i + 1, j)))
    for i in range(nx):
        f.append((B(i, 0), B(i + 1, 0), T(i + 1, 0), T(i, 0)))
        f.append((B(i + 1, ny), B(i, ny), T(i, ny), T(i + 1, ny)))
    for j in range(ny):
        f.append((B(0, j + 1), B(0, j), T(0, j), T(0, j + 1)))
        f.append((B(nx, j), B(nx, j + 1), T(nx, j + 1), T(nx, j)))
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], f); me.validate()
    for p in me.polygons:
        p.use_smooth = abs(p.normal.z) > 0.5       # the tapered surface smooth, the edges crisp
    o = bpy.data.objects.new(name, me); o.data.materials.append(material)
    return link(o, layer, name)


def coating(layer, i, material):
    """One coat as nested shells: field → cove over the bead → up the curb → over its top → up each penetration.
    i = 1 primer, 2 Flex, 3 topcoat (each one COAT further out)."""
    d0, d1 = (i - 1) * COAT, i * COAT
    s = Shell()
    ring(s, CURB_HX + FIELD[layer], CURB_HY + FIELD[layer], CURB_HX + d0, CURB_HY + d0, MEM_TOP + d0, MEM_TOP + d1)
    ring(s, CURB_HX + BEAD + d1, CURB_HY + BEAD + d1, CURB_HX + d0, CURB_HY + d0, MEM_TOP + d0, MEM_TOP + BEAD + d1)
    ring(s, CURB_HX + d1, CURB_HY + d1, CURB_HX + d0, CURB_HY + d0, MEM_TOP + d0, CURB_TOP + d1)
    ring(s, CURB_HX + d1, CURB_HY + d1, IX - d1, IY - d1, CURB_TOP + d0, CURB_TOP + d1)
    top = {"primer": FLEX_TOP, "flex": FLEX_TOP, "topcoat": TOP_TOP}[layer]
    z0 = {"primer": MEM_TOP, "flex": MEM_TOP + COAT, "topcoat": CURB_TOP}[layer]   # the flex and topcoat starts sit inside the fill
    for (x, y, r, _, _, _) in PIPES:
        shifted(s, x, y, lambda sh: sh.tube(r + d1, r + d0, z0, top))
    if layer == "primer":   # primer down the inside of the curb and across the pocket floor, before the fill
        ring(s, IX - d0, IY - d0, IX - d1, IY - d1, MEM_TOP, CURB_TOP + d1)
    s.emit(layer, "coat", material)
    if layer == "primer":
        punch(slab(layer, "pocket_floor", material, IX - COAT, IY - COAT, lambda x, y: MEM_TOP, lambda x, y: MEM_TOP + COAT), 0)
    elif layer == "flex":   # the fill IS the flashing coat's surface inside the curb
        punch(slab(layer, "pocket_fill", material, IX - COAT, IY - COAT, lambda x, y: MEM_TOP + COAT, fill_height), COAT)
    else:
        punch(slab(layer, "over_fill", material, IX - COAT, IY - COAT,
                   lambda x, y: fill_height(x, y), lambda x, y: fill_height(x, y) + COAT), 2 * COAT)


reset_scene()

# (E) roof assembly with the penetrations punched through
punch(ring(Shell(), PATCH_X, PATCH_Y, 0, 0, DECK_Z0, DECK_Z1).emit("existing", "steel_deck", M("deck")), 0)
punch(ring(Shell(), PATCH_X, PATCH_Y, 0, 0, DECK_Z1, INSUL_Z1).emit("existing", "insulation", M("insulation")), 0)
punch(ring(Shell(), PATCH_X, PATCH_Y, 0, 0, INSUL_Z1, MEM_TOP).emit("existing", "membrane", M("membrane")), 0)

# (E) penetrations
for key in ("castiron", "curb"):
    s = Shell()
    for (x, y, r, ri, up, m) in PIPES:
        if m == key:
            shifted(s, x, y, lambda sh: sh.tube(r, ri, DECK_Z0 - PIPE_DOWN, MEM_TOP + up))
    s.emit("existing", "penetration_" + key, M(key))

# Chem-Curb: new work, set at the prep stage (the "_after_" tag makes the app show it from prep on)
ring(Shell(), CURB_HX, CURB_HY, IX, IY, MEM_TOP, CURB_TOP).emit("existing", "chem_curb_after_prep", M("chemcurb"))

# RMI M-1 sealant: beads at the base of the curb, inside and out, and around each penetration — prep work
seal = Shell()
ring(seal, CURB_HX + BEAD, CURB_HY + BEAD, CURB_HX, CURB_HY, MEM_TOP, MEM_TOP + BEAD)
ring(seal, IX, IY, IX - BEAD, IY - BEAD, MEM_TOP, MEM_TOP + BEAD)
for (x, y, r, _, _, _) in PIPES:
    shifted(seal, x, y, lambda sh: sh.torus(r + BEAD / 2, BEAD / 2, MEM_TOP + BEAD / 2, seg=32, rings=8))
seal.emit("primer", "sealant_m1", M("seal"))

coating("primer", 1, M("primer"))
coating("flex", 2, M("flex"))
coating("topcoat", 3, M("thane"))

finalize("chem-curb-P-8-TYP")
