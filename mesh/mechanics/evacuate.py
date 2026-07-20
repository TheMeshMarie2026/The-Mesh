"""
mechanics/evacuate.py

Example mechanic: moves population/assets from one node to a connected
"safe" node. Kept intentionally simple - this file is the reference
pattern for every future mechanic.
"""

from mechanics.base import Mechanic, MechanicResult
from mechanics.registry import register_mechanic


@register_mechanic
class EvacuateMechanic(Mechanic):
    id = "evacuate"
    description = "Moves population from a source node to a connected target node."

    def execute(self, graph, action: dict, context: dict | None = None) -> MechanicResult:
        source = action["source_node"]
        target = action["target_node"]
        amount = action.get("amount", 0)

        # NOTE: actual graph mutation should go through engine/graph/'s
        # node/edge operations API once that's wired in here. Left as a
        # stub so this file runs standalone for now.

        return MechanicResult(
            success=True,
            effects={"source": source, "target": target, "moved": amount},
            message=f"Evacuated {amount} from '{source}' to '{target}'.",
        )
