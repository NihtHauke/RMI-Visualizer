"""
build_metal_coping_joint_W-1-TYP.py — metal coping joint per RMI detail W-1-TYP (METAL COPING JOINTS –
TYPICAL, 11/05/24) with W1-11-FT3D (EXISTING / NEW METAL COPING – CONCEPT DRAWING, 9/1/21) as reference.

    blender -b --python scripts/build_metal_coping_joint_W-1-TYP.py

The model is a 4-ft SECTION OF PARAPET with one coping joint in the middle. The app splices it into a
coping run, so the cap / leg / topcoat cross-sections match the code-drawn run exactly (18" cap, 3" thick,
6" drip legs, topcoat to the run's overlay surface) — change those and the seams will show.
x runs along the parapet; -y is the OUTSIDE face (run-local +z in the app, where the fasteners go).

What the 2D drawing says (VERIFIED):
  * Check for damaged components; replace damaged or broken components.
  * Replace loose/missing fasteners with new oversize stainless screws + EPDM washers; encapsulate with Flex.
  * Fasteners at overlapping metal not permitted (coping needs expansion/contraction at joints) — relocate per SMACNA.
  * Install TAPE a min 2" equally spaced over each side of the joint (4" band), no voids.
  * Clean, prepare and prime per the Spec Guide Manual.
  * RMI-Flex: extend a min 2" beyond the tape (8" band).
  * RMI-Thane / White: extend a min 2" past the Flex for repairs, OR the ENTIRE COPING under the system
    warranty (modelled). Vertical surfaces may need multiple coats.
  * Note 8: applies to all metal coping laps, joints, corners and transitions.

ASSUMED (not on the drawing): parapet 12" × 36"; the coping profile; a 1/2" open joint with a dark backer;
fastener size and 12" spacing either side of the joint; the primer band = the Flex band (is the whole coping
primed under the entire-coping topcoat option? — question for RMI); every coat thickness.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rmi_blender import IN, M, box, cyl, reset_scene, finalize

FT = 12 * IN
# ---------------------------------------------------------------- the run this splices into (must match makeBlock in index.html)
L        = 4 * FT                   # length of the modelled section
PT, PH   = 1 * FT, 3 * FT           # parapet thickness / height
CAP_W    = 1.5 * FT                 # cap width  (cw = PT + 0.5 ft)
CAP_T    = 0.25 * FT                # cap thickness
CAP_Z0   = PH - 0.005 * FT          # cap sits on the parapet top
CAP_Z1   = CAP_Z0 + CAP_T
LEG_T, LEG_H = 0.06 * FT, 0.5 * FT  # drip legs
LEG_Y    = CAP_W / 2 - 0.03 * FT    # leg centre-line (outer face flush with the cap edge)
LEG_Z0   = PH - 0.3 * FT
SIDE     = LEG_Y + LEG_T / 2        # outer face of the coping
TOP_Z1   = PH + 0.31 * FT           # the run's topcoat overlay: top surface …
TOP_ZU   = PH + 0.25 * FT           # … underside of its top slab …
TOP_Y    = CAP_W / 2 + 0.09 * FT    # … outer side surface …
TOP_YT   = CAP_W / 2 + 0.06 * FT    # … half-width of its top slab …
TOP_Z0   = PH - 0.31 * FT           # … and bottom edge
FAST_Z   = PH - 0.1 * FT            # fastener line on the outer face

# ---------------------------------------------------------------- the detail (VERIFIED unless marked)
JOINT_GAP = 0.5 * IN                # open expansion joint (top of the real range, so it reads on screen)   ASSUMED
FAST_X    = 12 * IN                 # fasteners 12" either side of the joint     ASSUMED (none at the joint — VERIFIED)
FAST_R, FAST_H = 5 / 32 * IN, 0.003 # oversize stainless screw + EPDM washer     ASSUMED size
TAPE_W    = 4 * IN                  # tape 2" each side of the joint             VERIFIED
FLEX_W    = TAPE_W + 2 * 2 * IN     # Flex min 2" beyond the tape               VERIFIED
PRIMER_W  = FLEX_W                  # primer under the Flex band                 ASSUMED
TAPE_T, PRIMER_T, FLEX_T = 0.0015, 0.0015, 0.003   # visual thicknesses          ASSUMED


def uband(layer, name, width, off, t, mat, x=0):
    """A band over the cap top and down both faces, `off` proud of the metal, `t` thick — like the app's U()."""
    box(f"{name}_top", layer, width, 2 * (SIDE + off + t), t, x, 0, CAP_Z1 + off + t / 2, mat)
    zt, zb = CAP_Z1 + off + t, LEG_Z0 - off
    for sg in (-1, 1):
        box(f"{name}_side{'_out' if sg < 0 else '_in'}", layer, width, t, zt - zb, x, sg * (SIDE + off + t / 2), (zt + zb) / 2, mat)


