"""
rmi_blender.py — shared helpers for building RMI detail models in Blender.

Every detail build script starts with:

    import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from rmi_blender import *
    reset_scene()
    ...build geometry using box/cyl/link/helper...
    finalize("cast-iron-drain-D-1-TYP")

Run from the command line (no window, no add-on needed):
    blender -b --python scripts/build_drain_D-1-TYP.py

Rules this file enforces (learned the hard way):
  * Layers are collections named exactly existing / primer / flex / topcoat, and every object
    is renamed "<layer>__<part>" so the web loader can switch it per stage.
  * Anything used only to carve geometry is registered with helper(); finalize() bakes all
    modifiers into the real meshes and DELETES the helpers before export, so a hidden cutter
    can never ship inside the .glb.
  * Export is glTF Binary, modifiers applied, visible objects only, saved next to the .blend in models/.
"""
import bpy, os

IN = 0.0254          # inches → metres (Blender works in metres; the web app scales to feet)
LAYERS = ("existing", "primer", "flex", "topcoat")
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")

_helpers = []
_coll = {}


def reset_scene():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for c in list(bpy.data.collections):
        if c.name in LAYERS:
            bpy.data.collections.remove(c)
    _helpers.clear(); _coll.clear()
    for L in LAYERS:
        c = bpy.data.collections.new(L); bpy.context.scene.collection.children.link(c); _coll[L] = c
    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", 'SUN')); sun.data.energy = 3
    sun.rotation_euler = (0.9, 0.2, 0.6); bpy.context.scene.collection.objects.link(sun)


def mat(name, rgb, rough=0.5, metal=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    return m


# Shared material library — one definition, every detail reuses it. Textures get added here later.
LIB = {
    "membrane":   lambda: mat("RMI_membrane",     (0.80, 0.80, 0.77), 0.85),
    "modbit":     lambda: mat("RMI_modbit",       (0.43, 0.42, 0.39), 1.0),
    "concrete":   lambda: mat("RMI_concrete",     (0.72, 0.71, 0.67), 0.95),
    "insulation": lambda: mat("RMI_insulation",   (0.93, 0.90, 0.70), 0.9),
    "deck":       lambda: mat("RMI_deck",         (0.55, 0.57, 0.60), 0.4, 0.8),
    "panel":      lambda: mat("RMI_panel_metal",  (0.61, 0.63, 0.61), 0.6, 0.35),
    "curb":       lambda: mat("RMI_curb_metal",   (0.58, 0.60, 0.62), 0.45, 0.85),
    "coping":     lambda: mat("RMI_coping_metal", (0.62, 0.64, 0.65), 0.35, 0.9),
    "castiron":   lambda: mat("RMI_castiron",     (0.20, 0.22, 0.24), 0.7, 0.6),
    "rust":       lambda: mat("RMI_rust",         (0.45, 0.25, 0.12), 0.95),
    "lead":       lambda: mat("RMI_lead",         (0.50, 0.52, 0.55), 0.6, 0.7),
    "unit":       lambda: mat("RMI_unit",         (0.86, 0.87, 0.85), 0.7),
    "unitD":      lambda: mat("RMI_unit_dark",    (0.32, 0.36, 0.40), 0.8),
    "wood":       lambda: mat("RMI_wood",         (0.55, 0.42, 0.28), 0.9),
    "fast":       lambda: mat("RMI_fastener",     (0.72, 0.74, 0.75), 0.4, 0.9),
    "seal":       lambda: mat("RMI_sealant",      (0.25, 0.25, 0.27), 0.6),
    "tape":       lambda: mat("RMI_tape",         (0.82, 0.83, 0.84), 0.5, 0.4),
    "primer":     lambda: mat("RMI_primer",       (0.90, 0.82, 0.62), 0.4),
    "flex":       lambda: mat("RMI_Flex",         (0.85, 0.62, 0.10), 0.45),
    "thane":      lambda: mat("RMI_Thane",        (0.82, 0.85, 0.88), 0.3, 0.6),
    "white":      lambda: mat("RMI_White",        (0.96, 0.96, 0.94), 0.5),
}


def M(key):
    return LIB[key]()


def link(o, layer, name):
    """Move an object into a layer collection and give it the layer-prefixed name."""
    for cc in o.users_collection:
        cc.objects.unlink(o)
    _coll[layer].objects.link(o); o.name = f"{layer}__{name}"
    return o


def helper(o):
    """Register a carving/cutter object. Deleted by finalize() after modifiers are baked."""
    o.hide_set(True); _helpers.append(o)
    return o


def cut(o, cutter):
    b = o.modifiers.new("cut", "BOOLEAN"); b.operation = 'DIFFERENCE'; b.object = cutter; b.solver = 'EXACT'


def box(name, layer, sx, sy, sz, x, y, z, m, bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z)); o = bpy.context.object
    o.scale = (sx, sy, sz); o.data.materials.append(m); link(o, layer, name)
    if bevel:
        b = o.modifiers.new("bevel", "BEVEL"); b.width = bevel; b.segments = 3
    return o


def cyl(name, layer, r, h, x, y, z, m, verts=48, r2=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=(x, y, z), vertices=verts)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=r, radius2=r2, depth=h, location=(x, y, z), vertices=verts)
    o = bpy.context.object; o.data.materials.append(m); link(o, layer, name)
    return o


def torus(name, layer, R, r, x, y, z, m, seg=64, rings=16):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=(x, y, z), major_segments=seg, minor_segments=rings)
    o = bpy.context.object; o.data.materials.append(m); link(o, layer, name)
    return o


def _override():
    win = bpy.context.window_manager.windows[0] if bpy.context.window_manager.windows else None
    if not win:
        return None
    areas = [a for a in win.screen.areas if a.type == 'VIEW_3D']
    if not areas:
        return None
    a = areas[0]
    return dict(window=win, area=a, region=a.regions[-1])


def finalize(name, models_dir=MODELS_DIR):
    """Bake modifiers, delete helpers, export <name>.glb and save <name>.blend into models/."""
    os.makedirs(models_dir, exist_ok=True)
    meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o not in _helpers]
    ov = _override()
    ctx = bpy.context.temp_override(**ov) if ov else None
    if ctx: ctx.__enter__()
    try:
        for o in meshes:
            bpy.context.view_layer.objects.active = o; o.select_set(True)
            for md in list(o.modifiers):
                try:
                    bpy.ops.object.modifier_apply(modifier=md.name)
                except Exception as e:
                    print("modifier_apply failed on", o.name, md.name, e)
            o.select_set(False)
        for h in _helpers:
            bpy.data.objects.remove(h, do_unlink=True)
        _helpers.clear()
        for L in LAYERS:
            for o in _coll[L].objects:
                if not o.name.startswith(L + "__"):
                    o.name = f"{L}__{o.name}"
        if meshes:
            bpy.context.view_layer.objects.active = meshes[0]
        glb = os.path.join(models_dir, name + ".glb")
        bpy.ops.export_scene.gltf(filepath=glb, export_format='GLB', export_apply=True, use_visible=True)
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(models_dir, name + ".blend"))
    finally:
        if ctx: ctx.__exit__(None, None, None)
    print(f"exported {glb} ({os.path.getsize(glb)//1024} KB), {len(meshes)} meshes")
    return glb
