"""
build_circular_support_P-5-C.py — circular steel support through a concrete deck, per RMI detail P-5-C (CIRCULAR SUPPORT
PENETRATION – CONCRETE – TYPICAL, 11/05/24), with P-7-C (CIRCULAR SUPPORT – CONCRETE – TYPICAL, 11/05/24) — the same support
on a fastened base plate — as reference. Neither has a 3D concept render.

    blender -b --python scripts/build_circular_support_P-5-C.py

Field-mounted like the drain and soil stack: the model carries its own disc of concrete deck (the app opens a round hole
in the field sheets over it) and the bottom 30" of the post; the app's code-drawn post (addPost in index.html) carries on
from there, and the other gallery posts draw the same wrap from the same numbers (SP) — keep the two in step.

What the drawings say (VERIFIED):
  * (E) circular support through the (E) concrete deck, with a backer rod in the gap at the deck (P-5-C).
  * RAKE OUT (E) SEALANT, MASTIC, REPAIRS. APPLY NEW CONTINUOUS BEAD OF RMI APPROVED SEALANT AND/OR TAPE PRIOR TO
    INSTALLATION OF RMI-FLEX AND WEAR SURFACE COATING — the old mastic collar is existing__mastic_before_rakeout, which the
    app removes at prep; the new bead and backer rod appear at prep.
  * RMI APPROVED BUTYL TAPE OR THREE COURSE APPLICATION OF RMI-FLEX / POLYESTER EXTENDING 2" VERTICALLY AND 4" HORIZONTAL.
    Butyl tape shown.
  * Note 10: clean, prepare and prime per the Spec Guide Manual. Note 9: adhesion test and moisture scan first.
  * RMI-FLEX VAPOR BARRIER-FLASHING COAT: EXTEND A MIN. 6" ONTO PENETRATION PAST FLASHING — 2" + 6" = 8" above the deck.
  * RMI-THANE, RMI-WHITE: EXTEND A MIN. 2" ONTO PENETRATION PAST RMI-FLEX — 10" above the deck. Both modelled at the minimum.
  * On the deck the Flex and topcoat run on across the field (Plate C is full-field).
  * Note 7: all circular supports — site screen, solar, mechanical. Note 8: installations directly over concrete decks.
  * P-7-C (reference): the same coats on a base-plate support — Flex min 4" up, topcoat min 2" past it, every fastener
    encapsulated in Flex, beads at the post and at the plate edge. The silo gallery posts pass through the deck, so P-5-C governs.

ASSUMED (the drawings are NOT TO SCALE and give only the wrap extents above): the 10-3/4" OD steel pipe post (10" NPS) with
a 0.365" wall; the 1/2" gap round it and a 6" deck; the 1/2" bead and the backer rod's size and depth; the old mastic
collar's shape; the 60-mil tape and where its corner cuts across the bead; coat thicknesses; the 18" deck patch.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from rmi_blender import IN, M, Shell, reset_scene, finalize, link, band, offset_path

# ---------------------------------------------------------------- dimensions (inches; ASSUMED unless noted) — same as SP in index.html
POST_R    = 5.375            # 10-3/4" OD steel pipe (10" NPS) — the app's gallery posts are this size
WALL      = 0.365            # standard-weight wall
GAP       = 0.5              # annular gap between the post and the deck (drawing: gap with backer rod, VERIFIED that it is there)
DECK_T    = 6.0              # concrete deck
DT        = 0.1              # deck top = 0.1" above the app's field plane, so the two never z-fight
PATCH_R   = 18.0             # deck patch (the app's membrane hole sits 1.2" inside it)
STUB_UP   = 30.0             # post modelled to 30" above the roof; the app's post carries on above
STUB_DOWN = 12.0             # below the deck soffit, so the section view shows it passing through
BEAD_R    = 0.25             # new continuous sealant bead at the post / deck corner (VERIFIED that it is there)
ROD_RR, ROD_RZ, ROD_Z = 0.24, 0.40, -0.45    # backer rod: radial and vertical half-sizes, centre height, in the gap
TAPE_UP   = 2.0              # VERIFIED: butyl tape 2" vertically ...
TAPE_OUT  = 4.0              # ... and 4" horizontally
TAPE_T    = 0.06             # 60-mil tape
CH        = 0.6              # tape corner cut across the bead
FLEX_UP   = TAPE_UP + 6.0    # VERIFIED: Flex min 6" onto the penetration past the flashing (modelled at the minimum)
TOP_UP    = FLEX_UP + 2.0    # VERIFIED: topcoat min 2" past the Flex
UP        = {"primer": FLEX_UP, "flex": FLEX_UP, "topcoat": TOP_UP}   # primer under the Flex, to the same height
FIELD     = {"primer": 17.0, "flex": 17.0, "topcoat": 17.2}         # coats onto the patch, from the post axis
COAT      = 0.04             # visual thickness per layer (1 mm), as the other models
LIFT      = 0.01             # primer's inner face off its substrate: the app's materials are double-sided, so a coincident face z-fights
MASTIC_OUT, MASTIC_UP = 2.5, 0.9   # old (E) mastic collar, raked out at prep

# ---------------------------------------------------------------- derived (inches)
HOLE_R = POST_R + GAP
R4     = POST_R + TAPE_OUT
TAPE_PATH = [(R4, DT), (POST_R + CH, DT), (POST_R, DT + CH), (POST_R, DT + TAPE_UP)]   # the substrate the tape lies on


def coat_path(layer):
    """Walked with the substrate on the left: across the deck → over the tape's edge → over the tape → up the post."""
    over = offset_path(TAPE_PATH, TAPE_T)
    return [(FIELD[layer], DT)] + [(R4, DT)] + over + [(POST_R, DT + TAPE_UP), (POST_R, DT + UP[layer])]