reset_scene()

# (E) parapet section — generic; the app re-skins it with the building's wall material
box("parapet", "existing", L, PT, PH, 0, 0, PH / 2, M("wall"))

# (E) metal coping: cap and drip legs in two pieces with an open joint between them; dark backer in the gap
half = (L - JOINT_GAP) / 2; cx = JOINT_GAP / 2 + half / 2
for sg, tag in ((-1, "a"), (1, "b")):
    box(f"cap_{tag}", "existing", half, CAP_W, CAP_T, sg * cx, 0, (CAP_Z0 + CAP_Z1) / 2, M("coping"))
    for sy, side in ((-1, "out"), (1, "in")):
        box(f"leg_{tag}_{side}", "existing", half, LEG_T, LEG_H, sg * cx, sy * LEG_Y, LEG_Z0 + LEG_H / 2, M("coping"))
box("joint_backer", "existing", JOINT_GAP, CAP_W - 0.004, CAP_T - 0.004, 0, 0, (CAP_Z0 + CAP_Z1) / 2 - 0.002, M("seal"))
for sy, side in ((-1, "out"), (1, "in")):
    box(f"joint_backer_{side}", "existing", JOINT_GAP, LEG_T, LEG_H - 0.004, 0, sy * LEG_Y, LEG_Z0 + LEG_H / 2 - 0.002, M("seal"))

# Fasteners on the outer face, clear of the joint (new oversize stainless + EPDM washer)
for i, x in enumerate((-FAST_X, FAST_X)):
    f = cyl(f"fastener_{i}", "existing", FAST_R, FAST_H, x, -(SIDE + FAST_H / 2), FAST_Z, M("fast"), verts=24); f.rotation_euler = (1.5708, 0, 0)

# Tape over the joint (prep-stage work; the app shows primer__tape from the prep stage), then primer over the band
uband("primer", "tape", TAPE_W, 0, TAPE_T, M("tape"))
uband("primer", "primer", PRIMER_W, TAPE_T, PRIMER_T, M("primer"))

# Flex: band over the tape and 2" beyond, down both faces; every fastener encapsulated
uband("flex", "flex", FLEX_W, TAPE_T + PRIMER_T, FLEX_T, M("flex"))
for i, x in enumerate((-FAST_X, FAST_X)):
    d = cyl(f"fastener_dot_{i}", "flex", 0.014, FAST_H + 0.004, x, -(SIDE + (FAST_H + 0.004) / 2), FAST_Z, M("flex"), verts=24); d.rotation_euler = (1.5708, 0, 0)

# Topcoat: the entire coping section, out to the run's overlay surface so it meets the neighbours flush
box("topcoat_top", "topcoat", L, 2 * TOP_YT, TOP_Z1 - TOP_ZU, 0, 0, (TOP_ZU + TOP_Z1) / 2, M("thane"))
for sy, side in ((-1, "out"), (1, "in")):
    box(f"topcoat_{side}", "topcoat", L, TOP_Y - SIDE, TOP_Z1 - TOP_Z0, 0, sy * (SIDE + TOP_Y) / 2, (TOP_Z0 + TOP_Z1) / 2, M("thane"))

finalize("metal-coping-joint-W-1-TYP")
