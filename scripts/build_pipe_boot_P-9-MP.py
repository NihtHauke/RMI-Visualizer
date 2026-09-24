"""
build_pipe_boot_P-9-MP.py — EPDM boot flashing on a pipe through a sloped metal roof per RMI detail P-9-MP (FLEXIBLE BOOT
FLASHING – METAL ROOF PANELS – TYP, 11/05/24). No 3D concept render exists for it. Spliced into the slope like the F-8-TYP
lap (index.html: SLOPE_BAY.mpipe, unitAt) at every pipe on the manufacturing and airport-hangar roofs.

    blender -b --python scripts/build_pipe_boot_P-9-MP.py

What the drawing says (VERIFIED):
  * (E) penetration through the (E) metal roof panel; (E) or (N) roof jack — replace damaged or ill-fitting boots.
  * (E)/(N) FLEXIBLE EPDM BOOT FLASHING WITH FORM FITTING ALUMINUM MOUNTING PLATE, fastened through the plate; for a new
    boot a bead of sealant goes under the mounting plate. A STAINLESS STEEL DRAW BAND clamps the boot to the pipe.
  * "RAKE OUT (E) SEALANT, MASTIC, REPAIRS. APPLY NEW CONTINUOUS BEAD OF RMI APPROVED SEALANT PRIOR TO INSTALLATION OF
    RMI-FLEX AND WEAR SURFACE COATING" — drawn at the edge of the mounting plate and at the top of the boot. The old
    mastic is existing__mastic_before_* (gone from mid-prep), the new beads primer__sealant_* (shown from prep).
  * "ENCAPSULATE ALL FASTENERS WITH RMI-FLEX."
  * "RMI-FLEX VAPOR BARRIER-FLASHING COAT. EXTEND A MIN. 2" PAST EPDM FLASHING UP PENETRATION AND 4" ONTO METAL ROOF
    PANEL." — modelled at 2-1/4" and 4" (then over any rib that 4" edge lands on, as at a lap — ASSUMED).
  * "RMI-THANE, RMI-WHITE. EXTEND A MINIMUM OF 2" UP PENETRATION PAST RMI FLEX." — 2-1/4" modelled; over the field too.
  * The boot is drawn stepped (the cut-to-size rings); note 7: all circular penetrations and supports; note 8: all (E)
    metal panel systems; note 10: clean, prepare and prime.
ASSUMED: the sheet draws the panel flat, so the plate formed over the R-panel ribs either side (a 24" square plate on
R-panel, 18" between the seams on standing seam) is ASSUMED, as are every size — 4" pipe (4-1/2" OD) standing 24" above
the panel, a four-step boot 11" across its base and 8-3/4" tall, the 3/16" plate, the band, fasteners 1" in from the plate
edge at 3" o.c., the beads — and the coat thicknesses. The pipe and boot stand plumb on the sloped panel.

Four models, R-panel and standing seam at each building's pitch:
    models/pipe-boot-{rpanel,sseam}-1in12-P-9-MP.glb       manufacturing (pipes at x = -74, -62, 40; z = 31.5 ft)
    models/pipe-boot-{rpanel,sseam}-1p5in12-P-9-MP.glb     airport hangar (pipes at x = -120, -108, 60; z = 21.5 ft)
Pipes sit at even x (a pan centre on both profiles), 6k ft apart so each building's pipes share one R-panel lap phase, and
at a z the purlin rows miss.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rmi_blender import IN, M, box, cyl, cut, reset_scene, finalize, Shell, band
from rmi_metal_curb import (Variant, rib_offsets, rib_xs, apron_extents, panel_patch, panel_cutter, level_to_panel, prism,
                            APRON_T, LIFT, LAYERS3, CURB_COAT, RP_B, RP_T, RP_H)

PIPE_R, PIPE_WALL, PIPE_H = 2.25, 0.25, 24.0
PLATE = {"rpanel": 12.0, "sseam": 9.0}         # half-width of the square mounting plate
PLATE_T = 0.19
FLEX_ONTO_PANEL = 4.0                          # VERIFIED min 4"
UP_PIPE = 2.25                                 # Flex past the EPDM up the pipe, and the topcoat past the Flex (VERIFIED min 2")
# the boot: (r, z) of its outer face, base to collar, z from the plate top at the pipe's axis (level frame)
BOOT = [(5.5, -2.0), (5.5, 0.9), (4.8, 1.3), (4.7, 2.4), (4.0, 2.8), (3.9, 3.9), (3.3, 4.3), (3.2, 5.4), (2.7, 5.8), (2.65, 8.7)]
COLLAR_TOP = 8.7
BAND = (2.85, 7.3, 8.0)                        # draw band: outer radius, z0, z1
BEAD_BASE, BEAD_TOP = (0.35, 0.30), 0.22       # new sealant: plate-edge bead width/height, top bead radius
FAST_IN, FAST_PITCH = 1.0, 3.0


def panel_z(V, x, ribs):
    """Top of the bare panel at x (R-panel ribs; standing seam plates stay between the seams). None on a rib slope."""
    if V.surface == "rpanel":
        for r in ribs:
            d = abs(x - r)
            if d <= RP_T / 2:
                return RP_H
            if d < RP_B / 2:
                return None
    return 0.0


def profile_band(V, x0, x1, ribs, off):
    """Closed (x, z) section from x0 to x1: the bare panel top raised by `off`, over any R-panel rib in between."""
    top = [(x0, off)]
    if V.surface == "rpanel":
        xs = rib_xs(off)
        for r in ribs:
            if x0 < r < x1:
                top += [(r - xs(off), off), (r - xs(RP_H + off), RP_H + off), (r + xs(RP_H + off), RP_H + off), (r + xs(off), off)]
    return top + [(x1, off), (x1, 0.0), (x0, 0.0)]


def build(V, B):
    reset_scene()
    ribs = rib_offsets(V)
    AX, AY = apron_extents(V, ribs, B + FLEX_ONTO_PANEL, B + FLEX_ONTO_PANEL)
    panel_patch(V, ribs, AX, AY, keep_out=lambda x, y: abs(x) < B + 2 and abs(y) < B + 2)
    cut_panel = panel_cutter(V, ribs, 0.0, "pipe_cutter")
    cut_plate = panel_cutter(V, ribs, PLATE_T, "boot_cutter")
    level = []

    # ---- the form-fitting mounting plate, fasteners through it, the beads at its edge (panel frame)
    prism("boot_plate", "existing", profile_band(V, -B, B, ribs, PLATE_T), -B, B, M("rubber"))
    n = 0
    for edge in range(4):
        for i in range(int((2 * (B - FAST_IN)) // FAST_PITCH) + 1):
            s = -(B - FAST_IN) + i * FAST_PITCH
            x, y = (s, (B - FAST_IN) * (1 if edge == 0 else -1)) if edge < 2 else ((B - FAST_IN) * (1 if edge == 2 else -1), s)
            z = panel_z(V, x, ribs)
            if z is None:
                continue
            z += PLATE_T
            cyl(f"fastener_boot_washer_{n}", "existing", 0.31 * IN, 0.06 * IN, x * IN, y * IN, (z + 0.03) * IN, M("fast"), verts=16)
            cyl(f"fastener_boot_head_{n}", "existing", 0.19 * IN, 0.2 * IN, x * IN, y * IN, (z + 0.16) * IN, M("fast"), verts=6)
            n += 1
    bw, bh = BEAD_BASE
    for layer, nm, mat, w, h in (("existing", "mastic_before", "mastic", bw * 1.8, bh * 1.5), ("primer", "sealant", "seal", bw, bh)):
        e = B + w
        for sg, tag in ((1, "up"), (-1, "dn")):     # across the ribs, up- and down-slope of the plate
            y0, y1 = (B, e) if sg > 0 else (-e, -B)
            prism(f"{nm}_base_{tag}", layer, profile_band(V, -e, e, ribs, h), y0, y1, M(mat))
        for sg, tag in ((1, "r"), (-1, "l")):       # along the slope, beside it (on a pan)
            box(f"{nm}_base_{tag}", layer, w * IN, 2 * B * IN, h * IN, sg * (B + w / 2) * IN, 0, h / 2 * IN, M(mat))

    # ---- Flex (and primer, topcoat) over the plate, its fasteners and bead (the 4" onto the panel is the apron above)
    for k, (layer, mat) in enumerate(LAYERS3):
        e = B + bw + 0.25 + (0.3 if k else 0) + (0.36 if k == 2 else 0)
        prism(f"{layer}_plate", layer, profile_band(V, -e, e, ribs, PLATE_T + APRON_T[k] + 0.12), -e, e, M(mat), LIFT[k])

    # ---- the pipe, the boot, band and top bead (level frame: plumb), cut to stand on the panel / the plate
    pipe = Shell().tube(PIPE_R * IN, (PIPE_R - PIPE_WALL) * IN, -6 * IN, PIPE_H * IN).emit("existing", "pipe", M("castiron"))
    cut(pipe, cut_panel); level.append(pipe)
    boot_poly = [(r * IN, z * IN) for r, z in BOOT] + [((PIPE_R + 0.05) * IN, COLLAR_TOP * IN), ((PIPE_R + 0.05) * IN, -2 * IN)]
    boot = Shell().ring(boot_poly, seg=48).emit("existing", "boot", M("rubber")); cut(boot, cut_plate); level.append(boot)
    level.append(Shell().tube(BAND[0] * IN, 2.6 * IN, BAND[1] * IN, BAND[2] * IN).emit("existing", "boot_band", M("fast")))
    level.append(Shell().torus((PIPE_R + BEAD_TOP) * IN, BEAD_TOP * IN, (COLLAR_TOP + 0.08) * IN).emit("primer", "sealant_top", M("seal")))
    level.append(Shell().torus((PIPE_R + BEAD_TOP * 1.4) * IN, BEAD_TOP * 1.5 * IN, (COLLAR_TOP + 0.08) * IN).emit("existing", "mastic_before_top", M("mastic")))

    # ---- the coats up the boot: over the steps, the top bead, and up the pipe past the EPDM
    path = BOOT + [(2.65, COLLAR_TOP + 0.45), (PIPE_R, COLLAR_TOP + 0.6)]
    tops = [COLLAR_TOP + UP_PIPE, COLLAR_TOP + UP_PIPE, COLLAR_TOP + 2 * UP_PIPE]
    for k, (layer, mat) in enumerate(LAYERS3):
        p = [(r * IN, z * IN) for r, z in path + [(PIPE_R, tops[k])]]
        shell_poly = band(p, 0.0, CURB_COAT[k] * IN)
        c = Shell().ring(shell_poly, seg=48).emit(layer, f"{layer}_boot", M(mat)); cut(c, cut_plate); level.append(c)

    level_to_panel(V.A, level)
    print(f"\n{V.name}: plate {2 * B:.0f} in, Flex to {AX[1] / 12:.2f} x {AY[1] / 12:.2f} ft; bay {2 * V.hx} x {2 * V.hz} ft")
    return finalize(V.name)


# (tag, pitch, bay half-width per roof, R-panel lap phase)
for tag, pitch, phase in (("1in12", 1, 0.5), ("1p5in12", 1.5, 2.5)):
    for surface, hx in (("rpanel", 3), ("sseam", 2)):
        V = Variant(f"pipe-boot-{surface}-{tag}-P-9-MP", surface, pitch, 0, 0, 0, hx=hx, hz=2, lap_phase=phase, rows=(),
                    rust=[(0.0, 19.5, 0.8), (-24.0, -8.0, 1.0)])
        build(V, PLATE[surface])
