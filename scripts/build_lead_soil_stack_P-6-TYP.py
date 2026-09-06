"""
build_lead_soil_stack_P-6-TYP.py — soil stack with (E) lead flashing, per RMI detail P-6-TYP
(SOIL STACK (LEAD) – TYPICAL, 11/05/24) with P3SP-11-FT-3D (SOIL STACK – CONCEPT DRAWING, 9/1/21)
as the 3D reference.

    blender -b --python scripts/build_lead_soil_stack_P-6-TYP.py

What the 2D drawing says (this is the logic the model follows):
  * (E) soil stack through the (E) BUR roof system. Note 7: equally applies to conduit, HVAC and
    refrigeration penetrations. Note 8: applies to all (E) BUR & mod-bit regardless of deck/insulation.
  * (E) lead flashing runs up the outside of the stack, over the top and turns down inside the bore;
    its base flange lies on the roof. "Replace damaged, ill-fitting lead."
  * Bead of RMI approved sealant at the base of the vertical lead (the two dots on the section).
  * Note 10: clean, prepare and prime per the RMI Specification Guide Manual.
  * RMI-Flex vapor barrier-flashing coat: encapsulates the lead flashing and EXTENDS INSIDE the stack.
  * RMI-Thane / RMI-White: EXTENDS PAST RMI-Flex (further out on the field, further down the bore).

What the drawing does NOT say: it is NOT TO SCALE and carries no dimensions at all. Every number
below is therefore ASSUMED and is written out so RMI can correct it. The (E) roof build-up matches
cast-iron-drain-D-1-TYP so the two read alike on one roof.

Every layer ships as ONE mesh (the hotel roof carries 33 of these), built with rmi_blender.Shell so
there are no boolean helpers to bake or delete.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from rmi_blender import IN, M, Shell, reset_scene, finalize

# ---------------------------------------------------------------- dimensions (all ASSUMED — see docstring)
# (E) roof assembly carried by the model. Metric so it sits at exactly the drain model's heights.
PATCH_R    = 16.0 * IN      # radius of the roof patch under the detail (keeps clear of 4-ft pipe clusters)
DECK_Z0, DECK_Z1 = -0.079, -0.064   # steel deck
INSUL_Z1   = 0.000                  # insulation up to the underside of the membrane
MEM_TOP    = 0.003                  # (E) cap sheet / membrane top = the roof surface the app sees at y=0

# (E) soil stack — 4" nominal cast iron. Drawing is NOT TO SCALE; 4" is the common soil/vent size.
STACK_OD   = 4.5  * IN
STACK_ID   = 4.0  * IN
STACK_UP   = 24.0 * IN      # above the roof. Drawing proportion reads ~5 diameters; 24" is typical.
STACK_DOWN = 10.0 * IN      # below the deck, so the section view shows it passing through

# (E) lead flashing — "replace damaged, ill fitting lead"
LEAD_T     = 0.0625 * IN    # 4-lb sheet lead
FLANGE_R   = 7.0 * IN       # base flange 14" across (a stock 4" lead roof flashing is ~12–14" square)
TURNDOWN   = 1.0 * IN       # lead folded down inside the bore — standard plumbing practice

# Bead of RMI approved sealant at the base of the vertical lead
BEAD_R     = 0.1875 * IN    # 3/8" bead

# Coatings. The drawing gives direction only: Flex encapsulates the lead and goes inside the stack;
# topcoat extends past the Flex. Field reach and bore depth are ASSUMED.
COAT       = 0.001          # visual thickness per layer (1 mm), same as the drain model
FIELD_R    = {"primer": 13.0 * IN, "flex": 13.0 * IN, "topcoat": 14.0 * IN}   # 6" past the flange; topcoat 1" past Flex
BORE_D     = {"primer":  6.0 * IN, "flex":  6.0 * IN, "topcoat":  7.0 * IN}   # down inside the stack; topcoat 1" past Flex

# ---------------------------------------------------------------- derived
STACK_TOP  = MEM_TOP + STACK_UP
FLANGE_TOP = MEM_TOP + LEAD_T
SLEEVE_OR  = STACK_OD / 2 + LEAD_T        # outside of the lead sleeve
RIM_TOP    = STACK_TOP + LEAD_T           # lead over the rim
BORE_IR    = STACK_ID / 2 - LEAD_T        # inside of the lead turn-down
TURN_BOT   = STACK_TOP - TURNDOWN


def coating(layer, i):
    """One coating layer as a nested shell: field → over the flange edge → over the flange → up the
    sleeve → over the rim → down the bore. i = 1 primer, 2 Flex, 3 topcoat (each one COAT further out)."""
    d0, d1 = (i - 1) * COAT, i * COAT
    s = Shell()
    s.tube(FIELD_R[layer], FLANGE_R + d0, MEM_TOP + d0, MEM_TOP + d1)                 # onto the field
    s.tube(FLANGE_R + d1, FLANGE_R + d0, MEM_TOP + d0, FLANGE_TOP + d1)               # step over the flange edge
    s.tube(FLANGE_R + d1, SLEEVE_OR + d0, FLANGE_TOP + d0, FLANGE_TOP + d1)           # over the lead flange
    s.tube(SLEEVE_OR + d1, SLEEVE_OR + d0, FLANGE_TOP + d0, RIM_TOP + d1)             # up the lead sleeve
    s.tube(SLEEVE_OR + d1, BORE_IR - d1, RIM_TOP + d0, RIM_TOP + d1)                  # over the rim
    s.tube(BORE_IR - d0, BORE_IR - d1, TURN_BOT, RIM_TOP + d1)                        # down the lead turn-down
    s.tube(STACK_ID / 2 - d0, STACK_ID / 2 - d1, STACK_TOP - BORE_D[layer], TURN_BOT)  # on down the bare bore
    if i >= 2:   # Flex and topcoat encapsulate the sealant bead as a cove at the base of the sleeve
        s.tube(SLEEVE_OR + 2 * BEAD_R + d1, SLEEVE_OR + d0, FLANGE_TOP, FLANGE_TOP + 2 * BEAD_R + d1)
    return s.emit(layer, layer, M(layer if layer != "topcoat" else "thane"))


reset_scene()

# (E) roof assembly — generic, per note 8
Shell().tube(PATCH_R, STACK_OD / 2, DECK_Z0, DECK_Z1).emit("existing", "steel_deck", M("deck"))
Shell().tube(PATCH_R, STACK_OD / 2, DECK_Z1, INSUL_Z1).emit("existing", "insulation", M("insulation"))
Shell().tube(PATCH_R, STACK_OD / 2, INSUL_Z1, MEM_TOP).emit("existing", "membrane", M("membrane"))

# (E) soil stack
Shell().tube(STACK_OD / 2, STACK_ID / 2, DECK_Z0 - STACK_DOWN, STACK_TOP).emit("existing", "soil_stack", M("castiron"))

# (E) lead flashing: flange on the roof, sleeve up the stack, over the rim, turned down inside
lead = Shell()
lead.tube(FLANGE_R, STACK_OD / 2, MEM_TOP, FLANGE_TOP)
lead.tube(SLEEVE_OR, STACK_OD / 2, FLANGE_TOP, STACK_TOP)
lead.tube(SLEEVE_OR, BORE_IR, STACK_TOP, RIM_TOP)
lead.tube(STACK_ID / 2, BORE_IR, TURN_BOT, STACK_TOP)
lead.emit("existing", "lead_flashing", M("lead"))

# Bead of RMI approved sealant at the base of the vertical lead — applied with the prep/prime work
Shell().torus(SLEEVE_OR + BEAD_R, BEAD_R, FLANGE_TOP + BEAD_R).emit("primer", "sealant_bead", M("seal"))

coating("primer", 1)
coating("flex", 2)
coating("topcoat", 3)

finalize("lead-soil-stack-P-6-TYP")
