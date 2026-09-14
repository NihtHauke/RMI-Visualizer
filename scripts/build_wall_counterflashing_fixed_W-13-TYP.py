"""
build_wall_counterflashing_fixed_W-13-TYP.py — penthouse wall with a fixed, surface-mounted counterflashing, per RMI
detail W-13-TYP (WALL COUNTERFLASHING (FIXED) – TYPICAL, 11/05/24) with W-11-24-FT-3D (surface counterflashing
concept) as reference.

    blender -b --python scripts/build_wall_counterflashing_fixed_W-13-TYP.py

A 4-ft SECTION of the wall base. The (E) wall itself is not in the model (the app's penthouse block is not cut);
everything stands against the wall face at y=0, with +y toward the roof and z=0 at the roof surface. The app
splices it into addPenthouse's code-drawn run, which draws the same cross-section from the same numbers
(index.html PW13 constants) — keep the two in step or the seams show.

What the 2D drawing says (VERIFIED):
  * Note 7: the detail applies to FIXED counterflashing that cannot be removed or lifted — it stays in place
    through every stage (unlike W-11-TYP, where it is removed and reset). Replace damaged metal counterflashing.
  * Bead of RMI approved sealant at the top edge of the counterflashing, where it meets the wall.
  * Clean, prepare and prime per the Spec Guide Manual for each roof system and surface.
  * RMI-Flex vapor barrier-flashing coat encapsulates the (E) flashing, up to the counterflashing.
  * RMI-Thane / White encapsulates the Flex. Coating the counterflashing assembly is OPTIONAL (not shown).
  * 24 ga. skirt metal, fastened through the counterflashing, extends a MIN. 4" over the RMI system.
  * Note 9: all (E) BUR, mod-bit, EPDM, PVC, TPO systems regardless of wall type and configuration.

ASSUMED (drawing is NTS, no dimensions): counterflashing top 24" above the roof, 6" tall, standing 1" off the wall
with a 1/2" hem turned toward the wall; the (E) flashing running up behind it to its top; 6" cant and 10" flashing
foot (not drawn — same generic base as W-11-TYP); coats 1/2" up behind the hem; skirt 21" to 13.5" (5" over the
coats); skirt fasteners 12" o.c.; the skirt going on after the topcoat; field extents; all coat thicknesses.
No term bar is drawn on W-13-TYP: the counterflashing's own top flange carries the sealant bead.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from rmi_blender import IN, M, box, cyl, link, reset_scene, finalize

# ---------------------------------------------------------------- dimensions (inches; ASSUMED unless noted)
L        = 48.0                     # modelled section along the wall
CANT     = 6.0                      # 45° cant, 6" legs (not drawn on W-13-TYP)
T        = 0.1875                   # (E) base flashing sheet
FOOT     = CANT + 4.0               # flashing foot on the field, from the wall face
CF_TOP   = 24.0                     # fixed counterflashing top flange (sealant bead above it)
CF_STAND, CF_BOT, HEM = 1.0, 18.0, 0.5            # face stand-off from the wall, bottom edge, hem turned toward the wall
COAT_TOP = CF_BOT + 0.5             # Flex / topcoat run up to the counterflashing, tucked 1/2" behind the hem
SK_TOP, SK_BOT, SK_KICK = 21.0, COAT_TOP - 5.0, 0.75   # 24 ga. skirt: laps the coats 5" (drawing: MIN. 4" — VERIFIED), kick-out at the bottom
SK_KNEE  = SK_BOT + SK_KICK
SCREW_Z  = 19.5                     # skirt fasteners through the counterflashing face
SCREW_X  = (-18.0, -6.0, 6.0, 18.0)               # 12" o.c.
SCREW_R, SCREW_H = 0.1875, 0.125
BEAD_R   = 0.1875                   # sealant bead at the top edge
COAT     = 0.04                     # visual coat thickness (1 mm) per layer
FIELD    = {"primer": FOOT + 2.0, "flex": FOOT + 2.0, "topcoat": FOOT + 3.0}   # coats onto the field, from the wall face
MT       = 0.04                     # sheet metal thickness (exaggerated)

X0, X1 = -L / 2 * IN, L / 2 * IN


def B(name, layer, y0, y1, z0, z1, mat, x0=X0, x1=X1):
    """Axis-aligned slab spanning y0..y1 (from the wall), z0..z1 (height), x0..x1 (along the wall). Inches in, metres out."""
    return box(name, layer, (x1 - x0), (y1 - y0) * IN, (z1 - z0) * IN, (x0 + x1) / 2, (y0 + y1) / 2 * IN, (z0 + z1) / 2 * IN, mat)


def slab_between(name, layer, p, q, t, mat, x0=X0, x1=X1):
    """Sheet of thickness t (inches) whose centre-line runs from (y,z)=p to q in the wall-normal plane."""
    (y0, z0), (y1, z1) = p, q
    ln = math.hypot(y1 - y0, z1 - z0); ang = math.atan2(z1 - z0, y1 - y0)
    o = box(name, layer, x1 - x0, ln * IN, t * IN, (x0 + x1) / 2, (y0 + y1) / 2 * IN, (z0 + z1) / 2 * IN, mat)
    o.rotation_euler = (ang, 0, 0)
    return o


def prism(name, layer, pts, mat, x0=X0, x1=X1):
    """Triangular prism along x from a (y,z) triangle in inches — the cant."""
    v = [(x0, y * IN, z * IN) for (y, z) in pts] + [(x1, y * IN, z * IN) for (y, z) in pts]
    f = [(0, 2, 1), (3, 4, 5), (0, 1, 4, 3), (1, 2, 5, 4), (2, 0, 3, 5)]
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], f); me.validate()
    o = bpy.data.objects.new(name, me); o.data.materials.append(mat)
    return link(o, layer, name)


def coat(layer, i):
    """One coat as nested sheets, i = 1 primer, 2 Flex, 3 topcoat: field foot → over the flashing foot → over the cant →
    up the (E) flashing to the underside of the fixed counterflashing (VERIFIED: encapsulate the (E) flashing)."""
    d0, d1 = (i - 1) * COAT, i * COAT
    mat = M(layer if layer != "topcoat" else "thane")
    B(f"{layer}_foot", layer, FOOT + d0, FIELD[layer], T + d0, T + d1, mat)
    B(f"{layer}_foot_over", layer, CANT, FOOT + d1, T + d0, T + d1, mat)
    slab_between(f"{layer}_cant", layer, (CANT + d0 * 0.7, T + d0 * 0.7), (d0 * 0.7, CANT + T + d0 * 0.7), COAT, mat)
    B(f"{layer}_flashing", layer, T + d0, T + d1, CANT, COAT_TOP, mat)


reset_scene()

# (E) cant + (E) base flashing: foot on the field, over the cant, up the wall behind the counterflashing to its top
prism("cant", "existing", [(0, 0), (CANT, 0), (0, CANT)], M("wood"))
B("flashing_foot", "existing", CANT, FOOT, 0, T, M("modbit"))
slab_between("flashing_cant", "existing", (CANT, T / 2), (0, CANT + T / 2), T, M("modbit"))
B("flashing_wall", "existing", 0, T, CANT, CF_TOP, M("modbit"))

# (E) fixed surface-mounted counterflashing — stays put (note 7). Named fixed_cf_* so the app's remove/reset rule
# (parts named counterflashing_*) never touches it.
B("fixed_cf_flange", "existing", 0, CF_STAND + MT, CF_TOP, CF_TOP + MT, M("coping"))
B("fixed_cf_face", "existing", CF_STAND, CF_STAND + MT, CF_BOT, CF_TOP, M("coping"))
slab_between("fixed_cf_hem", "existing", (CF_STAND + MT / 2, CF_BOT), (CF_STAND - HEM, CF_BOT - HEM * 0.6), MT, M("coping"))

# New bead of RMI approved sealant at the top edge, where the flange meets the wall (prep work: shown from prep)
B("sealant_top", "primer", 0, BEAD_R * 1.6, CF_TOP + MT, CF_TOP + MT + BEAD_R * 1.6, M("seal"))

coat("primer", 1)
coat("flex", 2)
coat("topcoat", 3)

# New 24 ga. skirt metal over the finished RMI system, fastened through the counterflashing face.
# Named skirt_* so the app shows it only once the topcoat is on.
SY = CF_STAND + MT
B("skirt_face", "existing", SY, SY + MT, SK_KNEE, SK_TOP, M("coping"))
slab_between("skirt_kick", "existing", (SY + MT / 2, SK_KNEE), (SY + MT / 2 + SK_KICK, SK_BOT), MT, M("coping"))
for i, x in enumerate(SCREW_X):
    s = cyl(f"skirt_screw_{i}", "existing", SCREW_R * IN, SCREW_H * IN, x * IN, (SY + MT + SCREW_H / 2) * IN, SCREW_Z * IN, M("fast"), verts=16)
    s.rotation_euler = (math.pi / 2, 0, 0)

finalize("wall-counterflashing-fixed-W-13-TYP")
