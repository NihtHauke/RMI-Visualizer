"""
build_expansion_joint_A-3-TYP.py — curb-mounted expansion joint per RMI detail A-3-TYP (EXPANSION JOINT – TYPICAL, 11/05/24).
There is no 3D concept render for A-3-TYP.

    blender -b --python scripts/build_expansion_joint_A-3-TYP.py

A 4-ft SECTION of the joint, field-mounted like the drain and sleeper: it carries its own patch of roof (the app opens a
rectangular hole in the field sheets round it) and splices into the hospital's code-drawn run (addExpansionJoint in
index.html), which draws the same cross-section from the same numbers (the EJ constants) — keep the two in step or the
seams show. The run lies along Blender Y (the app's z); x = 0 is the joint centre; z = 0 the roof surface under the patch.

What the drawing says (VERIFIED):
  * (E) METAL & FLEXIBLE BELLOW (notes 10 & 12): metal mounting flanges fastened down either side of the joint, with a
    flexible bellow looped up over the joint between them. Note 8: all (E) EPDM, neoprene, PVC and TPO expansion joints
    REGARDLESS OF INDIVIDUAL CONFIGURATION.
  * CONFIRM BELLOW INTEGRITY. REPAIR OR REPLACE DAMAGED MATERIALS. Note 10: improper or ill-fitting joints may move more
    than the RMI materials allow and void the warranty.
  * REPLACE DAMAGED, LOOSE OR MISSING FASTENERS — shown here as one fastener backed out at the existing stage and replaced
    at prep (existing__fastener_before_loose / existing__fastener_after_reset; the app swaps them at prep).
  * Note 12: clean, prepare and prime per the Spec Guide Manual for each (E) roof system, the metal and the flexible bellow.
  * RMI-FLEX VAPOR BARRIER-FLASHING COAT TO FULLY ENCAPSULATE THE EXPANSION JOINT BELLOW, FASTENERS AND MOUNTING FLANGE;
    EXTEND A MIN 2" PAST ASSEMBLY. RMI-THANE / RMI-WHITE over the Flex.
  * Note 11: where gaps at the attachment flanges cannot be bridged with Flex, tape or 3-course polyester/Flex min 2" each
    side of the joint, no voids. Conditional, and not drawn on the section, so not modelled.

ASSUMED (the drawing is NOT TO SCALE and gives only the 2" Flex extent):
  * Mounting the flanges on two wood curbs, with the (E) roof membrane carried up the curbs as base flashing and over their
    tops. The drawing lays the flanges on the roof system over the deck, which it says is "shown for illustration — actual
    type and configuration may vary"; note 8 covers every configuration.
  * The Flex and topcoat carried from the bellow over the flanges and curb tops, down the curbs and onto the field. On a
    full-field roof that is where the field coats meet them; it is well past the drawing's 2" minimum.
  * Every size: 4" joint between 5-1/2" x 10" curbs; 3/16" flashing; 4" x 1/16" flanges; 3/16" bellow rising 1" then
    looping over the joint (crown 3" above the flanges); hex washer-head fasteners mid-flange at 6" o.c.; coat thicknesses.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from rmi_blender import IN, M, box, reset_scene, finalize, link, band, prism_y, smooth_by_angle

# ---------------------------------------------------------------- dimensions (inches; ASSUMED unless noted) — same as EJ in index.html
L        = 48.0                  # modelled section along the joint
GAP      = 4.0                   # joint opening between the curbs' inner faces
CURB_W   = 5.5                   # wood curb
CURB_H   = 10.0                  # curb top above the roof surface
FT       = 0.1875                # (E) base flashing: roof membrane up the curb's outer face and over its top
MT       = 0.0625                # (E) metal mounting flange (drawing: thin plate each side, VERIFIED that it is there)
FLANGE   = 4.0                   # flange width, from the joint edge out across the curb top
BT       = 0.1875                # bellow wall (drawing: flexible bellow looped over the joint, VERIFIED)
LEG      = 1.0                   # straight bellow leg above the flange before the loop
FAST_Y   = 4.0                   # fastener line from the joint centre (mid-flange)
FAST_OC  = 6.0                   # fastener spacing along the joint
HEAD_R, HEAD_H, WASH_R, WASH_T, SHANK_R, SHANK_L = 0.22, 0.14, 0.30, 0.04, 0.09, 1.5
LOOSE_X, LOOSE_Y, LOOSE_UP, LOOSE_TILT = -FAST_Y, -3.0, 0.40, 9.0  # the fastener backed out at existing: west flange, app z = +3" (faces the detail camera)
COAT     = 0.04                  # visual thickness per layer (1 mm), as the edge-metal and penthouse runs
LIFT     = 0.01                  # primer's inner face off its substrate: the app's materials are double-sided, so a coincident face z-fights
FIELD    = {"primer": 17.0, "flex": 17.0, "topcoat": 17.2}   # coats onto the patch's field, from the joint centre
PATCH    = 18.0                  # roof patch half-width (the app's membrane hole sits 1.2" inside it)
DECK_Z0, DECK_Z1 = -3.1, -2.5    # steel deck, as the other flat-roof models
MEM_T    = 0.1                   # (E) membrane top = 0.1" above the app's field plane, so the two never z-fight
ARC      = 24                    # segments in the bellow loop

# ---------------------------------------------------------------- derived (inches)
CI  = GAP / 2                    # curb inner face = flange inner edge = bellow outer leg
CO0 = CI + CURB_W                # curb outer face
CO  = CO0 + FT                   # flashing outer face
CT  = CURB_H + FT                # flashing top (under the flange)
FLT = CT + MT                    # flange top
FO  = CI + FLANGE                # flange outer edge (1.5" short of the curb's outer edge)
RO, RI = CI, CI - BT             # bellow outer / inner radius
ZC  = FLT + LEG                  # centre of the loop
Y0, Y1 = -L / 2, L / 2


def arc(R, a0, a1):
    return [(R * math.cos(a0 + (a1 - a0) * i / ARC), ZC + R * math.sin(a0 + (a1 - a0) * i / ARC)) for i in range(ARC + 1)]


def mirror(pts):
    return [(-y, z) for y, z in pts]


def coat_path(field):
    """The surface every coat follows, walked with the substrate on the left: field → curb face → curb top → over the flange
    edge → across the flange → up the bellow, over the loop, and down the far side to the far field."""
    right = [(field, MEM_T), (CO, MEM_T), (CO, CT), (FO, CT), (FO, FLT), (RO, FLT)]
    return right + arc(RO, 0, math.pi) + mirror(right[::-1])


def P(name, layer, pts, mat):
    """Run part: a prism of the (y, z) inch polygon along the section, open at both ends."""
    return prism_y(name, layer, [(y * IN, z * IN) for y, z in pts], mat, Y0 * IN, Y1 * IN)


def B(name, layer, y0, y1, z0, z1, mat):
    """Patch part: a closed box spanning y0..y1 across, z0..z1 up, the full section length."""
    return box(name, layer, (y1 - y0) * IN, L * IN, (z1 - z0) * IN, (y0 + y1) / 2 * IN, 0, (z0 + z1) / 2 * IN, mat)


class Acc:
    """Accumulates small solids at (x, y) positions into ONE mesh: hex fasteners with washers and shanks, coat domes."""
    def __init__(self):
        self.v, self.f = [], []

    def cyl(self, x, y, z0, z1, r, seg=16, cap_bot=True):
        n = len(self.v); cs = [(math.cos(2 * math.pi * i / seg), math.sin(2 * math.pi * i / seg)) for i in range(seg)]
        self.v += [(x + r * c, y + r * s, z0) for c, s in cs] + [(x + r * c, y + r * s, z1) for c, s in cs] + [(x, y, z0), (x, y, z1)]
        c0, c1 = n + 2 * seg, n + 2 * seg + 1
        for i in range(seg):
            j = (i + 1) % seg
            self.f.append((n + i, n + j, n + seg + j, n + seg + i)); self.f.append((c1, n + seg + i, n + seg + j))
            if cap_bot:
                self.f.append((c0, n + j, n + i))

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
    acc.cyl(x, y, z0 - SHANK_L, z0, SHANK_R, 8)                        # into the curb (seen in section view)
    acc.cyl(x, y, z0, z0 + WASH_T, WASH_R, 16)                         # washer
    acc.cyl(x, y, z0 + WASH_T, z0 + WASH_T + HEAD_H, HEAD_R, 6)        # hex head


reset_scene()

# (E) roof patch: steel deck with the building joint open between the curbs, insulation and membrane outside them
for s in (1, -1):
    tag = "e" if s > 0 else "w"
    B(f"steel_deck_{tag}", "existing", *sorted((s * CI, s * PATCH)), DECK_Z0, DECK_Z1, M("deck"))
    B(f"insulation_{tag}", "existing", *sorted((s * CO0, s * PATCH)), DECK_Z1, 0, M("insulation"))
    B(f"membrane_{tag}", "existing", *sorted((s * CO, s * PATCH)), 0, MEM_T, M("membrane"))

# (E) wood curbs, the (E) membrane up each as base flashing and over its top, and the metal mounting flanges on top (ASSUMED mounting)
curb = [(CI, DECK_Z1), (CO0, DECK_Z1), (CO0, CURB_H), (CI, CURB_H)]
flashing = [(CO0, 0), (CO, 0), (CO, CT), (CI, CT), (CI, CURB_H), (CO0, CURB_H)]
flange = [(CI, CT), (FO, CT), (FO, FLT), (CI, FLT)]
for s, tag in ((1, "e"), (-1, "w")):
    f = (lambda p: p) if s > 0 else mirror
    P(f"curb_{tag}", "existing", f(curb), M("wood"))
    P(f"membrane_flashing_{tag}", "existing", f(flashing), M("membrane"))
    P(f"flange_{tag}", "existing", f(flange), M("coping"))

# (E) flexible bellow: legs up from the flanges' inner edges, looped over the joint
P("bellow", "existing", [(RO, CT)] + arc(RO, 0, math.pi) + [(-RO, CT), (-RI, CT)] + arc(RI, math.pi, 0) + [(RI, CT)], M("rubber"))

# Fasteners through the flanges into the curbs, 6" o.c. — one backed out at existing, replaced at prep
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
    d0, d1 = (i - 1) * COAT or LIFT, i * COAT   # the primer's inner face sits LIFT off its substrate: the app's materials are double-sided, so a face ON the substrate z-fights
    P(f"{layer}_profile", layer, band(coat_path(FIELD[layer]), d0, d1), M(mat))
    if i >= 2:
        domes = Acc()
        for x, y in spots:
            domes.dome(x, y, FLT + d0, WASH_R + 0.1 + d1, WASH_T + HEAD_H + 0.07 + d1)
        domes.emit(layer, f"{layer}_domes", M(mat))

finalize("expansion-joint-A-3-TYP")
