"""
build_overflow_scupper_D-4-TYP.py — overflow (thru-wall) scupper per RMI detail D-4-TYP (OVERFLOW SCUPPER –
TYPICAL, 11/05/24) with D4-1-FT-3D (THRU-WALL SCUPPER – CONCEPT DRAWING, 9/1/21) as reference.

    blender -b --python scripts/build_overflow_scupper_D-4-TYP.py

A 4-ft SECTION OF PARAPET with the scupper tube through it, sitting above the (E) cant. The app splices it into a
block's parapet (makeBlock `splices`), which draws the same parapet base — cant, base flashing and the three coats —
from the same numbers (index.html PB constants), so keep the two in step or the seams show. The coping run continues
over the section unchanged (the section stops at the top of the parapet).

x runs along the wall; y=0 is the ROOF-SIDE wall face with +y toward the roof (the loader maps it to run-local -z,
like the reglet model), so the parapet occupies y = -PT..0 and the exterior face is y = -PT; z=0 is the roof surface.

What the 2D drawing says (VERIFIED):
  * (E) scupper tube through the (E) wall above the (E) cant, (E) flashing on the wall. Replace damaged components;
    treat rust, replace where pin-holed (note 12); plastic/ABS scuppers excluded (note 11); water test before and
    after (note 10).
  * Clean, prepare and prime per the Spec Guide Manual for the roof system and the scupper (note 13).
  * RMI-Flex flashing coat: ENCAPSULATE THE INTERIOR OF THE SCUPPER TUBE and extend a minimum 12" from the scupper
    onto the field. RMI-Flex base coat continues over the field and up the (E) wall flashing.
  * RMI-Thane / RMI-White over all of it.
  * Bead of RMI approved sealant at the exterior termination (drawn at the tube's bottom edge). Configurations vary and
    sealant may or may not apply, but the exterior must be watertight to the building (note 14).

ASSUMED (the drawing is NTS and gives no sizes): tube 16" x 5" clear in sheet metal; 1" projection and a 2" collar
plate on the exterior, with the sealant bead run round the whole collar (the drawing shows it at the bottom); the
tube's bottom bent down 3" over the cant on the roof side (from the 3D concept); 6" cant; base flashing to the top
of the parapet; 10" flashing foot; the 12" apron measured from the cant toe and 12" either side of the tube; every
coat thickness (1/4" so the nested coats read on screen).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from rmi_blender import IN, M, box, link, reset_scene, finalize

# ---------------------------------------------------------------- the parapet this splices into (must match makeBlock / PB in index.html)
L, PT, PH = 48.0, 12.0, 36.0        # section length, parapet thickness, parapet height (bigbox: PH 3 ft)
CANT   = 6.0                        # 45° cant, 6" legs                                   ASSUMED (same as the reglet model)
FT     = 0.1875                     # (E) base flashing sheet                              ASSUMED
FOOT   = CANT + 4.0                 # flashing foot on the field, from the wall face       ASSUMED
COAT   = 0.25                       # visual coat thickness per layer                      ASSUMED
FIELD  = {"primer": FOOT + 2.0, "flex": FOOT + 2.0, "topcoat": FOOT + 3.0}   # base-coat foot on the field, from the wall face
TOP    = PH - 0.1                   # coats stop just under the coping cap
SLOPE  = CANT + FT / 2 + FT / math.sqrt(2)     # outer face of the flashing over the cant: y + z = SLOPE

# ---------------------------------------------------------------- the scupper (ASSUMED unless marked)
TW, TH = 16.0, 5.0                  # clear opening                                        ASSUMED
MT     = 0.08                       # tube sheet metal (exaggerated)                       ASSUMED
EXT    = 1.0                        # projection past the exterior face                    ASSUMED
COLLAR = 2.0                        # exterior collar plate margin round the opening      ASSUMED (3D concept)
FLANGE = 3.0                        # tube bottom bent down over the cant, roof side       ASSUMED (3D concept)
BEAD   = 0.25                       # sealant bead at the exterior termination            VERIFIED at the bottom, ASSUMED round the collar
APRON  = {"primer": CANT + 12.0, "flex": CANT + 12.0, "topcoat": CANT + 13.0}   # flashing-coat apron, from the wall face: 12" past the cant toe   VERIFIED (12" min)
APRON_X = TW / 2 + 12.0             # ... and 12" either side of the tube                  VERIFIED (12" min)
FL_LINE = SLOPE + MT / math.sqrt(2)            # centre-line of the flange lying on the flashing: y + z = FL_LINE
TUBE_Z0 = FL_LINE - FT - MT / 2                # underside of the tube's bottom sheet, so the sheet runs into the flange at the wall face
Z_IN0, Z_IN1 = TUBE_Z0 + MT, TUBE_Z0 + MT + TH # clear opening, bottom / top
Z_OUT1 = Z_IN1 + MT                            # top of the tube's top sheet
Y_OUT, Y_IN = -PT - EXT, FT                    # tube ends: past the exterior face / flush with the flashing on the roof side
XO = TW / 2 + MT                               # tube outer half-width
X0, X1 = -L / 2, L / 2


def B(name, layer, y0, y1, z0, z1, mat, x0=X0, x1=X1):
    """Axis-aligned slab: y0..y1 from the wall face (+ toward the roof), z0..z1 height, x0..x1 along the wall. Inches."""
    return box(name, layer, (x1 - x0) * IN, (y1 - y0) * IN, (z1 - z0) * IN, (x0 + x1) / 2 * IN, (y0 + y1) / 2 * IN, (z0 + z1) / 2 * IN, mat)


def slab_between(name, layer, p, q, t, mat, x0=X0, x1=X1):
    """Sheet of thickness t whose centre-line runs from (y,z)=p to q in the wall-normal plane — the 45° cant faces."""
    (y0, z0), (y1, z1) = p, q
    ln = math.hypot(y1 - y0, z1 - z0); ang = math.atan2(z1 - z0, y1 - y0)
    o = box(name, layer, (x1 - x0) * IN, ln * IN, t * IN, (x0 + x1) / 2 * IN, (y0 + y1) / 2 * IN, (z0 + z1) / 2 * IN, mat)
    o.rotation_euler = (ang, 0, 0)
    return o


def on_line(name, layer, c, y0, y1, t, mat, x0=X0, x1=X1):
    """A 45° sheet whose centre-line is y + z = c, from y0 to y1 (from the wall face)."""
    return slab_between(name, layer, (y0, c - y0), (y1, c - y1), t, mat, x0, x1)


def prism(name, layer, pts, mat, x0=X0, x1=X1):
    """Triangular prism along x from a (y,z) triangle in inches — the cant."""
    v = [(x0 * IN, y * IN, z * IN) for (y, z) in pts] + [(x1 * IN, y * IN, z * IN) for (y, z) in pts]
    f = [(0, 2, 1), (3, 4, 5), (0, 1, 4, 3), (1, 2, 5, 4), (2, 0, 3, 5)]
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], f); me.validate()
    o = bpy.data.objects.new(name, me); o.data.materials.append(mat)
    return link(o, layer, name)


def coat(layer, i):
    """One coat as nested sheets, i = 1 primer, 2 Flex, 3 topcoat. Field (foot + the 12" apron) → over the cant (over the
    flange in the tube's bay) → up the flashing round the opening to the coping; and the lining of the tube interior.
    Nothing on the exterior — the drawing's coats stop at the exterior termination."""
    d0, d1 = (i - 1) * COAT, i * COAT
    mat = M(layer if layer != "topcoat" else "thane")
    for tag, (a, b) in (("left", (X0, -APRON_X)), ("right", (APRON_X, X1))):
        B(f"{layer}_foot_{tag}", layer, FOOT + d0, FIELD[layer], FT + d0, FT + d1, mat, a, b)          # base coat past the flashing foot
    B(f"{layer}_apron", layer, FOOT + d0, APRON[layer], FT + d0, FT + d1, mat, -APRON_X, APRON_X)      # flashing coat: 12" past the cant onto the field
    B(f"{layer}_foot_over", layer, CANT, FOOT + d1, FT + d0, FT + d1, mat)                              # over the foot itself
    c = SLOPE + math.sqrt(2) * (d0 + COAT / 2)                                                          # this coat's centre-line over the cant
    for tag, (a, b) in (("left", (X0, -XO)), ("right", (XO, X1))):
        on_line(f"{layer}_cant_{tag}", layer, c, c - (FT + d0 + COAT / 2), d0 + COAT / 2, COAT, mat, a, b)
    cf = FL_LINE + MT / math.sqrt(2) + math.sqrt(2) * (d0 + COAT / 2)                                   # over the flange, MT further out
    on_line(f"{layer}_flange", layer, cf, cf - (FT + d0 + COAT / 2), FT + d0, COAT, mat, -XO, XO)
    hx = TW / 2 - d0                                                                                    # the opening in the wall coats, nested inward
    B(f"{layer}_wall_left", layer, FT + d0, FT + d1, CANT, TOP, mat, X0, -hx)
    B(f"{layer}_wall_right", layer, FT + d0, FT + d1, CANT, TOP, mat, hx, X1)
    B(f"{layer}_wall_above", layer, FT + d0, FT + d1, Z_IN1 - d0, TOP, mat, -hx, hx)
    # tube lining: bottom and top the full clear width, sides between them; runs from the exterior end to meet the wall coat
    B(f"{layer}_lining_bottom", layer, Y_OUT, Y_IN + d1, Z_IN0 + d0, Z_IN0 + d1, mat, -hx, hx)
    B(f"{layer}_lining_top", layer, Y_OUT, Y_IN + d1, Z_IN1 - d1, Z_IN1 - d0, mat, -hx, hx)
    B(f"{layer}_lining_left", layer, Y_OUT, Y_IN + d1, Z_IN0 + d1, Z_IN1 - d1, mat, -hx, -(TW / 2 - d1))
    B(f"{layer}_lining_right", layer, Y_OUT, Y_IN + d1, Z_IN0 + d1, Z_IN1 - d1, mat, TW / 2 - d1, hx)


reset_scene()

# (E) parapet section in four pieces round the tube — generic; the app re-skins it with the building's wall material
B("parapet_left", "existing", -PT, 0, 0, PH, M("wall"), X0, -XO)
B("parapet_right", "existing", -PT, 0, 0, PH, M("wall"), XO, X1)
B("parapet_below", "existing", -PT, 0, 0, TUBE_Z0, M("wall"), -XO, XO)
B("parapet_above", "existing", -PT, 0, Z_OUT1, PH, M("wall"), -XO, XO)

# (E) cant and (E) base flashing (the roof membrane carried up the wall): foot, over the cant, up the wall round the tube
prism("cant", "existing", [(0, 0), (CANT, 0), (0, CANT)], M("wood"))
B("flashing_foot", "existing", CANT, FOOT, 0, FT, M("membrane"))
slab_between("flashing_cant", "existing", (CANT, FT / 2), (0, CANT + FT / 2), FT, M("membrane"))
B("flashing_wall_left", "existing", 0, FT, CANT, PH, M("membrane"), X0, -XO)
B("flashing_wall_right", "existing", 0, FT, CANT, PH, M("membrane"), XO, X1)
B("flashing_wall_above", "existing", 0, FT, Z_OUT1, PH, M("membrane"), -XO, XO)

# (E) scupper tube: four sheets open at both ends, bottom sheet bent down over the cant on the roof side
B("tube_bottom", "existing", Y_OUT, Y_IN, TUBE_Z0, Z_IN0, M("coping"), -XO, XO)
B("tube_top", "existing", Y_OUT, Y_IN, Z_IN1, Z_OUT1, M("coping"), -XO, XO)
B("tube_left", "existing", Y_OUT, Y_IN, TUBE_Z0, Z_OUT1, M("coping"), -XO, -TW / 2)
B("tube_right", "existing", Y_OUT, Y_IN, TUBE_Z0, Z_OUT1, M("coping"), TW / 2, XO)
on_line("tube_flange", "existing", FL_LINE, FT, FT + FLANGE / math.sqrt(2), MT, M("coping"), -XO, XO)

# Exterior collar plate round the tube, against the exterior face (3D concept)
CX, CZ0, CZ1 = XO + COLLAR, TUBE_Z0 - COLLAR, Z_OUT1 + COLLAR
B("collar_top", "existing", -PT - MT, -PT, Z_OUT1, CZ1, M("coping"), -CX, CX)
B("collar_bottom", "existing", -PT - MT, -PT, CZ0, TUBE_Z0, M("coping"), -CX, CX)
B("collar_left", "existing", -PT - MT, -PT, TUBE_Z0, Z_OUT1, M("coping"), -CX, -XO)
B("collar_right", "existing", -PT - MT, -PT, TUBE_Z0, Z_OUT1, M("coping"), XO, CX)

# New sealant at the exterior termination: a bead where the collar meets the wall, all round (prep / primer stage)
B("sealant_bead_bottom", "primer", -PT - BEAD, -PT, CZ0 - BEAD, CZ0, M("seal"), -CX - BEAD, CX + BEAD)   # the bead the drawing shows
B("sealant_bead_top", "primer", -PT - BEAD, -PT, CZ1, CZ1 + BEAD, M("seal"), -CX - BEAD, CX + BEAD)
B("sealant_bead_left", "primer", -PT - BEAD, -PT, CZ0, CZ1, M("seal"), -CX - BEAD, -CX)
B("sealant_bead_right", "primer", -PT - BEAD, -PT, CZ0, CZ1, M("seal"), CX, CX + BEAD)

coat("primer", 1)
coat("flex", 2)
coat("topcoat", 3)

finalize("overflow-scupper-D-4-TYP")
