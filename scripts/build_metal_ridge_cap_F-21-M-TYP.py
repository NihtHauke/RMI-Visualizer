"""
build_metal_ridge_cap_F-21-M-TYP.py — metal ridge cap at the panel end closure, per RMI detail
F-21-M-TYP (METAL RIDGE CAP / L METAL @ PANEL END CLOSURE, 11/05/24).

    blender -b --python scripts/build_metal_ridge_cap_F-21-M-TYP.py

There is NO 3D concept render for this detail in the library, so unlike the coping or the drain there is
nothing to check the massing against — everything below beyond the drawing's own words is ASSUMED.

What the 2D drawing says (VERIFIED):
  * "(E) RIDGE CAP AND/OR L METAL WALL FLASHING" over "(E) METAL PANEL".
  * "(E) (N) METAL CLOSURE" at the panel end, with "(N) (E) CLOSURE FASTENER".
  * "(N) (E) CLOSURE SET IN SEALANT OR TAPE. APPLY SEALANT TO ANY VOIDS." and "RIBBON OF SEALANT AT VOIDS".
  * "RMI FLEX" at the cap, one call-out reading "(ENCAPSULATE METAL CLOSURE".
  * "RMI THANE" over all.
  * Note 3: do not overdrive fasteners.
  * Note 7: detail equally applies to all areas.
  * Note 8: "INSERT SHOWN FOR ILLUSTRATION PURPOSE ONLY. FOLLOW DETAIL DRAWING FOR CONFIGURATION."
  * Note 11: "CONFIRM METAL CLOSURE ARE PRESENT AND TIGHT FITTING WITHOUT GAPS. REPLACE DAMAGED OR ILL
    FITTING CLOSURES. SEAL EDGES OF CLOSURES PRIOR TO INSTALLATION OF RMI FLEX."  -> the sealant is prep
    work, so it is named primer__sealant_* and the app shows it from the prep stage and never sweeps it.
  * Note 12: "WHERE CLOSURES ARE NOT RECESSED A MINIMUM OF 6" UNDER FLASHING METAL OR RIDGE CAP, ADD
    ADDITIONAL FLAT STOCK FLASHING TO MEET REQUIREMENT."  -> the one real dimension the drawing gives.
    The closure here sits 18" from the ridge centreline, which puts it 7.8" under the cap edge: over the
    6" minimum, so no added flat stock is needed. That 6" is VERIFIED; the 18" placement is ASSUMED.
  * Note 13: foam closures are not permissible without prior written approval from RMI Technical Services.

This model is a 4-FT SECTION OF RIDGE that the app splices into the code-drawn ridge cap on the warehouse,
the same way the F-8-TYP lap section splices into the slope. The cap run, the cap's offset from the ridge,
its thickness and how far the cap floats above the panel are therefore NOT free: they are index.html's own
ridge-cap numbers (CAP_RUN / CAP_OFF / CAP_T / RIDGE_DROP below), and if those change in the app they must
change here too or the bay ends show a step.

PITCH: built for a 1:12 gable, which is what the warehouse uses. A different pitch needs a rebuild — the app
only splices this model in where `cfg.ridgeModel` is set, which is the warehouse alone.

ASSUMED (everything except the 6" recess): the 4-ft section length; the 6" cap lap and its joggled end; the
closure at 18" from the ridge, its 3" width and the rectangular notches where the ribs pass; fastener size and
12" o.c. spacing; the sealant bead sizes; how far the Flex runs onto the cap, over its edge and onto the panel;
and every coat thickness.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import math
from rmi_blender import IN, M, box, cyl, helper, cut, reset_scene, finalize

# ---------------------------------------------------------------- the app's own ridge-cap numbers (index.html)
PITCH = 1.0 / 12.0                  # warehouse gable
ANG = math.atan(PITCH)
TANG = math.tan(ANG)
CAP_RUN = 26.4                      # cap depth each side of the ridge  (app 2.2 ft)
CAP_OFF = 12.6                      # cap centre, out from the ridge    (app 1.05 ft)
CAP_T = 0.96                        # cap thickness                     (app 0.08 ft)
RIDGE_DROP = 1.44                   # cap group sits this far above the ridge panel line (app 0.12 ft)
TOPCOAT_LIFT = 0.6                  # app floats the cap topcoat this far above the cap (app 0.05 ft)

# ---------------------------------------------------------------- the section (inches; ASSUMED)
BAY = 48.0                          # 4-ft section along the ridge
LAP_W = 6.0                         # cap lap, joggled so both bay ends stay flush with the run
CLOSURE_A = 18.0                    # closure centre, out from the ridge -> 7.8" under the cap edge (note 12 wants >= 6")
CLOSURE_W = 3.0
RIB_PITCH, RIB_B, RIB_H = 12.0, 6.6, 1.32     # R-panel rib the closure notches over (LAP in index.html)
FAST_R, FAST_H = 0.22, 0.5
BEAD = 0.35
TP, TF, TT = 0.08, 0.30, 0.36       # primer / Flex / topcoat thicknesses over the cap lap (app lap coat steps)

# The band that runs out onto the panel from the cap edge is the SAME band index.html draws along the whole
# ridge (s.ridgeP / s.ridgeF and the topcoat over them), so the bay ends meet the run with no step: same
# length out from the cap edge, same heights above the panel, same thicknesses. Heights clear the rib crests,
# which is why the Flex bridges the ribs instead of being pierced by them.
BAND_LEN = 10.2                     # out from the cap edge (app 0.85 ft)
BAND_Y = {"primer": 1.92, "flex": 2.04, "topcoat": 2.10}    # above the panel (app eY+0.03 / +0.04 / +0.045)
BAND_T = {"primer": 0.60, "flex": 0.72, "topcoat": 1.20}   # the topcoat box encloses the other two
BAND_OVER = {"primer": 0.0, "flex": 0.0, "topcoat": 0.72}  # ... and overhangs them inboard and outboard

CAP_EDGE = CAP_OFF + CAP_RUN / 2.0  # 25.8" — the cap's outer edge
RECESS = CAP_EDGE - CLOSURE_A       # 7.8" of cap over the closure


def cap_z(a):
    """Height of the cap's centre plane at `a` inches out from the ridge."""
    return -(a - CAP_OFF) * TANG


