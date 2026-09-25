"""
build_gutter_inlet_D-8-TYP.py — a gutter inlet / downspout drop per RMI detail D-8-TYP (GUTTER INLET/DOWNSPOUT – TYPICAL,
11/05/24) with D8-9-FT-3D (GUTTER COLLECTOR / DOWNSPOUTS – CONCEPT DRAWING, 9/1/21) as reference.

    blender -b --python scripts/build_gutter_inlet_D-8-TYP.py

A 4-ft SECTION of the eave-hung gutter (scripts/rmi_gutter.py has the frame and every gutter size) with the outlet
tube through its floor at the centre and 12" of the drop below it; the app's code-drawn downspout carries on down from
there. Spliced into the gutter run at the arena's and the hangar's inlet hotspot (gutterRun in index.html).

What the drawing says (VERIFIED):
  * (E) gutter and (E) inlet drain: replace damaged, ill-fitting components (the gutter assembly is shown for
    illustration, notes 12 and 13). (E) or (N) inlet / downspout (note 13). Rust with pin holes: patch or replace (note 12).
  * Clean, prepare and prime per the Spec Guide Manual for each type of (E) gutter / inlet (note 13); adhesion test
    first (note 9).
  * "RMI-FLEX VAPOR BARRIER-FLASHING COAT. EXTEND A MINIMUM 3" DIAMETER FROM INLET AND 3" INTO INLET TUBE" — read as
    3" out from the inlet's edge across the gutter floor and 3" down inside the tube.
  * "RMI-THANE. EXTEND MIN. 1" INTO INLET TUBE PAST RMI-FLEX" — 4" down the tube; over the whole gutter interior per
    W-7-TYP, since the two sheets describe one gutter.
  * Note 10: water test the finished installation. Note 7: gutter / inlet configuration to code and SMACNA or excluded
    from warranty; note 11: plastic / ABS excluded. The sheet draws the tube's top flared onto the floor with a fastener
    each side; no sealant is drawn, so none is modelled.

ASSUMED (the sheet is not to scale and carries no dimensions): every gutter size (rmi_gutter.py); a 4" round outlet
tube with a 1" flange on the floor and two rivets; the wire-basket strainer in the outlet — no sheet mentions one,
it is lifted out for the work and reset after the topcoat; the primer 1/2" past the Flex out and down; the coat
thicknesses; 12" of drop modelled below the floor.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from rmi_blender import IN, M, cyl, cut, helper, reset_scene, finalize, Shell
from rmi_gutter import (X0, X1, MT, W, D, COATS, BAND_TOP, trough, straps, coat_u, rivet, apply_modifiers, open_ends)

OUT_R      = 2.0                        # 4" round outlet tube (ASSUMED)
OUT_FL     = 1.0                        # flange onto the floor (ASSUMED)
OUT_DROP   = 12.0                       # drop modelled below the floor; the app's downspout takes over (ASSUMED)
FLEX_OUT   = 3.0                        # VERIFIED: Flex min 3" out from the inlet across the floor
FLEX_IN    = 3.0                        # VERIFIED: Flex min 3" into the tube
THANE_IN   = FLEX_IN + 1.0              # VERIFIED: Thane min 1" into the tube past the Flex
PRIMER_PAST = 0.5                       # primer past the Flex, out and down (ASSUMED)
TOP_PAST   = 0.26                       # topcoat disc past the primer over the raised Flex (ASSUMED)
RIVET_R    = OUT_R + OUT_FL / 2         # rivets through the middle of the flange
STRAINER   = [(2.3, 0.15), (1.95, 1.6), (1.15, 3.0)]   # wire-basket rings: (r, height above the flange); 8 wires between them
WIRE       = 0.06                       # wire radius (1/8" wire)

UC = -W / 2                             # the outlet on the floor's centre-line
ZF = -D + MT                            # floor top
ZT = ZF + MT                            # flange top — the disc coats sit on it
IR = OUT_R - MT                         # tube bore

reset_scene()

# (E) gutter section and the outlet: tube through the floor with a flange on it, riveted; 12" of drop below
trough("gutter", X0, X1, floor_caps=True)
straps()
floor = bpy.data.objects["existing__gutter_floor"]
tube = Shell().tube(OUT_R * IN, IR * IN, (-D - OUT_DROP) * IN, ZT * IN).emit("existing", "outlet_tube", M("coping"))
flange = Shell().tube((OUT_R + OUT_FL) * IN, IR * IN, ZF * IN, ZT * IN).emit("existing", "outlet_flange", M("coping"))
for o in (tube, flange):
    o.location = (0, UC * IN, 0)
for i, x in enumerate((-RIVET_R, RIVET_R)):
    rivet(f"rivet_{i}", x, UC, ZT + 0.03, "v")

# the strainer basket: three wire rings and eight wires, lifted out for the work and reset after the topcoat (ASSUMED)
s = Shell()
for r, h in STRAINER:
    s.torus(r * IN, WIRE * IN, (ZT + h) * IN, seg=32, rings=6)
s.emit("existing", "strainer_rings", M("fast")).location = (0, UC * IN, 0)
(r0, h0), (r1, h1) = STRAINER[0], STRAINER[-1]
for i in range(8):
    a = 2 * math.pi * i / 8
    p0 = (r0 * math.cos(a), r0 * math.sin(a), ZT + h0); p1 = (r1 * math.cos(a), r1 * math.sin(a), ZT + h1)
    ln = math.dist(p0, p1); mid = [(p0[k] + p1[k]) / 2 for k in range(3)]
    o = cyl(f"strainer_wire_{i}", "existing", WIRE * IN, ln * IN, mid[0] * IN, (UC + mid[1]) * IN, mid[2] * IN, M("fast"), verts=8)
    d = [p1[k] - p0[k] for k in range(3)]
    o.rotation_euler = (0, math.acos(d[2] / ln), math.atan2(d[1], d[0]))   # tilt the wire from the bottom ring in to the top ring

# Coats: discs on the floor around the inlet (VERIFIED 3" out) and rings down the tube (VERIFIED 3" / 4" in);
# the topcoat film over the whole interior, rising over the disc to enclose it
def disc(layer, name, r_out, z0, z1, mat):
    o = Shell().tube(r_out * IN, IR * IN, (ZT + z0) * IN, (ZT + z1) * IN).emit(layer, name, mat); o.location = (0, UC * IN, 0); return o

def ring(layer, name, depth, o0, o1, mat):
    o = Shell().tube((IR - o0) * IN, (IR - o1) * IN, (ZT - depth) * IN, ZT * IN).emit(layer, name, mat); o.location = (0, UC * IN, 0); return o

p0, p1 = COATS["primer"]; f0, f1 = COATS["flex"]; t0, t1 = COATS["topcoat"]
disc("primer", "primer_disc", OUT_R + FLEX_OUT + PRIMER_PAST, p0, p1, M("primer"))
ring("primer", "primer_ring", FLEX_IN + PRIMER_PAST, p0, p1, M("primer"))
disc("flex", "flex_disc", OUT_R + FLEX_OUT, f0, f1, M("flex"))
ring("flex", "flex_ring", FLEX_IN, f0, f1, M("flex"))
disc("topcoat", "topcoat_disc", OUT_R + FLEX_OUT + PRIMER_PAST + TOP_PAST, t0, BAND_TOP, M("thane"))
ring("topcoat", "topcoat_ring", THANE_IN, f1, f1 + (t1 - t0), M("thane"))
u = coat_u("topcoat", "topcoat_run", X0, X1, t0, t1, caps=True)

# the outlet hole through the floor and the topcoat film over it
bore = helper(cyl("bore_cutter", "existing", IR * IN, (D + 4) * IN, 0, UC * IN, (ZF - 1) * IN, M("coping"), verts=48))
for o in (floor, u):
    cut(o, bore); apply_modifiers(o); open_ends(o)   # cut the capped mesh, then take the end caps off again

finalize("gutter-inlet-D-8-TYP")
