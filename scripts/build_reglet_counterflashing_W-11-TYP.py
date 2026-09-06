"""
build_reglet_counterflashing_W-11-TYP.py — wall tie-in with Fry-type reglet counterflashing, per RMI
detail W-11-TYP (REGLET COUNTERFLASHING @ WALL – TYPICAL, 11/05/24) with W13-FT-26-3D as reference.

    blender -b --python scripts/build_reglet_counterflashing_W-11-TYP.py

A 4-ft SECTION of the wall tie-in. The (E) wall itself is not in the model (the app's wall block is not
cut); everything here stands against the wall face at y=0, with +y toward the roof and z=0 at the roof
surface. The app splices it into addWallTie's code-drawn run, which draws the same cross-section from
the same numbers (index.html WT constants) — keep the two in step or the seams show.

What the 2D drawing says (VERIFIED):
  * (E) wall flashing up the wall to an (E) Fry-type reglet with counterflashing.
  * Remove and reset the (E) counterflashing; replace damaged or worn. (The app hides it from the prep
    stage until the topcoat goes on: parts named existing__counterflashing_*.)
  * Insure the wall flashing is firmly attached; where voids, fasten with termination bar and sealant,
    12" o.c.
  * Rake out (E) sealant/mastic at the reglet; new continuous bead of RMI approved sealant.
  * Clean, prepare and prime per the Spec Guide Manual.
  * RMI-Flex: encapsulate the (E) flashing and EXTEND TO THE REGLET RECEIVER — the full flashing height
    and on up the bare wall to the reglet, not a fixed band.
  * RMI-Thane / White: encapsulate the Flex. Coating the counterflashing assembly is OPTIONAL (not shown).
  * Note 9: applies to all (E) BUR, mod-bit, EPDM, PVC, TPO regardless of wall type.

ASSUMED (drawing is NTS, no dimensions beyond the 12" o.c.): flashing height 24"; reglet 2" above it;
6" cant (not drawn — generic under base flashing); flashing foot 4" past the cant; term bar at the
flashing top; counterflashing laps the flashing 4", stands 1" off it; Flex 2" past the flashing foot on
the field, topcoat 1" past the Flex; all coat thicknesses.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from rmi_blender import IN, M, box, cyl, link, reset_scene, finalize

# ---------------------------------------------------------------- dimensions (inches; ASSUMED unless noted)
L        = 48.0                     # modelled section along the wall
FH       = 24.0                     # (E) wall flashing height — the current app assumption
REG      = FH + 2.0                 # reglet, 2" above the flashing top
CANT     = 6.0                      # 45° cant, 6" legs
FLASH_T  = 0.1875                   # (E) mod-bit base flashing sheet
FOOT     = CANT + 4.0               # flashing foot on the field, from the wall face
BAR_H, BAR_T, BAR_TOP = 1.0, 0.125, FH - 0.5      # termination bar just below the flashing top
SCREW_X  = (-18.0, -6.0, 6.0, 18.0)               # 12" o.c. — VERIFIED
SCREW_R, SCREW_H = 0.1875, 0.125
GROOVE_H, LIP_H  = 0.75, 0.75                     # Fry reglet: groove in the wall + receiver lip below it
CF_STAND, CF_KNEE, CF_BOT, HEM = 1.0, REG - 1.5, FH - 4.0, 0.5   # counterflashing: stand-off, bend, bottom (4" lap), hem
BEAD_R   = 0.1875                                 # sealant beads (reglet, term bar)
COAT     = 0.04                                   # visual coat thickness (1 mm) per layer
FIELD    = {"primer": FOOT + 2.0, "flex": FOOT + 2.0, "topcoat": FOOT + 3.0}   # coats onto the field, from the wall face
MT       = 0.04                                   # metal sheet thickness for the counterflashing / lip (exaggerated)

X0, X1 = -L / 2 * IN, L / 2 * IN


def B(name, layer, y0, y1, z0, z1, mat, x0=X0, x1=X1):
    """Axis-aligned slab spanning y0..y1 (from the wall), z0..z1 (height), x0..x1 (along the wall). Inches in, metres out."""
    return box(name, layer, (x1 - x0), (y1 - y0) * IN, (z1 - z0) * IN, (x0 + x1) / 2, (y0 + y1) / 2 * IN, (z0 + z1) / 2 * IN, mat)


def slab_between(name, layer, p, q, t, mat, x0=X0, x1=X1):
    """Sheet of thickness t (inches) whose centre-line runs from (y,z)=p to q in the wall-normal plane (a 45° cant
    face, an angled counterflashing bend). Built as a box rotated about x."""
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
    """One coat as nested sheets, i = 1 primer, 2 Flex, 3 topcoat: field foot → over the cant → up the flashing →
    over the term bar → on up the bare wall to the reglet receiver (VERIFIED: Flex extends to the reglet)."""
    d0, d1 = (i - 1) * COAT, i * COAT
    mat = M(layer if layer != "topcoat" else "thane")
    B(f"{layer}_foot", layer, FOOT + d0, FIELD[layer], FLASH_T + d0, FLASH_T + d1, mat)                       # field, past the flashing foot
    B(f"{layer}_foot_over", layer, CANT, FOOT + d1, FLASH_T + d0, FLASH_T + d1, mat)                          # over the foot itself
    slab_between(f"{layer}_cant", layer, (CANT + d0 * 0.7, FLASH_T + d0 * 0.7), (d0 * 0.7, CANT + FLASH_T + d0 * 0.7), COAT, mat)
    B(f"{layer}_flashing", layer, FLASH_T + d0, FLASH_T + d1, CANT, BAR_TOP - BAR_H - d1, mat)               # up the flashing to the bar
    B(f"{layer}_bar", layer, FLASH_T, FLASH_T + BAR_T + d1, BAR_TOP - BAR_H - d1, BAR_TOP + d1, mat)          # encapsulates the term bar
    B(f"{layer}_flashing_top", layer, d0, FLASH_T + BAR_T + d1, BAR_TOP + d0, FH + d1, mat)                   # over the flashing's top edge
    B(f"{layer}_wall", layer, d0, d1, FH, REG - LIP_H, mat)                                                  # bare wall up to the reglet receiver


reset_scene()

# (E) cant + (E) mod-bit base flashing: foot on the field, over the cant, up the wall
prism("cant", "existing", [(0, 0), (CANT, 0), (0, CANT)], M("wood"))
B("flashing_foot", "existing", CANT, FOOT, 0, FLASH_T, M("modbit"))
slab_between("flashing_cant", "existing", (CANT, FLASH_T / 2), (0, CANT + FLASH_T / 2), FLASH_T, M("modbit"))
B("flashing_wall", "existing", 0, FLASH_T, CANT, FH, M("modbit"))

# Termination bar + screws 12" o.c. (voids fastened per the drawing)
B("term_bar", "existing", FLASH_T, FLASH_T + BAR_T, BAR_TOP - BAR_H, BAR_TOP, M("coping"))
for i, x in enumerate(SCREW_X):
    s = cyl(f"screw_{i}", "existing", SCREW_R * IN, SCREW_H * IN, x * IN, (FLASH_T + BAR_T + SCREW_H / 2) * IN, (BAR_TOP - BAR_H / 2) * IN, M("fast"), verts=16)
    s.rotation_euler = (math.pi / 2, 0, 0)

# (E) Fry-type reglet: dark groove at the wall face with the receiver lip below it
B("reglet_groove", "existing", -0.05, 0.05, REG, REG + GROOVE_H, M("seal"))
B("reglet_lip", "existing", 0, MT, REG - LIP_H, REG, M("coping"))

# (E) counterflashing hooked into the reglet: bend out, drop over the flashing, hemmed kick-out at the bottom.
# Named existing__counterflashing_* so the app removes it at prep and resets it with the topcoat.
slab_between("counterflashing_bend", "existing", (MT / 2, REG - LIP_H), (CF_STAND, CF_KNEE), MT, M("coping"))
B("counterflashing_drop", "existing", CF_STAND, CF_STAND + MT, CF_BOT, CF_KNEE, M("coping"))
slab_between("counterflashing_hem", "existing", (CF_STAND, CF_BOT), (CF_STAND + HEM, CF_BOT - HEM * 0.6), MT, M("coping"))

# New sealant: continuous bead in the reglet (rake out the old), and along the top of the term bar
B("sealant_reglet", "primer", 0, BEAD_R * 1.6, REG + GROOVE_H * 0.25, REG + GROOVE_H * 0.25 + BEAD_R * 1.6, M("seal"))
B("sealant_bar", "primer", FLASH_T, FLASH_T + BAR_T + BEAD_R, BAR_TOP, BAR_TOP + BEAD_R, M("seal"))

coat("primer", 1)
coat("flex", 2)
coat("topcoat", 3)

finalize("reglet-counterflashing-W-11-TYP")
