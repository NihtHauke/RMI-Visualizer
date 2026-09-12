"""
rmi_curb.py — the curb core shared by every curb-mounted unit model.

CS-1-TYP (CURB MOUNTED UNITS - TYPICAL, 11/05/24) note 7, VERIFIED, quoted from the drawing:

    "DETAIL EQUALLY APPLIES TO ALL CURB MOUNTED UNITS THAT CAN BE LIFTED INCLUDING VENTS, DUCTS,
     SOIL STACKS, CONDUIT PENETRATIONS, HVAC, REFRIGERATION PENETRATIONS, ACCESS HATCH, SMOKE
     HATCH, SKYLIGHTS DOMES."

So the roof hatch, the curb-mounted skylight, the kitchen exhaust fan and the bin vent are all the
SAME assembly as the RTU — one curb, one set of coatings, a different unit on top. That is what this
module is: build_curb_mounted_unit_CS-1-TYP.py's curb, lifted out so the four derived units share it.

What the drawing says (VERIFIED, all four units):
  * (E) CURB. TYPE MAY VARY. (E) FLASHING. (E) FASTENER.
  * "(E) LIFT & RESET UNIT AFTER RMI SYSTEM HAS FULLY CURED. FASTEN WITH STAINLESS STEEL SCREWS
    W/EPDM WASHERS."  -> unit parts are named existing__unit_* so the app seats/lifts them.
  * "RMI-FLEX VAPOR BARRIER-FLASHING COAT. EXTEND TO INTERIOR OF CURB. ENCAPSULATE (E) FLASHING."
    -> the wrap runs up the outside, over the nailer and turns down INSIDE the curb (curb_return).
  * "RMI-THANE, RMI WHITE" over all.
  * "CLEAN, REPAIR, PREPARE AND PRIME PER RMI SPECIFICATION GUIDE MANUAL FOR EACH TYPE OF SURFACE
    OR ROOF SYSTEM."
  * Note 8: "DETAIL APPLIES TO ALL (E) BUR, MODIFIED BITUMEN, EPDM, PVC, TPO, SYSTEMS REGARDLESS OF
    DECK AND INSULATION CONFIGURATION."  -> membrane roofs. Exposed concrete is CS-12-CON (liftable)
    / CS-14-CON (fixed); exposed metal curbs are CS-13-MP (liftable) / CS-15-MP (fixed).
  * Note 9: perform adhesion test and moisture scan before installation.

ASSUMED (the drawing is NOT TO SCALE and carries no dimensions): every number below — curb footprint
and height, wall and skirt thickness, how far up the curb the skirt starts, the nailer, fastener size
and 12" o.c. spacing, the sealant bead, how far the Flex runs onto the field (18", the same figure the
RTU and D-1-TYP drain models use), how far it turns down inside the curb (3"), and every coat thickness.

Usage from a unit script:

    from rmi_curb import curb_core
    C = curb_core(curb_w_in=48.0, curb_h_in=16.8)      # builds patch + curb + coatings
    ... add the unit on top at C["top"] ...
    finalize("kitchen-exhaust-fan-CS-1-TYP")

curb_core() returns the numbers the app needs for its mount (printed by each script):
    top        top of the nailer, metres  — where the unit sits
    patch_half half the roof patch, feet  — the membrane cutout goes just inside this
    flex_half  half the Flex apron, feet  — the coating cutout goes just inside this
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rmi_blender import IN, M, box, cyl, helper, cut, link

M2FT = 3.28084

# ---------------------------------------------------------------- shared dimensions (inches; ASSUMED)
WT_IN        = 0.6      # curb wall (sheet-metal curb box)
SKIRT_T_IN   = 0.2      # (E) flashing skirt thickness
SKIRT_FRAC   = 0.6      # skirt covers the top 60% of the curb wall
NAILER_IN    = 1.5      # wood nailer on the curb top
FAST_PITCH   = 12.0     # fasteners through the skirt, 12" o.c.
FAST_R_IN    = 0.22
FAST_L_IN    = 0.12
BEAD_IN      = 0.35     # sealant bead at the curb base
APRON_IN     = 18.0     # Flex onto the field past the curb  (same figure as the RTU / drain models)
PATCH_PAD_IN = 9.0      # roof patch carries on past the coatings so the cutout has something to sit in
RETURN_IN    = 3.0      # "EXTEND TO INTERIOR OF CURB" — how far down inside (ASSUMED)

# (E) roof build-up under a membrane roof
DECK_IN, INSUL_IN, MEM_IN = 0.6, 3.0, 0.1

# coats, innermost first; each sits one COAT_STEP outboard of / above the one before
COAT = [("primer", "primer"), ("flex", "flex"), ("topcoat", "thane")]
COAT_STEP_IN = 0.06
APRON_T_IN = 0.05


def _tube(name, layer, outer, inner, z0, z1, m):
    """Hollow square tube: a box from z0..z1 with a rectangular hole of half-width `inner` cut out."""
    o = box(name, layer, 2 * outer, 2 * outer, z1 - z0, 0, 0, (z0 + z1) / 2, m)
    cut(o, helper(box(f"{name}_cutter", layer, 2 * inner, 2 * inner, (z1 - z0) * 3, 0, 0, (z0 + z1) / 2, m)))
    return o


def curb_core(curb_w_in, curb_h_in, substrate=True, skirt=True, fasteners=True):
    """Build the (E) roof patch, the (E) curb and the three coats. Returns the mount numbers.

    substrate=False leaves the roof patch out (the caller supplies its own).
    skirt/fasteners=False drops the sheet-metal flashing skirt — exposed concrete curbs (CS-12-CON)
    have no (E) flashing to encapsulate.
    """
    CW = curb_w_in * IN
    CH = curb_h_in * IN
    WT = WT_IN * IN
    ST = SKIRT_T_IN * IN
    NAIL = NAILER_IN * IN
    top = CH + NAIL                                   # top of the nailer — the unit sits here

    apron_half_in = curb_w_in / 2 + APRON_IN
    patch_half_in = apron_half_in + PATCH_PAD_IN
    PATCH = 2 * patch_half_in * IN

    # ---------------------------------------------------------------- (E) roof assembly
    if substrate:
        z_mem = MEM_IN * IN
        box("steel_deck", "existing", PATCH, PATCH, DECK_IN * IN, 0, 0, -(INSUL_IN + DECK_IN / 2) * IN, M("deck"))
        box("insulation", "existing", PATCH, PATCH, INSUL_IN * IN, 0, 0, -(INSUL_IN / 2) * IN, M("insulation"))
        box("membrane", "existing", PATCH, PATCH, z_mem, 0, 0, z_mem / 2, M("membrane"))

    # ---------------------------------------------------------------- (E) curb: four walls + skirt + nailer
    for i, (x, y, sx, sy) in enumerate([(0, CW / 2 - WT / 2, CW, WT), (0, -(CW / 2 - WT / 2), CW, WT),
                                        (CW / 2 - WT / 2, 0, WT, CW), (-(CW / 2 - WT / 2), 0, WT, CW)]):
        box(f"curb_wall_{i}", "existing", sx, sy, CH, x, y, CH / 2, M("curb"))
    outer = CW / 2
    if skirt:
        sk_z0 = CH * (1 - SKIRT_FRAC)
        _tube("flashing_skirt", "existing", CW / 2 + ST, CW / 2, sk_z0, CH, M("coping"))
        outer = CW / 2 + ST
    # the nailer is a RING on top of the curb walls, not a lid: the coating has to cross it and turn down
    # inside, and on a skylight or hatch the curb throat is open. (A solid slab here left bare wood showing.)
    _tube("nailer", "existing", CW / 2, CW / 2 - WT, CH, CH + NAIL, M("wood"))

    # fasteners through the skirt near the top, 12" o.c., pointing into the curb
    if skirt and fasteners:
        face = outer + 0.0015
        fz = CH - min(2.5, curb_h_in * 0.17) * IN
        n = max(1, int((curb_w_in - 8) // FAST_PITCH))
        span = [(i - (n - 1) / 2) * FAST_PITCH * IN for i in range(n + 1)] if n else [0.0]
        for s in span:
            for side, (x, y, rot) in enumerate([(s, face, (1.5708, 0, 0)), (face, -s, (0, 1.5708, 0)),
                                                (-s, -face, (-1.5708, 0, 0)), (-face, s, (0, -1.5708, 0))]):
                f = cyl(f"fastener_{side}_{round(s / IN)}", "existing", FAST_R_IN * IN, FAST_L_IN * IN,
                        x, y, fz, M("fast"), verts=16)
                f.rotation_euler = rot

    # ---------------------------------------------------------------- sealant bead at the curb base (prep work)
    bo = outer + BEAD_IN * IN / 2
    bead = BEAD_IN * IN
    for i, (x, y, sx, sy) in enumerate([(0, bo, 2 * outer + 2 * bead, bead), (0, -bo, 2 * outer + 2 * bead, bead),
                                        (bo, 0, bead, 2 * outer + 2 * bead), (-bo, 0, bead, 2 * outer + 2 * bead)]):
        box(f"sealant_bead_{i}", "primer", sx, sy, bead, x, y, bead * 0.8, M("seal"))

    # ---------------------------------------------------------------- coats: field apron + wrap up/over + interior return
    # Flex "EXTEND TO INTERIOR OF CURB. ENCAPSULATE (E) FLASHING" — outside face, over the nailer, down inside.
    inner_face = CW / 2 - WT
    wrap_inner = outer
    for idx, (layer, matname) in enumerate(COAT):
        m = M(matname)
        step = (idx + 1) * COAT_STEP_IN * IN
        # field apron
        aw = 2 * (apron_half_in * IN) + 2 * step
        box("field_apron", layer, aw, aw, APRON_T_IN * IN, 0, 0, (MEM_IN + 0.05) * IN + step, m)
        # up the outside face of the curb, each coat nesting over the one before
        wrap_outer = outer + step
        _tube("curb_wrap", layer, wrap_outer, wrap_inner, 0, CH, m)
        wrap_inner = wrap_outer
        # over the nailer and down inside the curb throat — "EXTEND TO INTERIOR OF CURB".
        # One piece: its top covers the curb top, its inner wall is the turn-down to RETURN_IN below the top.
        _tube("curb_cap", layer, wrap_outer, inner_face - step, top - RETURN_IN * IN, top + step, m)

    # the inside of the curb, below the turn-down: dark, so the throat does not read as a hole through the roof
    box("curb_interior", "existing", 2 * inner_face, 2 * inner_face, 0.2 * IN, 0, 0,
        top - (RETURN_IN + 1.0) * IN, M("unitD"))

    return {
        "top": top,
        "curb_half_ft": (curb_w_in / 2) * IN * M2FT,
        "patch_half_ft": patch_half_in * IN * M2FT,
        "flex_half_ft": (apron_half_in * IN + 2 * COAT_STEP_IN * IN) * M2FT,
    }


def report(name, C):
    """Print the numbers index.html needs for the mount (cutouts sit just inside each extent)."""
    print(f"\n{name}:")
    print(f"  unit sits at z = {C['top'] / IN:.2f} in  ({C['top'] * M2FT:.3f} ft)")
    print(f"  roof patch half-width {C['patch_half_ft']:.3f} ft  -> hMem  {C['patch_half_ft'] - 0.10:.2f}")
    print(f"  Flex apron half-width {C['flex_half_ft']:.3f} ft  -> hCoat {C['flex_half_ft'] - 0.21:.2f}")
