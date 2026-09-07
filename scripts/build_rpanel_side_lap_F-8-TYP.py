"""
build_rpanel_side_lap_F-8-TYP.py — metal R-panel side lap per RMI detail F-8-TYP (METAL "R" PANEL SIDE LAP –
TYPICAL, 11/05/24) with F8-2-FT-3D and F8-10-FT-3D (ROOF / FIELD / SIDE LAPS – CONCEPT DRAWING, 9/1/21) as reference.

    blender -b --python scripts/build_rpanel_side_lap_F-8-TYP.py

The model is a 16" x 6-ft SECTION OF ROOF PANEL centred on one side lap: two panels overlapping at a major rib, the
lap fastened through the crest. The app splices it into the warehouse's R-panel slope (buildGable, cfg.lapModel):
the panel field and the rib/lap overlays stop at the bay ends and this section fills the bay, so the rib profile
and the three coat profiles are the SAME numbers as `LAP` / `lapProfile()` in index.html — change them together or
the seams show at the bay ends. Axes: x across the panels, y along the slope (the loader maps Blender +y to
slope-local -z, i.e. up-slope), z the panel normal. The section is symmetric in y, so orientation does not matter.

What the 2D drawing says (VERIFIED):
  * (E) min 24 ga. metal roof panels, two overlapping at a major rib; fastener through the crest of the lap rib.
  * Replace damaged, loose or missing fasteners. Do not overdrive fasteners (note 3).
  * Treat rusted metal with an RMI approved application; rust with pin holes or lost structural integrity is
    patched, overlaid or replaced (note 10).
  * Bead of RMI approved sealant at all voids (drawn at the foot of the lap, where the overlapping edge meets the flat).
  * Clean, prepare and prime per the Spec Guide Manual for the panel type (note 11).
  * RMI-Flex flashing coat fully encapsulates the fasteners and the lap — crest, both rib slopes and onto the flat
    both sides.
  * RMI-Thane / RMI-White over all. (Optional) RMI-Flex base coat to the whole field.
  * Notes 7/8: the detail applies to all seams, laps and flashing transitions on any panel configuration.
  * Note 12: ill-fitting overlapping panels with excessive movement can void the warranty.
  * The concept renders show a row of fasteners along the crest of the lap rib under one continuous Flex band.

ASSUMED (not dimensioned on the drawing): the rib profile (6.6" base, 3" crest, 1.32" high — a generic 12" o.c.
R-panel major rib, the same trapezoid the app draws), sheet thickness drawn at 0.05" so the lap reads (24 ga. is
0.024"), the 1" underlap and 3/4" overlap lips, the lap fastener (5/8" EPDM washer, hex head) at 12" o.c., how far
the Flex runs onto the flat (2" past the rib base), that the primer band equals the Flex band, which side of the rib
the sealant bead sits, and every coat thickness (visual: the pan topcoat is 0.36" so it meets the app's field
overlay flush).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bmesh
from rmi_blender import IN, M, box, cyl, hemisphere, link, reset_scene, finalize

# ---------------------------------------------------------------- the bay this fills and the rib it continues (must match LAP in index.html)
BAY_W, BAY_L = 16.0, 72.0           # section size across / along the slope (inches)
RIB_B, RIB_T, RIB_H = 6.6, 3.0, 1.32  # major rib: base width, crest width, height          ASSUMED (generic R-panel; app trap(0.55,0.25,0.11) ft)
TP, TF, TT = 0.08, 0.30, 0.36       # visual coat thicknesses: primer, Flex, topcoat      ASSUMED (TT = the app's 0.03-ft field overlay)
FOOT = 2.0                          # primer/Flex run this far past the rib base onto the flat   ASSUMED
LIFT_P, LIFT_F, LIFT_T = 0.018, 0.024, 0.036   # the app floats its lap overlays 0.0015/0.002/0.003 ft off the pan; same here so the profiles meet

# ---------------------------------------------------------------- the detail
SHEET_T = 0.05                      # drawn sheet thickness (24 ga. = 0.024" — VERIFIED min gauge, thickness exaggerated to read)
LIP_A, LIP_B = 1.0, 0.75            # underlap lip past the rib base (under the overlapping panel) / overlap lip onto the flat   ASSUMED
FAST_Y = [-30, -18, -6, 6, 18, 30]  # lap fasteners through the crest at 12" o.c.            ASSUMED spacing (row of fasteners — VERIFIED from F8-10-FT-3D)
WASHER_R, WASHER_H = 5 / 16, 0.06   # 5/8" EPDM-backed washer                                  ASSUMED size
HEAD_R, HEAD_H = 0.19, 0.20         # hex head                                                 ASSUMED size
BEAD_R = 0.12                       # sealant bead at the lap voids                            VERIFIED bead; size ASSUMED
DOME_R = 0.5                        # Flex mound over each encapsulated fastener               visual
RUST = [(-5.0, 12.0, 1.3), (5.6, -22.0, 1.0)]   # (x, y, r) rust patches on the pans; the app fades them out during prep


def rib_xs(off):
    """x of the +x rib side, offset outward by `off`, as a function of height y (inches)."""
    hw, tw, H = RIB_B / 2, RIB_T / 2, RIB_H
    ln = math.hypot(tw - hw, H); nx, ny = H / ln, (hw - tw) / ln
    p0 = (hw + off * nx, off * ny); p1 = (tw + off * nx, H + off * ny)
    return lambda y: p0[0] + (y - p0[1]) * (p1[0] - p0[0]) / (p1[1] - p0[1])


def lap_profile(off, foot_x):
    """Closed (x, z) polygon of a coat over the rib: the rib trapezoid offset outward by `off`, flat feet out to
    ±foot_x at height `off`, closed along z=0. Identical to lapProfile() in index.html."""
    xs = rib_xs(off); H = RIB_H
    right = [(foot_x, 0.0), (foot_x, off), (xs(off), off), (xs(H + off), H + off)]
    return [(-x, y) for x, y in reversed(right)] + right


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
hw, tw, H, t = RIB_B / 2, RIB_T / 2, RIB_H, SHEET_T
Y0, Y1, X1 = -BAY_L / 2, BAY_L / 2, BAY_W / 2

# (E) panels: A (underlap, -x) is the bare rib with a lip under B; B (overlap, +x) nests over A's rib by one sheet
# and lands on A's pan with a short lip. Pan and rib are separate meshes so the app can skin them with its own
# field and rib materials (the sheets are split at the rib base, not at the lap).
sheet("panel_a", "existing", [(-X1, 0), (-hw, 0)], t, Y0, Y1, M("panel"))
sheet("rib_a", "existing", [(-hw, 0), (-tw, H), (tw, H), (hw, 0), (hw + LIP_A, 0)], t, Y0, Y1, M("panel"))
xb = rib_xs(t); step = hw + LIP_A + 0.2
sheet("rib_b", "existing", [(-(xb(t) + LIP_B), t), (-xb(t), t), (-xb(H + t), H + t), (xb(H + t), H + t), (xb(t), t), (step, t), (step, 0)], t, Y0, Y1, M("panel"))
sheet("panel_b", "existing", [(step, 0), (X1, 0)], t, Y0, Y1, M("panel"))

# Lap fasteners through the crest: EPDM washer + hex head (replace damaged/loose/missing — VERIFIED)
for i, y in enumerate(FAST_Y):
    cyl(f"fastener_{i}_washer", "existing", WASHER_R * IN, WASHER_H * IN, 0, y * IN, (H + t + WASHER_H / 2) * IN, M("fast"), verts=24)
    cyl(f"fastener_{i}_head", "existing", HEAD_R * IN, HEAD_H * IN, 0, y * IN, (H + t + WASHER_H + HEAD_H / 2) * IN, M("fast"), verts=6)

# Rust on the pans — thin discs the app fades out through the prep stage
for i, (x, y, r) in enumerate(RUST):
    cyl(f"rust_{i}", "existing", r * IN, 0.01 * IN, x * IN, y * IN, 0.006 * IN, M("rust"), verts=24)

# Sealant bead at the lap voids: along B's lip on A's pan and along B's step onto A's underlap (prep work — shown from prep)
for i, x in enumerate((-(xb(t) + LIP_B) - 0.06, step + 0.06)):
    b = cyl(f"sealant_{i}", "primer", BEAD_R * IN, BAY_L * IN, x * IN, 0, (BEAD_R - 0.02) * IN, M("seal"), verts=12); b.rotation_euler = (math.pi / 2, 0, 0)

# Coats: each one the rib profile offset by its thickness, feet 2" past the rib base (primer), and each coat wrapping
# the last. Same polygons as the app's lap overlays, so the section meets them flush at both ends of the bay.
F_P = hw + FOOT; F_F = F_P + TF; F_T = F_F + TT
prism("primer", "primer", lap_profile(TP, F_P), Y0, Y1, M("primer"), LIFT_P)
prism("flex", "flex", lap_profile(TP + TF, F_F), Y0, Y1, M("flex"), LIFT_F)
prism("topcoat", "topcoat", lap_profile(TP + TF + TT, F_T), Y0, Y1, M("thane"), LIFT_T)
for i, y in enumerate(FAST_Y):   # the fasteners under the Flex read as mounds; the topcoat follows them
    hemisphere(f"flex_dome_{i}", "flex", DOME_R * IN, 0, y * IN, (H + TP + TF + LIFT_F) * IN, M("flex"))
    hemisphere(f"topcoat_dome_{i}", "topcoat", (DOME_R + TT) * IN, 0, y * IN, (H + TP + TF + TT + LIFT_T) * IN, M("thane"))
# Field topcoat over the bare pans, top at TT so it meets the app's field overlay flush at the bay edges
for sg, side in ((-1, "l"), (1, "r")):
    w = X1 - F_T + 0.1
    box(f"topcoat_pan_{side}", "topcoat", w * IN, BAY_L * IN, TT * IN, sg * (X1 - w / 2) * IN, 0, TT / 2 * IN, M("thane"))

finalize("rpanel-side-lap-F-8-TYP")
