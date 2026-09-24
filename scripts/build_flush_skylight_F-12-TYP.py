"""
build_flush_skylight_F-12-TYP.py — flush-mounted translucent skylight panel in a sloped metal roof per RMI detail F-12-TYP
(FLUSH MOUNTED SKYLIGHT PANEL – TYPICAL, 11/05/24). NO 3D CONCEPT RENDER EXISTS for this detail: everything past the sheet's
one section through a side lap is ASSUMED. Spliced into the slope like the F-8-TYP lap (index.html: SLOPE_BAY.mskylight,
unitAt) at every skylight on the manufacturing and airport-hangar roofs.

    blender -b --python scripts/build_flush_skylight_F-12-TYP.py

What the drawing says (VERIFIED):
  * (E) or new skylight panel lapped into the (E) adjacent metal roof panel at a rib: the skylight panel comes up over the
    metal rib and the two are fastened through the crest; double-sided butyl tape in the lap for (N) panels.
  * "RMI-FLEX VAPOR BARRIER-FLASHING COAT. ENCAPSULATE FASTENERS AND LAPS. EXTEND A MIN. 3" ONTO SKYLIGHT PANEL."
  * "RMI-THANE, RMI-WHITE. EXTEND A MIN. 1" PAST RMI-FLEX ONTO SKYLIGHT." — and over the whole metal field.
  * (Optional) RMI-Flex base coat to the metal field. Replace damaged, loose or missing fasteners; treat rusted metal.
  * Note 12: covering skylight panels with RMI-Flex / Thane / White is PROHIBITED unless regulatory-approved fall
    protection is installed over the panel — so the panel face stays clear; only its laps and fasteners are coated.
  * Note 7: applies to all seams, laps and flashing transitions — read here as covering the panel's end laps too.
  * Note 8: replace damaged panels (including exposed glass fibres); new panels to meet fall-resistance ratings.
ASSUMED (the sheet is NTS and shows one side lap only): the panel spans one R-panel sheet between two lap ribs (36") or one
standing-seam pan between two seams (24"), with the metal's own profile; how it laps at the ends (metal over the panel
up-slope, panel over the metal down-slope, 6" laps, fasteners across each at the pans); that "3" onto the skylight" is
measured from where the panel's flat starts (the rib base on R-panel, the seam leg on standing seam) — 3-1/4" modelled,
topcoat 1-1/4" past the Flex; the Flex 3" onto the metal past an end lap; the purlin fasteners through the panel's own ribs
(Flex and topcoat dabs on them, as on every exposed fastener); panel lengths (10 ft manufacturing, 14 ft hangar); sheet
thicknesses; coat thicknesses. The butyl tape is not drawn (the (E) panel is shown sound).

Four models, R-panel and standing seam for each length:
    models/flush-skylight-{rpanel,sseam}-10ft-F-12-TYP.glb     manufacturing (x = -82, -52, -22, 8, 38, 68; z = 32 ft)
    models/flush-skylight-{rpanel,sseam}-14ft-F-12-TYP.glb     airport hangar, both slopes (x = -130 ... 122 by 42; z = 35 ft)
Every skylight sits between two R-panel lap ribs (x = lap + 1.5 ft, an even x — which is also a standing-seam pan centre),
so one lap phase serves all; the purlin rows cross each bay at the same offsets.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rmi_blender import IN, M, box, cyl, reset_scene, finalize, offset_path
from rmi_metal_curb import (Variant, rib_offsets, rib_xs, is_lap, rib_coat, apron_top, panel_top, prism, SEAM, SHELLS,
                            LAP_TP, LAP_TF, LAP_TT, LAP_FOOT, APRON_T, LIFT, LAYERS3, FIELD_TT, FAST, SHEET_T, RP_B, RP_T, RP_H, RIBO)

LAPL = 6.0                      # end laps                                       ASSUMED
SKY_T = 0.07                    # skylight sheet (drawn, sits 0.01" on the metal)
ONTO_SKY = 3.25                 # Flex onto the skylight past where its flat starts (VERIFIED min 3")
PAST_FLEX = 1.25                # topcoat past the Flex onto the skylight (VERIFIED min 1")
ONTO_METAL = 3.0                # Flex onto the metal past an end lap               ASSUMED
LAP_EDGE = {"rpanel": 18.0, "sseam": 12.0}      # the panel's side laps: the lap ribs / the seams either side


def lap_asym(V, k, inner_sign):
    """Coat k over a side-lap rib (or seam) with the skylight on side `inner_sign` (-1: toward -x): the metal side keeps the
    app's profile, the skylight side runs ONTO_SKY past the panel's flat edge (and the topcoat PAST_FLEX beyond)."""
    if V.surface == "rpanel":
        off = APRON_T[k]; xs = rib_xs(off); H = RP_H; hw = RP_B / 2
        metal = hw + LAP_FOOT + (LAP_TF if k >= 1 else 0) + (LAP_TT if k >= 2 else 0)
        sky = hw + ONTO_SKY + (-0.25 if k == 0 else 0) + (PAST_FLEX if k == 2 else 0)
        right = lambda f: [(f, 0.0), (f, off), (xs(off), off), (xs(H + off), H + off)]
    else:
        o, f0 = SHELLS[k]
        metal = (0.16 + f0) * 12
        flex = max((0.16 + SHELLS[min(k, 1)][1]) * 12, 0.84 + ONTO_SKY + (-0.25 if k == 0 else 0))   # the app's shell already reaches past 3"
        sky = flex + (PAST_FLEX if k == 2 else 0)
        right = lambda f: [(f, 0.0), (f, (0.03 + o) * 12), ((0.12 + o) * 12, (0.03 + o) * 12), ((0.12 + o) * 12, 2.4),
                           ((0.18 + o) * 12, 2.4), ((0.18 + o) * 12, (0.31 + o) * 12)]
    fl, fr = (sky, metal) if inner_sign < 0 else (metal, sky)
    return [(-x, z) for x, z in reversed(right(fl))] + right(fr)


def build(V, sky_len):
    reset_scene()
    X, Y = V.hx * 12, V.hz * 12
    ribs = rib_offsets(V)
    E = LAP_EDGE[V.surface]
    flat = E - (RP_B / 2 if V.surface == "rpanel" else 0.84)     # where the skylight's own flat begins, each side
    y_dn, y_up = -sky_len / 2, sky_len / 2                         # the panel's visible ends: its own edge / the metal's edge
    hole = (flat, y_dn + LAPL, y_up)                                # no metal under the panel here

    # ---- metal: the pan round the hole, ribs (the panel's own ribs only in metal beyond its ends), rust
    for nm, (x0, x1, y0, y1) in {"up": (-X, X, hole[2], Y), "dn": (-X, X, -Y, hole[1]), "l": (-X, -hole[0], hole[1], hole[2]),
                                 "r": (hole[0], X, hole[1], hole[2])}.items():
        box(f"panel_{nm}", "existing", (x1 - x0) * IN, (y1 - y0) * IN, SHEET_T * IN, (x0 + x1) / 2 * IN, (y0 + y1) / 2 * IN, -SHEET_T / 2 * IN, M("panel"))
    for i, r in enumerate(ribs):
        prof = ([(r - RP_B / 2, 0), (r - RP_T / 2, RP_H), (r + RP_T / 2, RP_H), (r + RP_B / 2, 0)] if V.surface == "rpanel"
                else [(r + x * 12, z * 12) for x, z in SEAM])
        if abs(r) < E - 0.01:                       # under the skylight: metal only where the panel's ends lap it
            prism(f"rib_{i}_dn", "existing", prof, -Y, hole[1], M("panel"), caps=(False, True))
            prism(f"rib_{i}_up", "existing", prof, hole[2], Y, M("panel"), caps=(True, False))
        else:
            prism(f"rib_{i}", "existing", prof, -Y, Y, M("panel"), caps=(False, False))
    for i, (x, y, rr) in enumerate(V.rust):
        cyl(f"rust_{i}", "existing", rr * IN, 0.01 * IN, x * IN, y * IN, 0.006 * IN, M("rust"), verts=20)

    # ---- the translucent panel: the metal's profile, over the lap ribs (R-panel) or between the seam legs; dark below
    if V.surface == "rpanel":
        x1 = E + RP_B / 2 + 0.75
        path = panel_top(V, -x1, x1, [r for r in ribs if abs(r) <= E + 0.01])[::-1]    # right to left: panel below, on the left
        sec = offset_path(path, SKY_T + 0.01) + offset_path(path, 0.01)[::-1]
    else:
        x1 = E - 0.84
        sec = [(-x1, 0.01), (x1, 0.01), (x1, SKY_T + 0.01), (-x1, SKY_T + 0.01)]
    prism("skylight_panel", "existing", sec, y_dn, y_up, M("frp"))
    # the building's inside, seen through the panel: runs a foot under the metal all round, or the view past its edge at an
    # angle lands on the attic below and reads as a white strip
    box("skylight_interior", "existing", (2 * flat + 24) * IN, (y_up - y_dn + 24) * IN, 0.2 * IN, 0, (y_dn + y_up) / 2 * IN, -6 * IN, M("interior"))

    # ---- fasteners: purlin rows through every crest (the panel's own ribs too — Flex and topcoat dabs, as on every exposed
    # fastener), and across each end lap at the pans
    if V.surface == "rpanel":
        for j, y in enumerate(V.rows):
            for i, r in enumerate(ribs):
                z = FAST["z"] + (SKY_T + 0.01 if abs(r) <= E + 0.01 and y_dn < y < y_up else 0)
                cyl(f"fastener_{j}_{i}", "existing", FAST["r"] * IN, FAST["h"] * IN, r * IN, y * IN, z * IN, M("fast"), verts=10)
                cyl(f"flex_dab_{j}_{i}", "flex", FAST["fr"][1] * IN, FAST["h"] * IN, r * IN, y * IN, (z + 0.06) * IN, M("flex"), verts=14, r2=FAST["fr"][0] * IN)
                cyl(f"topcoat_dab_{j}_{i}", "topcoat", FAST["tr"][1] * IN, FAST["h"] * IN, r * IN, y * IN, (z + 0.12) * IN, M("thane"), verts=14, r2=FAST["tr"][0] * IN)
    xs_lap = [-13.0, -11.0, -1.5, 1.5, 11.0, 13.0] if V.surface == "rpanel" else [-9.0, -3.0, 3.0, 9.0]
    for tag, y in (("dn", y_dn + 2.0), ("up", y_up + 2.5)):
        for i, x in enumerate(xs_lap):
            cyl(f"fastener_endlap_{tag}_{i}_washer", "existing", 0.31 * IN, 0.06 * IN, x * IN, y * IN, (SKY_T + 0.04) * IN, M("fast"), verts=16)
            cyl(f"fastener_endlap_{tag}_{i}_head", "existing", 0.19 * IN, 0.2 * IN, x * IN, y * IN, (SKY_T + 0.17) * IN, M("fast"), verts=6)

    # ---- coats. Metal field: topcoat everywhere but the panel face. Side laps: the app's profile beyond the panel's ends,
    # the skylight side run 3-1/4" onto it along the panel. End laps: a band across, 3-1/4" onto the panel, 3" onto the metal.
    t = FIELD_TT
    for nm, (x0, x1_, y0, y1) in {"up": (-X, X, y_up, Y), "dn": (-X, X, -Y, y_dn), "l": (-X, -flat, y_dn, y_up), "r": (flat, X, y_dn, y_up)}.items():
        box(f"topcoat_field_{nm}", "topcoat", (x1_ - x0) * IN, (y1 - y0) * IN, t * IN, (x0 + x1_) / 2 * IN, (y0 + y1) / 2 * IN, t / 2 * IN, M("thane"))
    band_dn = [(y_dn - ONTO_METAL + 0.25, y_dn + ONTO_SKY - 0.25), (y_dn - ONTO_METAL, y_dn + ONTO_SKY), (y_dn - ONTO_METAL - 0.36, y_dn + ONTO_SKY + PAST_FLEX)]
    band_up = [(y_up - ONTO_SKY + 0.25, y_up + ONTO_METAL - 0.25), (y_up - ONTO_SKY, y_up + ONTO_METAL), (y_up - ONTO_SKY - PAST_FLEX, y_up + ONTO_METAL + 0.36)]
    for i, r in enumerate(ribs):
        lap = is_lap(V, r)
        for k, (layer, mat) in enumerate(LAYERS3):
            if abs(r) < E - 0.01:                   # the panel's own ribs: coated only in the metal beyond its ends
                poly = rib_coat(V, k, lap)
                if poly is None:
                    continue
                poly = [(r + x, z) for x, z in poly]
                prism(f"{layer}_rib_{i}_dn", layer, poly, -Y, band_dn[k][0], M(mat), LIFT[k], caps=(False, True))
                prism(f"{layer}_rib_{i}_up", layer, poly, band_up[k][1], Y, M(mat), LIFT[k], caps=(True, False))
            elif abs(abs(r) - E) < 0.01:            # a side lap: symmetric beyond the panel, skylight side widened along it
                sym = [(r + x, z) for x, z in rib_coat(V, k, True)]
                asym = [(r + x, z) for x, z in lap_asym(V, k, -1 if r > 0 else 1)]
                prism(f"{layer}_lap_{i}_dn", layer, sym, -Y, band_dn[k][0], M(mat), LIFT[k], caps=(False, True))
                prism(f"{layer}_lap_{i}", layer, asym, band_dn[k][0], band_up[k][1], M(mat), LIFT[k])
                prism(f"{layer}_lap_{i}_up", layer, sym, band_up[k][1], Y, M(mat), LIFT[k], caps=(True, False))
            else:
                poly = rib_coat(V, k, lap)
                if poly is not None:
                    prism(f"{layer}_rib_{i}", layer, [(r + x, z) for x, z in poly], -Y, Y, M(mat), LIFT[k], caps=(False, False))
        # end-lap bands, across both side laps (their metal-side feet) and every rib between, following the profile
    for k, (layer, mat) in enumerate(LAYERS3):
        ext = E + (RP_B / 2 + LAP_FOOT + (LAP_TF if k >= 1 else 0) + (LAP_TT if k >= 2 else 0) if V.surface == "rpanel"
                   else (0.16 + SHELLS[k][1]) * 12) + 0.05
        sec = apron_top(V, k, -ext, ext, [r for r in ribs if abs(r) <= E + 0.01])
        prism(f"{layer}_endlap_dn", layer, sec, band_dn[k][0], band_dn[k][1], M(mat), LIFT[k] + 0.07)
        prism(f"{layer}_endlap_up", layer, sec, band_up[k][0], band_up[k][1], M(mat), LIFT[k] + 0.07)
    print(f"\n{V.name}: {sky_len / 12:.0f}-ft panel, {2 * E:.0f} in between laps; bay {2 * V.hx} x {2 * V.hz} ft")
    return finalize(V.name)


# (tag, panel length in, bay half-length ft, purlin rows in, +up-slope from the panel's centre)
for tag, sky_len, hz, rows in (("10ft", 120.0, 6, (36.0, -24.0)), ("14ft", 168.0, 8, (72.0, 12.0, -48.0))):
    for surface, hx in (("rpanel", 3), ("sseam", 2)):
        V = Variant(f"flush-skylight-{surface}-{tag}-F-12-TYP", surface, 1, 0, 0, 0, hx=hx, hz=hz, lap_phase=1.5, rows=rows,
                    rust=[(0.0, sky_len / 2 + 8, 0.9), (0.0, -sky_len / 2 - 8, 0.8)])     # on the metal pans past the panel's ends
        build(V, sky_len)