def panel_z(a):
    """Height of the (E) panel surface at `a` inches out from the ridge."""
    return -RIDGE_DROP - a * TANG


def tilted(name, layer, lx, ly, lz, x, a, z, m, sgn, shadow=True):
    """A box on one slope: `a` is out from the ridge (unsigned), `sgn` picks the side, and the box is
    rotated about its own centre by the roof pitch exactly the way index.html rotates the cap."""
    o = box(name, layer, lx * IN, ly * IN, lz * IN, x * IN, sgn * a * IN, z * IN, m, )
    o.rotation_euler = (-sgn * ANG, 0, 0)
    return o


reset_scene()

for sgn in (1, -1):
    s = "p" if sgn > 0 else "m"

    # ------------------------------------------------------------ (E) ridge cap: two lengths with a joggled lap
    # cap_a runs to the lap, cap_b carries on from it, and cap_lap is cap_b's joggled end sitting over cap_a.
    # The joggle is why both bay ends stay flush with the code-drawn run either side.
    a0, a1 = -BAY / 2, LAP_W / 2
    tilted(f"cap_a_{s}", "existing", a1 - a0, CAP_RUN, CAP_T, (a0 + a1) / 2, CAP_OFF, cap_z(CAP_OFF), M("coping"), sgn)
    b0, b1 = LAP_W / 2, BAY / 2
    tilted(f"cap_b_{s}", "existing", b1 - b0, CAP_RUN, CAP_T, (b0 + b1) / 2, CAP_OFF, cap_z(CAP_OFF), M("coping"), sgn)
    l0, l1 = -LAP_W / 2, LAP_W / 2 + 0.2
    tilted(f"cap_lap_{s}", "existing", l1 - l0, CAP_RUN, CAP_T, (l0 + l1) / 2, CAP_OFF, cap_z(CAP_OFF) + CAP_T, M("coping"), sgn)

    # ------------------------------------------------------------ (E)/(N) metal closure at the panel end
    top = cap_z(CLOSURE_A) - CAP_T / 2.0        # underside of the cap
    bot = panel_z(CLOSURE_A)                    # panel surface
    ch = top - bot
    cl = tilted(f"closure_{s}", "existing", BAY, CLOSURE_W, ch, 0, CLOSURE_A, (top + bot) / 2.0, M("curb"), sgn)
    for i in range(-2, 3):                      # notches where the R-panel ribs pass under it
        rx = i * RIB_PITCH - RIB_PITCH / 2.0
        if abs(rx) > BAY / 2:
            continue
        n = tilted(f"closure_notch_{s}_{i}", "existing", RIB_B, CLOSURE_W * 3, RIB_H,
                   rx, CLOSURE_A, bot + RIB_H / 2.0, M("curb"), sgn)
        cut(cl, helper(n))

    # ------------------------------------------------------------ closure fasteners through the cap, 12" o.c.
    for i in range(-2, 3):
        fx = i * RIB_PITCH - RIB_PITCH / 2.0
        if abs(fx) > BAY / 2:
            continue
        fz = cap_z(CLOSURE_A) + CAP_T / 2.0 + FAST_H / 2.0
        f = cyl(f"fastener_{s}_{i}", "existing", FAST_R * IN, FAST_H * IN,
                fx * IN, sgn * CLOSURE_A * IN, fz * IN, M("fast"), verts=12)
        f.rotation_euler = (-sgn * ANG, 0, 0)

    # ------------------------------------------------------------ sealant: closure set in sealant, ribbon at voids
    tilted(f"sealant_closure_{s}", "primer", BAY, CLOSURE_W + 2 * BEAD, BEAD, 0, CLOSURE_A, bot + BEAD / 2.0,
           M("seal"), sgn, shadow=False)
    tilted(f"sealant_lap_{s}", "primer", LAP_W, CAP_RUN, BEAD, 0, CAP_OFF, cap_z(CAP_OFF) + CAP_T / 2.0 + BEAD / 2.0,
           M("seal"), sgn, shadow=False)

    # ------------------------------------------------------------ coats
    # Primer goes on what will take Flex: the cap lap and the fastener line (the app's own layer text).
    # Flex goes over the cap lap and over both cap edges, bridging cap -> closure -> panel.
    # Topcoat covers the cap, the lap and the edges.
    for layer, mat, t, grow in (("primer", "primer", TP, 0.0), ("flex", "flex", TF, 1.0), ("topcoat", "thane", TT, 2.0)):
        # over the cap lap
        zl = cap_z(CAP_OFF) + CAP_T / 2.0 + CAP_T + grow * TF * 0.6      # clear of the joggled lap
        tilted(f"{layer}_lap_{s}", layer, LAP_W + 4 + grow, CAP_RUN + 1.5 + grow * 0.5, t, 0, CAP_OFF + 0.75,
               zl + t / 2.0, M(mat), sgn, shadow=False)

        # out onto the panel from the cap edge — the run's own band, so the bay ends meet it flush
        by, bt, bo = BAND_Y[layer], BAND_T[layer], BAND_OVER[layer]
        ln = BAND_LEN + bo
        pa = CAP_EDGE - bo / 2.0 + ln / 2.0
        tilted(f"{layer}_panel_{s}", layer, BAY, ln, bt, 0, pa, panel_z(pa) + by, M(mat), sgn, shadow=False)

        if layer == "primer":
            continue                                                      # on the cap it is the lap and fasteners only

        # turned up over the cap edge, sealing cap to closure to panel (the drawing's Flex at the cap edge)
        z_hi = cap_z(CAP_EDGE) + CAP_T / 2.0 + t
        # bottom referenced to the Flex band so each coat reaches a touch lower than the one it covers
        z_lo = panel_z(CAP_EDGE) + BAND_Y["flex"] - BAND_T["flex"] / 2.0 - (grow - 1.0) * t
        # every coat shares the Flex closer's centre line, so the thicker topcoat wraps it on both faces
        tilted(f"{layer}_edge_{s}", layer, BAY, t, z_hi - z_lo, 0, CAP_EDGE + TF / 2.0,
               (z_hi + z_lo) / 2.0, M(mat), sgn, shadow=False)

    # ------------------------------------------------------------ topcoat over the whole cap (the app floats one too)
    tilted(f"topcoat_cap_{s}", "topcoat", BAY, CAP_RUN, CAP_T, 0, CAP_OFF, cap_z(CAP_OFF) + TOPCOAT_LIFT,
           M("thane"), sgn, shadow=False)

print(f"\nmetal ridge cap: {BAY:.0f}in section, cap {CAP_RUN}in each side, closure {CLOSURE_A}in from the ridge")
print(f"  closure recessed {RECESS:.1f}in under the cap edge — note 12 wants a minimum of 6in")
print(f"  cap floats {RIDGE_DROP + CAP_T / 2:.2f}in above the ridge panel line; closure height {ch:.2f}in")

finalize("metal-ridge-cap-F-21-M-TYP")
