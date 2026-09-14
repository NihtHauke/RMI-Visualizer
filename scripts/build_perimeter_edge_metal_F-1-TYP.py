"""
build_perimeter_edge_metal_F-1-TYP.py — perimeter edge metal per RMI detail F-1-TYP (PERIMETER EDGE METAL – TYPICAL,
11/05/24; the library file is named "F1-1-TYP Perimeter Edge Metal") with F1-34-FT-3D (PERIMETER EDGE – CONCEPT
DRAWING, 9/1/21) as reference.

    blender -b --python scripts/build_perimeter_edge_metal_F-1-TYP.py

A 4-ft SECTION of the roof edge. The building wall and the field are not in the model: everything hangs off the
wall's outer face at y=0, with +y toward the roof and z=0 at the roof surface. The app splices it into the office's
code-drawn edge-metal run (addEdgeMetal in index.html), which draws the same cross-section from the same numbers
(the EM constants) — keep the two in step or the seams show. On a metal-edged block the app's field membrane and its
three coat sheets run out to the wall face, so the model's coats stop at y=0, where those sheets begin, at the sheets'
own heights (0.6", 0.96", 1.32" above the roof).

What the drawings say (VERIFIED):
  * (E) perimeter edge metal with cleat (shown for illustration). Replace damaged, ill-fitting or severely rusted metal.
  * The (E) roof system runs under the flange and is stripped in over it; the stripping steps down past the flange
    onto the field. Confirm seam and flashing integrity, repair as required.
  * Note 10: clean, prepare and prime per the Spec Guide Manual for each type of (E) roof system and surface.
  * RMI-Flex vapor barrier-base coat over the stripped flange and on across the field; RMI-Thane / White over the Flex.
  * Note 7: edge metal and cleats must meet code / SMACNA for wind uplift or the edge is excluded from warranty.
  * Note 8: all (E) BUR, mod-bit, EPDM, PVC, TPO and concrete deck systems.
  * F1-34-FT-3D note 10: roof coating (RMI-Thane or White Plus) to all surface areas.
  * No raised gravel stop on F-1-TYP: the flange runs flat to the edge (the raised stop is F-2-TYP).

ASSUMED (not on the drawings, which are not to scale and carry no dimensions):
  * 4" tape over the metal-to-membrane joint at the roof edge, 2" onto the stripping and 2" down the fascia.
  * Flex carried down the fascia face to the drip. The 2D drawing ends both coats at the roof edge.
  * Exposed face fasteners 12" o.c., each encapsulated in Flex. The drawing shows only the cleat fastener, behind the fascia.
  * Every size: 4" flange; 4" fascia standing 1/2" off the wall; 3/8" hem hooked on the cleat's kick; stripping 4" past
    the flange; cleat screws 12" o.c.; the sheet and coat thicknesses.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bmesh
from rmi_blender import IN, M, box, cyl, reset_scene, finalize

# ---------------------------------------------------------------- dimensions (inches; ASSUMED unless noted) — same as EM in index.html
L          = 48.0                   # modelled section along the edge
MT         = 0.06                   # sheet metal (24 ga. drawn thicker so it reads)
FLANGE     = 4.0                    # flange onto the roof, from the wall face
FACE_OFF   = 0.5                    # fascia stand-off from the wall face — room for the cleat (drawing: cleat behind the fascia, VERIFIED)
FACE_H     = 4.0                    # fascia drop below the roof surface
HEM        = 0.375                  # hem turned in and up at the drip, hooked on the cleat
CLEAT_T, CLEAT_TOP, CLEAT_BOT, KICK = 0.04, -0.25, -3.2, 0.25    # continuous cleat on the wall face, kicked out at the bottom
PLY_T      = 0.125                  # (E) stripping over the flange (VERIFIED that it is there; thickness ASSUMED)
PLY_END    = 8.0                    # stripping steps down past the flange and ends 4" onto the field
TAPE, TAPE_T = 2.0, 0.03            # tape 2" each side of the edge joint (the 4" band of W-1-TYP)
FAST_X     = (-18.0, -6.0, 6.0, 18.0)                             # face fasteners 12" o.c.
FAST_Z, FAST_R, FAST_H = -2.75, 0.156, 0.12
SCREW_X    = (-12.0, 0.0, 12.0)     # cleat screws (VERIFIED that the cleat is fastened to the support; spacing ASSUMED)
SCREW_Z, SCREW_R, SCREW_H = -1.75, 0.2, 0.06
DAB_R, DAB_Y = 0.55, (0.70, 0.98)   # Flex dab over each face fastener, out from the wall face
# per coat: top slab z-range (the app's field sheet sits at its top), face slab y-range out from the wall face, bottom of the face slab
COATS = {"primer":  ((0.30, 0.60), (0.70, 0.76), -3.90),
         "flex":    ((0.66, 0.96), (0.78, 0.88), -3.95),
         "topcoat": ((1.02, 1.32), (1.00, 1.10), -4.00)}

YO = FACE_OFF + MT                  # outer face of the fascia
X0, X1 = -L / 2 * IN, L / 2 * IN


def B(name, layer, y0, y1, z0, z1, mat, x0=X0, x1=X1):
    """Axis-aligned slab spanning y0..y1 (from the wall face), z0..z1 (height), x0..x1 (along the edge). Inches in, metres out."""
    return box(name, layer, (x1 - x0), (y1 - y0) * IN, (z1 - z0) * IN, (x0 + x1) / 2, (y0 + y1) / 2 * IN, (z0 + z1) / 2 * IN, mat)


def slab_between(name, layer, p, q, t, mat, x0=X0, x1=X1):
    """Sheet of thickness t (inches) whose centre-line runs from (y,z)=p to q in the section plane."""
    (y0, z0), (y1, z1) = p, q
    ln = math.hypot(y1 - y0, z1 - z0); ang = math.atan2(z1 - z0, y1 - y0)
    o = box(name, layer, x1 - x0, ln * IN, t * IN, (x0 + x1) / 2, (y0 + y1) / 2 * IN, (z0 + z1) / 2 * IN, mat)
    o.rotation_euler = (ang, 0, 0)
    return o


def fastener(name, layer, r, h, x, y_mid, z, mat, verts=16):
    """Cylinder with its axis along y (normal to the wall face)."""
    o = cyl(name, layer, r * IN, h * IN, x * IN, y_mid * IN, z * IN, mat, verts=verts)
    o.rotation_euler = (math.pi / 2, 0, 0)
    return o


reset_scene()
metal = M("coping")

# (E) edge metal: flange flat on the roof, fascia down the outside, hem at the drip hooked on the cleat
B("flange", "existing", -YO, FLANGE, 0, MT, metal)
B("fascia", "existing", -YO, -FACE_OFF, -FACE_H, 0, metal)
slab_between("hem", "existing", (-YO + MT / 2, -FACE_H), (-YO + MT / 2 + HEM, -FACE_H + HEM), MT, metal)

# (E) continuous cleat on the wall face, screwed to the support, kicked out at the bottom
B("cleat", "existing", -CLEAT_T, 0, CLEAT_BOT, CLEAT_TOP, metal)
slab_between("cleat_kick", "existing", (-CLEAT_T / 2, CLEAT_BOT), (-CLEAT_T / 2 - KICK, CLEAT_BOT - KICK), CLEAT_T, metal)
for i, x in enumerate(SCREW_X):
    fastener(f"screw_{i}", "existing", SCREW_R, SCREW_H, x, -(CLEAT_T + SCREW_H / 2), SCREW_Z, M("fast"))

# (E) stripping: over the flange from the edge, stepping down past the flange onto the field (the app skins it to the roof surface)
B("ply_flange", "existing", -FACE_OFF, FLANGE + 0.25, MT, MT + PLY_T, M("membrane"))
B("ply_field", "existing", FLANGE, PLY_END, 0, PLY_T, M("membrane"))

# (E) face fasteners — ASSUMED (F-1-TYP draws only the concealed cleat fastener)
for i, x in enumerate(FAST_X):
    fastener(f"fastener_{i}", "existing", FAST_R, FAST_H, x, -(YO + FAST_H / 2), FAST_Z, M("fast"))

# Tape over the metal-to-membrane joint at the edge: 2" onto the stripping, 2" down the fascia (prep work: the app shows primer__tape from prep)
top = MT + PLY_T
B("tape_top", "primer", -(YO + TAPE_T), -YO + TAPE, top, top + TAPE_T, M("tape"))
B("tape_face", "primer", -(YO + TAPE_T), -YO, -TAPE, top, M("tape"))

# Coats: a top slab from the fascia out to the wall face (the field sheets take over from there) and a face slab down the fascia to the drip
for layer, ((z0, z1), (y0, y1), zb) in COATS.items():
    mat = M("thane" if layer == "topcoat" else layer)
    B(f"{layer}_top", layer, -y1, 0, z0, z1, mat)
    B(f"{layer}_face", layer, -y1, -y0, zb, z0, mat)

# Every face fastener encapsulated in Flex
for i, x in enumerate(FAST_X):
    fastener(f"flex_dab_{i}", "flex", DAB_R, DAB_Y[1] - DAB_Y[0], x, -(DAB_Y[0] + DAB_Y[1]) / 2, FAST_Z, M("flex"), verts=24)

# Open both ends of the section. The app's code run overlaps each end by 0.6 mm; an end face left there shows as a hairline across the seam.
bpy.context.view_layer.update()
for o in [o for o in bpy.data.objects if o.type == 'MESH']:
    mw = o.matrix_world; bm = bmesh.new(); bm.from_mesh(o.data)
    ends = [f for f in bm.faces if abs(abs((mw @ f.calc_center_median()).x) - X1) < 1e-5 and abs((mw.to_3x3() @ f.normal).normalized().x) > 0.99]
    if ends:
        bmesh.ops.delete(bm, geom=ends, context='FACES'); bm.to_mesh(o.data)
    bm.free()

finalize("perimeter-edge-metal-F-1-TYP")
