"""
build_silo_wall_W-7-TYP.py — a section of the concrete silo bin wall, vertical application, per RMI detail W-7-TYP
(CONCRETE WALL – TYPICAL, 11/05/24; the sheet filed under Typical Wall Configurations — the gutter-seams sheet under
Drains carries the same number) with Plate C (concrete substrate, 1/01/2020) for the crack repair. No 3D concept render;
no sheet shows a silo or a curved wall.

    blender -b --python scripts/build_silo_wall_W-7-TYP.py

A 4-ft-tall RING of one bin's wall (the bin is 14 ft in radius, the app's own number), origin on the bin axis at the
band's bottom, z up. The app splices it into the code-drawn bin at the silo hotspot (buildSilo in index.html): the bin's
concrete cylinder and its three coat cylinders stop 0.6 mm inside the band and the ring fills it, faceted on the same
48-segment grid as the app's cylinders so the facets meet. Nothing here is capped top or bottom.

What the documents say (VERIFIED):
  * W-7-TYP: (E) concrete wall. Check all (E) panel joint sealant; replace all damaged, aged or cracked panel joint
    sealant. Clean, repair, prepare and prime per the Spec Guide Manual for each type of surface. RMI-Flex vapor
    barrier-base coat — the rate may increase depending on the wall finish. RMI-Thane / RMI-White over it. Note 7: all
    types of concrete wall panels and finishes; note 8: adhesion test and moisture scan first.
  * Plate C (concrete substrate): repair voids, cracks or deficiency in the concrete — spalling and cracks according to
    concrete standards including concrete patch, epoxy injection, joints; patch materials to match the concrete; install
    Flex at all repairs; check (E) joint sealant; power wash; moisture test mandatory.

ASSUMED — everything about extents, pending RMI's answer (catalog §5 #17): that W-7-TYP, a flat wall sheet, and Plate C,
a roof plate, carry over to a curved slipformed bin wall sprayed vertically; the whole wall coated full height (the
app's bins have always been drawn that way); eight vertical control joints per bin, 1" wide, 1/2" deep, sealant in
them; a 3/4" construction (lift) line at mid-band; three hairline cracks on the front face, routed and patched 1-1/2"
wide; 24" of the 1" thick wall shell modelled; coat thicknesses drawn at the app's own 0.48" / 0.96" / 1.44" radii.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from rmi_blender import IN, M, link, reset_scene, finalize, smooth_by_angle

# ---------------------------------------------------------------- dimensions (inches; ASSUMED unless noted)
R        = 14 * 12.0            # bin radius — the app's silo (buildSilo: R = 14 ft)
H        = 48.0                 # band height
SEG      = 48                   # facets per turn — the app's CylinderGeometry(…, 48) so the facets meet at the seam
SHELL    = 1.0                  # wall shell modelled (the app's bin is a surface)
N_JOINT  = 8                    # vertical control joints per bin, evenly spaced
JOINT_W, JOINT_D = 1.0, 0.5     # joint width and depth
LIFT_Z, LIFT_H, LIFT_D = 24.0, 0.75, 0.5        # horizontal construction (lift) line at mid-band
SEAL_OLD = (0.5, 0.25)          # (E) sealant, sunk in the joint: from JOINT_D down to this off the face; raked out at prep
SEAL_NEW = (0.5, 0.1)           # new sealant, nearly flush (W-7-TYP: replace damaged, aged or cracked sealant)
FRONT    = -math.pi / 2         # the bin's front face (the app's +z, where the hotspot and camera are) in Blender's angle
CRACKS   = [(-14.0, 4.0, 34.0, 4), (3.0, 12.0, 46.0, 5), (19.0, 2.0, 26.0, 3)]   # (degrees from FRONT, z bottom, z top, steps)
CRACK_W, CRACK_T = 0.15, 0.06   # hairline crack drawn as a strip proud of the face so it reads
PATCH_W, PATCH_T = 1.5, 0.1     # routed and patched: patch material to match concrete (Plate C), drawn slightly proud
# coat shells, off the concrete face — each encloses the radius the app draws that coat at (0.48", 0.96", 1.44")
COATS    = {"primer": (0.12, 0.60), "flex": (0.60, 1.08), "topcoat": (1.08, 1.56)}

STEP = 2 * math.pi / SEG
reset_scene()


def arc(name, layer, r0, r1, z0, z1, a0, a1, mat, ends=True):
    """A curved slab between radii r0..r1, heights z0..z1 and angles a0..a1 (radians), subdivided at every facet angle of
    the app's cylinder grid so the flats line up. Open top and bottom; `ends` closes the two angular end faces."""
    k0, k1 = math.floor(a0 / STEP) + 1, math.ceil(a1 / STEP) - 1
    angs = [a0] + [k * STEP for k in range(k0, k1 + 1) if a0 + 1e-9 < k * STEP < a1 - 1e-9] + [a1]
    v, f = [], []
    for a in angs:
        c, s = math.cos(a), math.sin(a)
        v += [(r0 * c * IN, r0 * s * IN, z0 * IN), (r1 * c * IN, r1 * s * IN, z0 * IN), (r1 * c * IN, r1 * s * IN, z1 * IN), (r0 * c * IN, r0 * s * IN, z1 * IN)]
    n = len(angs)
    for i in range(n - 1):
        a, b = 4 * i, 4 * (i + 1)
        f.append((a + 1, b + 1, b + 2, a + 2))     # outer face
        f.append((b + 0, a + 0, a + 3, b + 3))     # inner face
    if ends:
        f.append((0, 1, 2, 3)); e = 4 * (n - 1); f.append((e + 3, e + 2, e + 1, e + 0))
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], f); me.validate(); smooth_by_angle(me, 20)
    o = bpy.data.objects.new(name, me); o.data.materials.append(mat)
    return link(o, layer, name)