def S(pts):
    return [(r * IN, z * IN) for r, z in pts]


reset_scene()

# (E) concrete deck patch with the gap round the post
Shell().tube(PATCH_R * IN, HOLE_R * IN, -DECK_T * IN, DT * IN).emit("existing", "concrete_deck", M("concrete"))

# (E) steel pipe post through the deck: outer wall, bore, bottom end (the top is open — the app's post continues above)
zb, zt = -(DECK_T + STUB_DOWN) * IN, STUB_UP * IN
Shell().revolve([(POST_R * IN, zb), (POST_R * IN, zt)]).revolve([((POST_R - WALL) * IN, zt), ((POST_R - WALL) * IN, zb)]) \
       .revolve([((POST_R - WALL) * IN, zb), (POST_R * IN, zb)]).emit("existing", "post", M("castiron"))

# (E) sealant and mastic at the base — lumpy with age; raked out at prep
seg, K = 48, 8
mv, mf = [], []
for i in range(seg):
    t = 2 * math.pi * i / seg
    a = MASTIC_OUT * (1 + 0.18 * math.sin(3 * t) + 0.10 * math.sin(7 * t + 1.0))
    b = MASTIC_UP * (1 + 0.20 * math.sin(5 * t + 0.5))
    for k in range(K + 1):
        p = (math.pi / 2) * k / K
        r, z = POST_R - 0.05 + a * math.cos(p), DT - 0.02 + b * math.sin(p)
        mv.append((r * IN * math.cos(t), r * IN * math.sin(t), z * IN))
for i in range(seg):
    j = (i + 1) % seg
    for k in range(K):
        mf.append((i * (K + 1) + k, j * (K + 1) + k, j * (K + 1) + k + 1, i * (K + 1) + k + 1))
me = bpy.data.meshes.new("mastic"); me.from_pydata(mv, [], mf); me.validate()
for p in me.polygons:
    p.use_smooth = True
o = bpy.data.objects.new("mastic", me); o.data.materials.append(M("mastic")); link(o, "existing", "mastic_before_rakeout")

# Prep (shown from the prep stage, not swept): backer rod in the gap, new bead at the corner, butyl tape 2" up / 4" out
rod = [(POST_R + GAP / 2 + ROD_RR * math.cos(2 * math.pi * k / 16), ROD_Z + ROD_RZ * math.sin(2 * math.pi * k / 16)) for k in range(16)]
Shell().ring(S(rod)).emit("primer", "sealant_backer_rod", M("rubber"))
Shell().torus((POST_R + 0.1) * IN, BEAD_R * IN, (DT + 0.1) * IN).emit("primer", "sealant_bead", M("seal"))
Shell().ring(S(band(TAPE_PATH, 0, TAPE_T))).emit("primer", "tape_butyl", M("tape"))

# Coats: primer and Flex 8" up the post, topcoat 10"; all three on across the deck patch
for i, (layer, mat) in enumerate((("primer", "primer"), ("flex", "flex"), ("topcoat", "thane")), start=1):
    Shell().ring(S(band(coat_path(layer), (i - 1) * COAT or LIFT, i * COAT))).emit(layer, f"{layer}_wrap", M(mat))   # primer lifted LIFT off its substrate (see LIFT)

finalize("circular-support-P-5-C")
