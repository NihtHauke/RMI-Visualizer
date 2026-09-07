"""
build_standing_seam_F-9-TYP.py — metal panel standing seam per RMI detail F-9-TYP (METAL PANEL - STANDING SEAM –
TYPICAL, 11/05/24), with F-20-TYP (DOWNSLOPE - OVERLAY PANEL @ (E) STANDING SEAM, 11/05/24) for the seam lap
condition and B-1-F10-22-3D as the 3D reference.

    blender -b --python scripts/build_standing_seam_F-9-TYP.py

The model is a 24" x 6-ft SECTION OF ROOF centred on one standing seam: two pans turning up into a crimped
double-lock seam, a concealed clip in the throat, and the RMI-Flex shell over it. The app splices it into the
manufacturing building's standing-seam slope (buildGable, cfg.seamModel): the panel field, the seam and the seam
overlays stop at the bay ends and this section fills the bay, so the seam profile and the three coat profiles are
the SAME numbers as SEAM / SHELL in index.html — change them together or the seam shows a step at the bay ends.
Axes: x across the pans, y along the slope (the loader maps Blender +y to slope-local -z, i.e. up-slope), z the
panel normal. The section is symmetric in y, so orientation does not matter.

What the 2D drawing says (VERIFIED):
  * (E) min 24 ga. metal roof panels; a standing seam between pans, shown as a crimped double-lock — vertical legs
    with the tops folded together into a cap. No exposed fasteners at the seam: the clips are concealed.
  * "(E) TYPICAL STANDING SEAM SHOWN FOR ILLUSTRATION. CONFIGURATION MAY VARY. (SEE NOTE No. 11)."
  * Treat rusted metal with an RMI approved application (note 10); rust with pin holes or lost structural integrity
    is patched, overlaid or replaced.
  * Note 11: LOOSE OR IMPROPER CRIMPING MAY RESULT IN EXCESSIVE VOIDS OR STRUCTURAL MOVEMENT EXCEEDING RMI MATERIAL
    PERFORMANCE CRITERIA AND VOID WARRANTY. RE-CRIMP STANDING SEAM AS REQUIRED TO MEET MFG. ORIGINAL CONFIGURATION
    REQUIREMENTS.  -> the open crimp is modelled as a void at the cap joint and closed during the PREP stage.
  * Note 12: clean, prepare and prime per the Spec Guide Manual for each type of (E) panel system and surface.
  * "RMI-FLEX VAPOR BARRIER-FLASHING COAT TO FULLY STANDING SEAM" — the Flex is a shell over the whole seam: over
    the cap, down both legs and out onto the flat on both sides.
  * "(OPTIONAL) RMI-FLEX VAPOR BARRIER-BASE COAT APPLIED TO FIELD" — a separate band on the pan, optional.
  * RMI-THANE / RMI-WHITE over everything, seam and field alike.
  * Notes 7/8: the detail applies equally to all seams, laps and flashing transitions, on any panel configuration.

ASSUMED (the drawing is NOT TO SCALE and carries no dimensions): every dimension below. The seam silhouette
(1.68" wide legs 2.4" tall under a 3.12" wide, 0.72" tall folded cap) is the app's own SEAM profile, itself a
generic 24"-o.c. double-lock; sheet thickness drawn at 0.05" so the plies read (24 ga. is 0.024" — the min gauge
is VERIFIED, the drawn thickness is not); which pan's cap laps over the other and where the joint falls; the
interlocking return plies inside the cap; the concealed clip (size, and 24" o.c. spacing); how far the Flex runs
onto the flat; and every coat thickness.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bmesh
from rmi_blender import IN, M, box, cyl, link, reset_scene, finalize

# ---------------------------------------------------------------- the bay this fills (must match SEAMD in index.html)
BAY_W, BAY_L = 24.0, 72.0           # section size across / along the slope (inches) — one full 24" o.c. panel width

# ---------------------------------------------------------------- the seam silhouette (must match SEAM in index.html)
LEG_HW = 0.84                       # half-width of the pair of vertical legs   (app SEAM +/-0.07 ft)
LEG_Z = 2.40                        # top of the legs / underside of the cap    (app SEAM 0.2 ft)
HEAD_HW = 1.56                      # half-width of the folded cap              (app SEAM +/-0.13 ft)
HEAD_Z = 3.12                       # top of the cap                            (app SEAM 0.26 ft)

# ---------------------------------------------------------------- the coats (must match SHELL in index.html)
SHELL_P = (0.03, 0.26)              # SHELL(o, f) for primer, in FEET — the app's own numbers
SHELL_F = (0.06, 0.30)              # ... Flex
SHELL_T = (0.10, 0.34)              # ... topcoat
LIFT_P, LIFT_F, LIFT_T = 0.018, 0.024, 0.036   # the app floats its seam overlays 0.0015/0.002/0.003 ft off the pan
TT = 0.36                           # field topcoat thickness = the app's 0.03-ft field overlay

# ---------------------------------------------------------------- the detail
SHEET_T = 0.05                      # drawn sheet thickness (24 ga. = 0.024" — VERIFIED min gauge, exaggerated to read)
APEX = 0.22                         # x of the cap joint: pan A's cap laps this far past centre     ASSUMED
FOLD_A = [(-1.20, 3.02), (-1.20, 2.62), (0.50, 2.62)]    # A's return ply inside the cap (the lock) ASSUMED
FOLD_B = [(1.20, 3.02), (1.20, 2.78), (-0.35, 2.78)]     # B's return ply, interlocking with A's    ASSUMED
CLIP_Y = [-24.0, 0.0, 24.0]         # concealed clips at 24" o.c.                                   ASSUMED spacing
CLIP_W, CLIP_L, CLIP_T = 2.4, 1.4, 0.06   # clip base plate, under the pan so nothing of it shows    ASSUMED
CLIP_BASE_Z = -0.08                       # its centre: below the pan's underside (pan is -SHEET_T..0)
CLIP_TAB_W, CLIP_TAB_Z = 0.12, 2.30       # tab folded up inside the seam                            ASSUMED
SCREW_R, SCREW_H = 0.19, 0.16             # clip screw into the purlin                               ASSUMED
GAPE = 0.55                               # how far a loose cap stands off the crimped height (note 11)  ASSUMED
VOID_X0, VOID_X1 = APEX, HEAD_HW - 0.03   # the open void between A's cap and B's un-driven one
VOID_Z0, VOID_Z1 = HEAD_Z + 0.01, HEAD_Z + GAPE - SHEET_T - 0.01
CRIMP_W, CRIMP_T = 0.40, 0.06             # the dressed crimp line after re-crimping                 ASSUMED size


def shell(o, f):
    """SHELL(o, f) from index.html — the coat profile over a standing seam — as a closed (x, z) polygon in INCHES.
    Flat foot out to +/-(0.16+f) ft, up the legs at +/-(0.12+o), out over the cap at +/-(0.18+o)."""
    right = [(0.16 + f, 0.0), (0.16 + f, 0.03 + o), (0.12 + o, 0.03 + o),
             (0.12 + o, 0.20), (0.18 + o, 0.20), (0.18 + o, 0.31 + o)]
    right = [(x * 12, z * 12) for x, z in right]
    return [(-x, z) for x, z in reversed(right)] + right


def offset_polyline(pts, d):
    """Offset an open (x, z) polyline by `d` toward the right-hand side of travel (mitred corners)."""
    n = len(pts); segn = []
    for i in range(n - 1):
        dx, dz = pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]; ln = math.hypot(dx, dz)
        segn.append((dz / ln, -dx / ln))
    out = []
    for i in range(n):
        if i == 0:
            nx, nz = segn[0]
        elif i == n - 1:
            nx, nz = segn[-1]
        else:
            a, b = segn[i - 1], segn[i]; dot = a[0] * b[0] + a[1] * b[1]
            nx, nz = (a[0] + b[0]) / (1 + dot), (a[1] + b[1]) / (1 + dot)
        out.append((pts[i][0] + d * nx, pts[i][1] + d * nz))
    return out


def _mesh(name, layer, verts, faces, mat):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.validate()
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); o.data.materials.append(mat)
    return link(o, layer, name)


def prism(name, layer, poly, y0, y1, mat, lift=0.0):
    """A closed (x, z) polygon (inches) extruded along y from y0 to y1, lifted by `lift`."""
    n = len(poly)
    v = [(x * IN, y0 * IN, (z + lift) * IN) for x, z in poly] + [(x * IN, y1 * IN, (z + lift) * IN) for x, z in poly]
    f = [tuple(range(n)), tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return _mesh(name, layer, v, f, mat)


def sheet(name, layer, pts, t, y0, y1, mat):
    """A bent sheet: open polyline `pts` is its OUTER surface, thickness `t` to the right of travel."""
    return prism(name, layer, pts + list(reversed(offset_polyline(pts, t))), y0, y1, mat)


reset_scene()
t = SHEET_T
Y0, Y1, X1 = -BAY_L / 2, BAY_L / 2, BAY_W / 2

# (E) panels: each pan runs out flat, turns up into a leg, flares out at the top and folds across into the cap.
# A (-x) caps first and laps APEX past centre; B (+x) butts to it, so the crimp line reads off-centre the way a
# folded cap does. Traversed so the sheet thickness always falls on the inboard/underside — see sheet().
# The pan runs as one sheet right under the seam: the roof surface is continuous, so the seam encloses a closed
# cavity (the clip lives in it, out of sight) and there is neither a slot through the deck nor a butt line for the
# clip to show through. Which pan owns which side of the joint is hidden under the seam either way.
# Pans are named panel_* and the seam rib_* so the app can skin them with its own field and rib materials.
sheet("panel_pans", "existing", [(-X1, 0), (X1, 0)], t, Y0, Y1, M("panel"))
sheet("rib_seam_a", "existing",
      [(-LEG_HW, 0), (-LEG_HW, LEG_Z), (-HEAD_HW, LEG_Z), (-HEAD_HW, HEAD_Z), (APEX, HEAD_Z)], t, Y0, Y1, M("panel"))
B_TAIL = [(HEAD_HW, LEG_Z), (LEG_HW, LEG_Z), (LEG_HW, 0)]
sheet("rib_after_seam_b", "existing", [(APEX, HEAD_Z), (HEAD_HW, HEAD_Z)] + B_TAIL, t, Y0, Y1, M("panel"))
sheet("rib_before_seam_b", "existing",   # loose: B's fold has not been driven down, so its cap stands GAPE proud
      [(APEX, HEAD_Z + GAPE), (HEAD_HW, HEAD_Z + GAPE)] + B_TAIL, t, Y0, Y1, M("panel"))

# The double lock: each cap turns back down and hooks under the other. Enclosed by the cap, so it shows in section view.
sheet("rib_fold_a", "existing", FOLD_A, t, Y0, Y1, M("panel"))
sheet("rib_fold_b", "existing", FOLD_B, t, Y0, Y1, M("panel"))

# Concealed clip: base plate under the pan, tab folded up inside the seam, screw down into the purlin. Nothing of
# it shows from above — that is the point of a standing seam — so both parts are enclosed and read only in section.
for i, y in enumerate(CLIP_Y):
    box(f"fastener_clip_{i}_base", "existing", CLIP_W * IN, CLIP_L * IN, CLIP_T * IN, 0, y * IN, CLIP_BASE_Z * IN, M("fast"))
    box(f"fastener_clip_{i}_tab", "existing", CLIP_TAB_W * IN, (CLIP_L - 0.2) * IN, CLIP_TAB_Z * IN,
        0, y * IN, (CLIP_TAB_Z / 2) * IN, M("fast"))
    cyl(f"fastener_clip_{i}_screw", "existing", SCREW_R * IN, SCREW_H * IN, 0, y * IN, (CLIP_BASE_Z - 0.11) * IN, M("fast"), verts=6)

# Note 11 as a stage: a loose seam stands open at the cap joint (rib_before_seam_b above lifts pan B's cap by GAPE
# and this is the void behind it), and re-crimping to the manufacturer's profile closes it and dresses the joint.
# applyModels() shows _before_ parts until prep is half done and _after_ parts from there on.
box("void_before_crimp", "existing", (VOID_X1 - VOID_X0) * IN, BAY_L * IN, (VOID_Z1 - VOID_Z0) * IN,
    ((VOID_X0 + VOID_X1) / 2) * IN, 0, ((VOID_Z0 + VOID_Z1) / 2) * IN, M("castiron"))
box("rib_after_crimp", "existing", CRIMP_W * IN, BAY_L * IN, CRIMP_T * IN,
    APEX * IN, 0, (HEAD_Z - CRIMP_T / 2) * IN, M("panel"))

# Coats: the Flex shell fully encapsulates the seam — over the cap, down both legs, onto the flat both sides — with
# primer under it and the topcoat over it. Same polygons as the app's seam overlays, so the section meets them flush
# at both ends of the bay.
prism("primer", "primer", shell(*SHELL_P), Y0, Y1, M("primer"), LIFT_P)
prism("flex", "flex", shell(*SHELL_F), Y0, Y1, M("flex"), LIFT_F)
prism("topcoat", "topcoat", shell(*SHELL_T), Y0, Y1, M("thane"), LIFT_T)

# Field topcoat over the bare pans, top at TT so it meets the app's field overlay flush at the bay edges
F_T = (0.16 + SHELL_T[1]) * 12
for sg, side in ((-1, "l"), (1, "r")):
    w = X1 - F_T + 0.1
    box(f"topcoat_pan_{side}", "topcoat", w * IN, BAY_L * IN, TT * IN, sg * (X1 - w / 2) * IN, 0, TT / 2 * IN, M("thane"))

finalize("standing-seam-F-9-TYP")