def ring(name, layer, r0, r1, z0, z1, mat):
    """A full ring — the same slab all the way round, no end faces."""
    return arc(name, layer, r0, r1, z0, z1, 0.0, 2 * math.pi, mat, ends=False)


concrete, seal = M("concrete"), M("seal")
half_j = JOINT_W / 2 / R                        # half a joint, in radians
joints = [FRONT + i * 2 * math.pi / N_JOINT + math.pi / N_JOINT for i in range(N_JOINT)]   # joints straddle the front face, none at its centre

# (E) concrete wall shell between the control joints, split at the lift line
for i, a in enumerate(joints):
    b = joints[(i + 1) % N_JOINT]
    if b < a:
        b += 2 * math.pi
    a0, a1 = a + half_j, b - half_j
    arc(f"concrete_{i}_lo", "existing", R - SHELL, R, 0.0, LIFT_Z - LIFT_H / 2, a0, a1, concrete)
    arc(f"concrete_{i}_hi", "existing", R - SHELL, R, LIFT_Z + LIFT_H / 2, H, a0, a1, concrete)
    # the joint: its floor, the (E) sealant raked out at prep, the new sealant from prep on
    arc(f"concrete_joint_{i}", "existing", R - SHELL, R - JOINT_D, 0.0, H, a - half_j, a + half_j, concrete)
    arc(f"oldseal_before_{i}", "existing", R - SEAL_OLD[0], R - SEAL_OLD[1], 0.0, H, a - half_j, a + half_j, M("mastic"))
    arc(f"sealant_new_{i}", "primer", R - SEAL_NEW[0], R - SEAL_NEW[1], 0.0, H, a - half_j, a + half_j, seal)
ring("concrete_lift", "existing", R - SHELL, R - LIFT_D, LIFT_Z - LIFT_H / 2, LIFT_Z + LIFT_H / 2, concrete)   # the lift line's floor

# hairline cracks on the front face: stepped strips, each routed and patched at prep (Plate C: patch to match the concrete)
for k, (deg, z0, z1, steps) in enumerate(CRACKS):
    a = FRONT + math.radians(deg); dz = (z1 - z0) / steps; w = CRACK_W / R
    for j in range(steps):
        off = (0.45 if j % 2 else -0.45) / R
        arc(f"crack_before_{k}_{j}", "existing", R, R + CRACK_T, z0 + j * dz, z0 + (j + 1) * dz, a + off - w / 2, a + off + w / 2, M("mastic"))
    pw = PATCH_W / 2 / R
    arc(f"patch_after_{k}", "existing", R, R + PATCH_T, z0 - 1.0, z1 + 1.0, a - pw, a + pw, M("unit"))

# the coats: full height, all the way round (ASSUMED extents — no sheet gives any)
for layer, (o0, o1) in COATS.items():
    ring(f"{layer}_shell", layer, R + o0, R + o1, 0.0, H, M("thane" if layer == "topcoat" else layer))

finalize("silo-wall-W-7-TYP")
