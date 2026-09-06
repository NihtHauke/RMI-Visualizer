"""
build_cast_iron_drain_D-1-TYP.py — cast-iron roof drain per RMI detail D-1-TYP (with CID-1-21-FT3D as
the 3D reference). VERIFIED against the drawing in an earlier session; this script reproduces the
model that shipped in models/cast-iron-drain-D-1-TYP.glb so it can be regenerated and revised.

    blender -b --python scripts/build_cast_iron_drain_D-1-TYP.py

What the drawing says (VERIFIED):
  * (E) cast-iron bowl set below the field; clamping ring removed and reset in sealant; strainer replaced.
  * Flex encapsulates the ring, extends a minimum of 18" out from the drain and 3" down into the bowl
    past the ring; topcoat extends 1" further into the bowl.
Dimensions of the bowl, ring, flange, sump dish and the (E) roof build-up are ASSUMED (generic 12" drain).

Two things in the shipped .glb were reversed and are corrected here (nothing else changed):
  * the bowl cone was wider at the BOTTOM (Blender's radius1 is the bottom, the opposite of three.js);
  * — see build_curb_mounted_unit_CS-1-TYP.py for the second.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rmi_blender import IN, M, Shell, box, cyl, torus, helper, cut, bevel, hemisphere, reset_scene, finalize

# ---------------------------------------------------------------- dimensions (metres; ASSUMED unless noted)
PATCH        = 60.0 * IN            # square roof patch the model carries (the app's rMem hole sits just inside)
DECK_Z0, DECK_Z1 = -0.0787, -0.0635 # steel deck
INSUL_Z1     = 0.0                  # insulation to the underside of the membrane
MEM_T        = 0.0025               # (E) membrane

DISH_R_BOT   = 6.5 * IN             # sump dish in the insulation: 1" deep, flat floor …
DISH_DEPTH   = 1.0 * IN
DISH_SLOPE   = 3.437                # … opening at this rate (r grows 3.437 m per m of rise) — reads 9.9" at the surface

BOWL_R_TOP   = 6.0 * IN             # (E) cast-iron bowl, wider at the top
BOWL_R_BOT   = 0.1097
BOWL_WALL    = 0.1097 - 0.1066      # bowl wall thickness
BOWL_Z0, BOWL_Z1 = -0.2007, -0.0229
FLANGE_R, FLANGE_T, FLANGE_Z = 0.2083, 0.0089, -0.02415   # bowl flange (solid disc; strainer sits on it)
RING_R, RING_r, RING_Z = 7.0 * IN, 0.014, -0.0089         # clamping ring (rusted): major / minor radius, centre
BOLT_R, BOLT_H, BOLT_Z = 0.0069, 0.0152, 0.0089           # 4 hex bolts on the ring at 45°
STRAINER_R   = 0.1327                                     # replacement strainer dome (wire)
SEAL_R, SEAL_r, SEAL_Z = 0.1933, 0.00485, -0.0191        # sealant bead the ring is reset in

FLEX_OUT     = 24.0 * IN            # Flex min 18" out from the drain — VERIFIED D-1-TYP (24" modelled)
TOP_OUT      = 25.0 * IN            # topcoat 1" past the Flex on the field
FIELD_IN     = 12.0 * IN            # inner edge of the field annuli (meets the sump cone)
INTO_BOWL    = {"primer": -0.1003, "flex": -0.1003, "topcoat": -0.1257}   # 3" into the bowl; topcoat 1" further — VERIFIED
BOWL_TUBE    = {"primer": (0.1106, 0.1091), "flex": (0.1115, 0.1100), "topcoat": (0.1123, 0.1095)}   # (ro, ri) of the tube down the bowl
RING_WRAP    = {"primer": 0.01535, "flex": 0.0166, "topcoat": 0.0178}     # minor radius of the coat over the ring
FIELD_Z      = {"primer": (0.0029, 0.0042), "flex": (0.0039, 0.0052), "topcoat": (0.0050, 0.0062)}
SUMP_Z       = {"primer": (-0.0065, 0.0188), "flex": (-0.0055, 0.0198), "topcoat": (-0.0045, 0.0208)}   # funnel from the ring out to the field

reset_scene()

# (E) roof assembly with the sump dish cut into it
dish = helper(cyl("dish_cutter", "existing", DISH_R_BOT, 2 * DISH_DEPTH, 0, 0, 0, M("deck"), verts=64,
                  r2=DISH_R_BOT + 2 * DISH_DEPTH * DISH_SLOPE))
dish.data.materials.clear()          # a cutter with a material would paint the dish faces in it
box("steel_deck", "existing", PATCH, PATCH, DECK_Z1 - DECK_Z0, 0, 0, (DECK_Z0 + DECK_Z1) / 2, M("deck"))
insul = box("insulation", "existing", PATCH, PATCH, INSUL_Z1 - DECK_Z1, 0, 0, (DECK_Z1 + INSUL_Z1) / 2, M("insulation")); cut(insul, dish)
mem = box("membrane", "existing", PATCH, PATCH, MEM_T, 0, 0, MEM_T / 2, M("membrane")); cut(mem, dish)

# (E) drain body: hollow bowl, solid flange, rusted clamping ring with 4 bolts, new strainer
bowl = cyl("drain_bowl", "existing", BOWL_R_BOT, BOWL_Z1 - BOWL_Z0, 0, 0, (BOWL_Z0 + BOWL_Z1) / 2, M("castiron"), verts=64, r2=BOWL_R_TOP)
cut(bowl, helper(cyl("bowl_bore", "existing", BOWL_R_BOT - BOWL_WALL, 0.3, 0, 0, (BOWL_Z0 + BOWL_Z1) / 2, M("castiron"), verts=64)))
bevel(cyl("bowl_flange", "existing", FLANGE_R, FLANGE_T, 0, 0, FLANGE_Z, M("castiron"), verts=64), 0.0013)
torus("clamping_ring", "existing", RING_R, RING_r, 0, 0, RING_Z, M("rust"))
for i in range(4):
    a = (i * 2 + 1) * 3.14159265 / 4
    cyl(f"bolt_{i}", "existing", BOLT_R, BOLT_H, RING_R * __import__("math").cos(a), RING_R * __import__("math").sin(a), BOLT_Z, M("fast"), verts=6)
hemisphere("strainer_dome", "existing", STRAINER_R, 0, 0, 0, M("castiron"), segments=24, rings=12, wire=0.004)

# Sealant bead the ring is reset in — prep/prime stage work
torus("sealant_bead", "primer", SEAL_R, SEAL_r, 0, 0, SEAL_Z, M("seal"), seg=40)

# Coatings: over the ring → down into the bowl → funnel out over the sump → onto the field
for layer, mat in (("primer", "primer"), ("flex", "flex"), ("topcoat", "thane")):
    torus("over_ring", layer, RING_R, RING_WRAP[layer], 0, 0, RING_Z, M(mat))
    ro, ri = BOWL_TUBE[layer]
    Shell().tube(ro, ri, INTO_BOWL[layer], -0.0241, seg=64).emit(layer, "into_bowl", M(mat))
    z0, z1 = SUMP_Z[layer]
    Shell().revolve([(0.2233, z0), (0.295, z1), (0.3153, z1)], seg=64).emit(layer, "sump", M(mat))
    fz0, fz1 = FIELD_Z[layer]
    Shell().tube(TOP_OUT if layer == "topcoat" else FLEX_OUT, FIELD_IN, fz0, fz1, seg=96).emit(layer, "field", M(mat))

finalize("cast-iron-drain-D-1-TYP")
