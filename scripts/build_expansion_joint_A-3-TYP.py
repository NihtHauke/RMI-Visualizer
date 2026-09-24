"""
build_expansion_joint_A-3-TYP.py — expansion joint per RMI detail A-3-TYP (EXPANSION JOINT – TYPICAL, 11/05/24), as drawn:
metal mounting flanges fastened down flat on the (E) roof system either side of the joint, the flexible bellow looped up
between them. There is no 3D concept render for A-3-TYP.

    blender -b --python scripts/build_expansion_joint_A-3-TYP.py

A 4-ft SECTION of the joint. The hospital's code-drawn run (addExpansionJoint in index.html) is a strip of this same
cross-section, built from the same numbers (the EJ constants) — roof strip, flanges, bellow, fasteners and tight coats —
lying in one long hole the app cuts in the field sheets; this model replaces 4 ft of that strip at the hotspot. Keep the
two in step or the seams show. The run lies along Blender Y (the app's z); x = 0 is the joint centre; z = 0 the app's
field plane.

What the drawing says (VERIFIED):
  * (E) METAL & FLEXIBLE BELLOW (notes 10 & 12): metal mounting flanges fastened through the (E) roof system either side
    of the joint, the flexible bellow looped up over the joint between their inner edges. The (E) roof system runs to the
    joint edge under the flanges.
  * Note 8: DETAIL APPLIES TO ALL (E) EPDM, NEOPRENE, PVC, TPO EXPANSION JOINTS REGARDLESS OF INDIVIDUAL CONFIGURATION.
    The insulation and deck are "shown for illustration — actual type and configuration may vary between roof and wall
    applications".
  * CONFIRM BELLOW INTEGRITY. REPAIR OR REPLACE DAMAGED MATERIALS. Note 10: improper or ill-fitting joints may move more
    than the RMI materials allow and void the warranty.
  * REPLACE DAMAGED, LOOSE OR MISSING FASTENERS — shown as one fastener backed out at the existing stage and replaced at
    prep (existing__fastener_before_loose / existing__fastener_after_reset; the app swaps them at prep).
  * Note 12: clean, prepare and prime per the Spec Guide Manual for each (E) roof system, the metal and the flexible bellow.
  * RMI-FLEX VAPOR BARRIER-FLASHING COAT TO FULLY ENCAPSULATE THE EXPANSION JOINT BELLOW, FASTENERS AND MOUNTING FLANGE;
    EXTEND A MIN 2" PAST ASSEMBLY — the coats step over the flange edges onto the roof system. RMI-THANE / RMI-WHITE over
    the Flex. On the hospital's full-field roofs the field coats carry on from there.
  * Note 11: where gaps at the attachment flanges cannot be bridged with Flex, tape or 3-course polyester/Flex min 2" each
    side of the joint, no voids. Conditional, and not drawn on the section, so not modelled.

ASSUMED (the drawing is NOT TO SCALE and gives only the 2" Flex extent): the 4" joint; 4" x 1/16" flanges from the joint
edge; a 3/16" bellow rising 1/2" and looping over the joint (crown 2-1/2" above the flanges, the drawing's proportion);
hex washer-head fasteners mid-flange at 6" o.c.; the roof build-up; the 12" roof strip each side; coat thicknesses.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from rmi_blender import IN, M, box, reset_scene, finalize, link, band, prism_y, smooth_by_angle

# ---------------------------------------------------------------- dimensions (inches; ASSUMED unless noted) — same as EJ in index.html
L        = 48.0                  # modelled section along the joint
GAP      = 4.0                   # joint opening between the deck edges = between the flanges' inner edges (drawing)
MT       = 0.0625                # (E) metal mounting flange (drawing: thin plate each side on the roof system, VERIFIED that it is there)
FLANGE   = 4.0                   # flange width, from the joint edge out
BT       = 0.1875                # bellow wall (drawing: flexible bellow looped over the joint, VERIFIED)
LEG      = 0.5                   # straight bellow leg above the flange before the loop — crown 2.5" up, the drawing's proportion
FAST_Y   = 4.0                   # fastener line from the joint centre (drawing: one fastener mid-flange in section)
FAST_OC  = 6.0                   # fastener spacing along the joint
HEAD_R, HEAD_H, WASH_R, WASH_T, SHANK_R, SHANK_L = 0.22, 0.14, 0.30, 0.04, 0.09, 3.0
LOOSE_X, LOOSE_Y, LOOSE_UP, LOOSE_TILT = -FAST_Y, -3.0, 0.60, 18.0 # the fastener backed out at existing: west flange, app z = +3" (faces the detail camera)
COAT     = 0.04                  # visual thickness per layer (1 mm), as the edge-metal and penthouse runs
LIFT     = 0.01                  # primer's inner face off its substrate: the app's materials are double-sided, so a coincident face z-fights
FIELD    = {"primer": 11.0, "flex": 11.0, "topcoat": 11.2}   # coats onto the roof strip from the joint centre, 5" past the flanges (the app's topcoat hole must clear them)
PATCH    = 12.0                  # roof strip half-width (the app's membrane hole sits 1.2" inside it)
DECK_Z0, DECK_Z1 = -3.1, -2.5    # steel deck, as the other flat-roof models
MEM_T    = 0.1                   # (E) roof system top = 0.1" above the app's field plane, so the two never z-fight
ARC      = 24                    # segments in the bellow loop

# ---------------------------------------------------------------- derived (inches)
CI  = GAP / 2                    # joint edge = flange inner edge = bellow outer leg
FO  = CI + FLANGE                # flange outer edge
FLT = MEM_T + MT                 # flange top
RO, RI = CI, CI - BT             # bellow outer / inner radius
ZC  = FLT + LEG                  # centre of the loop
Y0, Y1 = -L / 2, L / 2


def arc(R, a0, a1):
    return [(R * math.cos(a0 + (a1 - a0) * i / ARC), ZC + R * math.sin(a0 + (a1 - a0) * i / ARC)) for i in range(ARC + 1)]


def mirror(pts):
    return [(-y, z) for y, z in pts]


def coat_path(field):
    """The surface every coat follows, walked with the substrate on the left: roof → over the flange edge → across the
    flange → up the bellow, over the loop, and down the far side to the far roof."""
    right = [(field, MEM_T), (FO, MEM_T), (FO, FLT), (RO, FLT)]
    return right + arc(RO, 0, math.pi) + mirror(right[::-1])


def P(name, layer, pts, mat):
    """Run part: a prism of the (y, z) inch polygon along the section, open at both ends."""
    return prism_y(name, layer, [(y * IN, z * IN) for y, z in pts], mat, Y0 * IN, Y1 * IN)


def B(name, layer, y0, y1, z0, z1, mat):
    """Build-up under the strip: a closed box spanning y0..y1 across, z0..z1 up, the full section length."""
    return box(name, layer, (y1 - y0) * IN, L * IN, (z1 - z0) * IN, (y0 + y1) / 2 * IN, 0, (z0 + z1) / 2 * IN, mat)


class Acc:
    """Accumulates small solids at (x, y) positions into ONE mesh: hex fasteners with washers and shanks, coat domes."""
    def __init__(self):
        self.v, self.f = [], []

    def cyl(self, x, y, z0, z1, r, seg=16):
        n = len(self.v); cs = [(math.cos(2 * math.pi * i / seg), math.sin(2 * math.pi * i / seg)) for i in range(seg)]
        self.v += [(x + r * c, y + r * s, z0) for c, s in cs] + [(x + r * c, y + r * s, z1) for c, s in cs] + [(x, y, z0), (x, y, z1)]
        c0, c1 = n + 2 * seg, n + 2 * seg + 1
        for i in range(seg):
            j = (i + 1) % seg
            self.f += [(n + i, n + j, n + seg + j, n + seg + i), (c1, n + seg + i, n + seg + j), (c0, n + j, n + i)]

    def dome(self, x, y, z0, r, h, seg=20, rings=6):
        """Quarter-ellipse dome (radius r, rise h) standing on z0 — a coat over a fastener head."""
        n = len(self.v)
        for k in range(rings + 1):
            p = (math.pi / 2) * k / rings; rr, zz = r * math.cos(p), z0 + h * math.sin(p)
            for i in range(seg):
                t = 2 * math.pi * i / seg; self.v.append((x + rr * math.cos(t), y + rr * math.sin(t), zz))
        for k in range(rings):
            for i in range(seg):
                j = (i + 1) % seg
                self.f.append((n + k * seg + i, n + k * seg + j, n + (k + 1) * seg + j, n + (k + 1) * seg + i))

    def emit(self, layer, name, material):
        me = bpy.data.meshes.new(name); me.from_pydata([(a * IN, b * IN, c * IN) for a, b, c in self.v], [], self.f); me.validate()
        smooth_by_angle(me, 40)
        o = bpy.data.objects.new(name, me); o.data.materials.append(material)
        return link(o, layer, name)


def fastener(acc, x, y, z0):
    acc.cyl(x, y, z0 - SHANK_L, z0, SHANK_R, 8)                        # through the roof system into the deck (seen in section view)
    acc.cyl(x, y, z0, z0 + WASH_T, WASH_R, 16)                         # washer
    acc.cyl(x, y, z0 + WASH_T, z0 + WASH_T + HEAD_H, HEAD_R, 6)        # hex head


reset_scene()

# (E) roof build-up either side of the joint: deck and insulation (shown for illustration, note), roof system to the joint edge
for s, tag in ((1, "e"), (-1, "w")):
    f = (lambda p: p) if s > 0 else mirror
    B(f"steel_deck_{tag}", "existing", *sorted((s * CI, s * PATCH)), DECK_Z0, DECK_Z1, M("deck"))
    B(f"insulation_{tag}", "existing", *sorted((s * CI, s * PATCH)), DECK_Z1, 0, M("insulation"))
    P(f"membrane_{tag}", "existing", f([(CI, 0), (PATCH, 0), (PATCH, MEM_T), (CI, MEM_T)]), M("membrane"))   # open ends: the app's strip continues it
    P(f"flange_{tag}", "existing", f([(CI, MEM_T), (FO, MEM_T), (FO, FLT), (CI, FLT)]), M("coping"))          # (E) metal mounting flange on the roof system

# (E) flexible bellow: legs up from the flanges' inner edges, looped over the joint
P("bellow", "existing", [(RO, MEM_T)] + arc(RO, 0, math.pi) + [(-RO, MEM_T), (-RI, MEM_T)] + arc(RI, math.pi, 0) + [(RI, MEM_T)], M("rubber"))

# Fasteners through the flanges, 6" o.c. — one backed out at existing, replaced at prep
spots = [(sx * FAST_Y, Y0 + FAST_OC / 2 + k * FAST_OC) for sx in (1, -1) for k in range(int(L // FAST_OC))]
seated = Acc()
for x, y in spots:
    if (x, y) != (LOOSE_X, LOOSE_Y):
        fastener(seated, x, y, FLT)
seated.emit("existing", "fastener", M("fast"))
loose = Acc(); fastener(loose, 0, 0, 0)
o = loose.emit("existing", "fastener_before_loose", M("fast"))
o.location = (LOOSE_X * IN, LOOSE_Y * IN, (FLT + LOOSE_UP) * IN); o.rotation_euler = (math.radians(LOOSE_TILT), 0, 0)
reset = Acc(); fastener(reset, LOOSE_X, LOOSE_Y, FLT); reset.emit("existing", "fastener_after_reset", M("fast"))

# Coats: primer, Flex, topcoat — each a band over the whole profile; Flex and topcoat also dome over every fastener head
for i, (layer, mat) in enumerate((("primer", "primer"), ("flex", "flex"), ("topcoat", "thane")), start=1):
    d0, d1 = (i - 1) * COAT or LIFT, i * COAT   # the primer's inner face sits LIFT off its substrate (see LIFT)
    P(f"{layer}_profile", layer, band(coat_path(FIELD[layer]), d0, d1), M(mat))
    if i >= 2:
        domes = Acc()
        for x, y in spots:
            domes.dome(x, y, FLT + d0, WASH_R + 0.1 + d1, WASH_T + HEAD_H + 0.07 + d1)
        domes.emit(layer, f"{layer}_domes", M(mat))

finalize("expansion-joint-A-3-TYP")
