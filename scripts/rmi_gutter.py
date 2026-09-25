"""
rmi_gutter.py — the eave-hung box gutter shared by the W-7-TYP seam section (build_gutter_seam_W-7-TYP.py) and the
D-8-TYP inlet section (build_gutter_inlet_D-8-TYP.py). Both are 4-ft sections of the same gutter, spliced into the
code-drawn gutter run that hangs on the arena and airport-hangar eaves (index.html: GUT, gutterRun).

Frame (the eave-hung splice — see CLAUDE.md "Blender model conventions"):
  * x along the run, -24"..+24". Blender +y toward the building: the fascia face is y = 0 and the gutter hangs in -y,
    which the glTF export turns into the app's run-local +z (outward). z = 0 at the eave — the panel edge — and the
    gutter hangs below it. The app mounts the model with its origin on the eave line (y = H, z = ±W/2), so nothing
    here is rotated onto a slope: a gutter is level.
  * The code run draws the SAME cross-section from the same numbers (GUT in index.html) and over-laps each end of the
    model by 0.6 mm; the model's full-length parts are open at both ends (no cap faces), so no hairline shows at the
    seam. Anything that ends inside the section (a coat band, the outlet) is capped.
  * Part names: existing__gutter_* / tab_* / strap_* / rivet_* / outlet_* / strainer_* and primer__primer_*,
    flex__flex_*, topcoat__topcoat_* — the app skins `gutter`, `tab`, `strap`, `outlet` to the run's metal, `rivet`
    and `strainer` to its fastener metal, and the three coats to the scene's coat materials.

Neither sheet is to scale or carries a dimension, so EVERY size below is ASSUMED (a typical SMACNA-style box gutter);
only the coat extents on the sheets are VERIFIED, and they live in the two build scripts.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from rmi_blender import IN, M, box, cyl, link, band, smooth_by_angle

# ---------------------------------------------------------------- dimensions (inches; ASSUMED) — same as GUT in index.html
L          = 48.0                 # modelled section along the run
MT         = 0.06                 # sheet metal (24 ga. drawn thicker so it reads)
W          = 12.0                 # outside width, from the fascia face
D          = 8.0                  # outside depth below the eave (panel edge)
BACK_TOP   = -0.25                # top of the back wall, just under the panel edge
FRONT_TOP  = -0.75                # front wall 1/2" lower than the back, so an overflow goes out, not in
BEAD_W, BEAD_H = 0.75, 0.5        # rolled bead along the front top edge
STRAP_W, STRAP_T = 1.0, 0.125     # hanger strap, fascia to bead, over the gutter top
STRAP_X    = (-15.0, 15.0)        # 30" o.c. — the run's straps keep this phase past the section
TOPIN      = 0.5                  # coats stop this far below each wall's top edge
# coat offsets from the metal, inside the gutter (drawn thick so they read): the primer film, the Flex over it, and the
# topcoat film over bare metal; over a Flex band the topcoat rises to BAND_TOP and encloses primer and Flex
COATS      = {"primer": (0.02, 0.08), "flex": (0.08, 0.32), "topcoat": (0.02, 0.28)}
BAND_TOP   = 0.58

X0, X1 = -L / 2, L / 2


def interior_path():
    """The gutter's inside, walked with the metal on the left: down the back wall, across the floor, up the front.
    (u, v) = (Blender y, Blender z): u = 0 at the fascia face, negative outward; v = 0 at the eave."""
    return [(-MT, BACK_TOP - TOPIN), (-MT, -D + MT), (-(W - MT), -D + MT), (-(W - MT), FRONT_TOP - TOPIN)]


def prism_x(name, layer, pts, material, x0, x1, caps=False, sharp=35):
    """Prism of the closed (u, v) polygon `pts` (inches) from x0 to x1 (inches) along Blender x. Open-ended unless
    `caps` (an n-gon cap each end, so a concave coat band caps correctly)."""
    a = sum(p[0] * q[1] - q[0] * p[1] for p, q in zip(pts, pts[1:] + pts[:1]))
    if a < 0:
        pts = pts[::-1]
    n = len(pts)
    v = [(x0 * IN, u * IN, w * IN) for u, w in pts] + [(x1 * IN, u * IN, w * IN) for u, w in pts]
    f = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]      # wound outward for a CCW (u, v) polygon
    if caps:
        f.append(tuple(range(n))[::-1]); f.append(tuple(range(n, 2 * n)))
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], f); me.validate(); smooth_by_angle(me, sharp)
    o = bpy.data.objects.new(name, me); o.data.materials.append(material)
    return link(o, layer, name)


def rect(u0, u1, v0, v1):
    return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]


def B(name, layer, x0, x1, u0, u1, v0, v1, m):
    """Axis-aligned box spanning x0..x1 along the run, u0..u1 (toward the building), v0..v1 (height). Inches in."""
    return box(name, layer, (x1 - x0) * IN, (u1 - u0) * IN, (v1 - v0) * IN, (x0 + x1) / 2 * IN, (u0 + u1) / 2 * IN, (v0 + v1) / 2 * IN, m)


def trough(tag, x0, x1, inset=0.0, bead=True, metal=None, floor_caps=False):
    """The gutter metal from x0 to x1: back wall, floor, front wall and (unless `inset`) the front bead. `inset` nests the
    section inside another one by that much — the lapped tab of the next section (W-7-TYP). `floor_caps` closes the
    floor so a boolean can cut through it (the D-8-TYP outlet); open_ends() takes the caps off again."""
    m = metal or M("coping"); i = inset; layer = "existing"
    prism_x(f"{tag}_back",  layer, rect(-MT - i, -i, -D + i, BACK_TOP - i), m, x0, x1)
    prism_x(f"{tag}_floor", layer, rect(-W + i, -i, -D + i, -D + MT + i), m, x0, x1, caps=floor_caps)
    prism_x(f"{tag}_front", layer, rect(-W + i, -(W - MT) - i, -D + i, FRONT_TOP - i), m, x0, x1)
    if bead and not inset:
        prism_x(f"{tag}_bead", layer, rect(-(W + BEAD_W), -(W - MT), FRONT_TOP - BEAD_H, FRONT_TOP), m, x0, x1)


def straps(xs=STRAP_X):
    """Hanger straps over the gutter top, fascia to bead (ASSUMED 30" o.c.)."""
    for i, x in enumerate(xs):
        B(f"strap_{i}", "existing", x - STRAP_W / 2, x + STRAP_W / 2, -(W + BEAD_W), 0, BACK_TOP, BACK_TOP + STRAP_T, M("curb"))


def coat_u(layer, name, x0, x1, o0, o1, caps=True):
    """A coat film following the gutter's inside from x0 to x1, lying between offsets o0 and o1 off the metal."""
    m = M("thane" if layer == "topcoat" else layer)
    return prism_x(name, layer, band(interior_path(), o0, o1), m, x0, x1, caps=caps)


def apply_modifiers(o):
    """Bake an object's modifiers now (a boolean whose result still needs editing before export)."""
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    for md in list(o.modifiers):
        bpy.ops.object.modifier_apply(modifier=md.name)
    o.select_set(False)


def open_ends(o):
    """Delete the faces on the section's two end planes (x = ±24"), so the run that over-laps them shows no hairline."""
    import bmesh
    bpy.context.view_layer.update()
    mw = o.matrix_world; bm = bmesh.new(); bm.from_mesh(o.data)
    ends = [f for f in bm.faces if abs(abs((mw @ f.calc_center_median()).x) - X1 * IN) < 1e-5 and abs((mw.to_3x3() @ f.normal).normalized().x) > 0.99]
    if ends:
        bmesh.ops.delete(bm, geom=ends, context='FACES'); bm.to_mesh(o.data)
    bm.free()


def rivet(name, x, u, v, axis):
    """A 5/16" rivet head on an interior face: axis 'u' (through a wall) or 'v' (through the floor)."""
    r, h = 0.16, 0.06
    if axis == "u":
        o = cyl(name, "existing", r * IN, h * IN, x * IN, u * IN, v * IN, M("fast"), verts=14); o.rotation_euler = (math.pi / 2, 0, 0)
    else:
        o = cyl(name, "existing", r * IN, h * IN, x * IN, u * IN, v * IN, M("fast"), verts=14)
    return o
