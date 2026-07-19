import json
import networkx as nx

# -------------------------------
# Dependencies you already have:
# - validate_narrator_json(json_obj)
# - apply_narrator_impacts(G, narrator_json)
# -------------------------------

class MeshTurnEngine:
    """
    A full turn-cycle engine for The Mesh.
    Handles:
      - narrator event generation (via LLM)
      - JSON validation
      - applying impacts to the graph
      - updating crisis state
      - advancing turns
    """

    def __init__(self, G, narrator_llm, crisis_state):
        """
        G: NetworkX graph
        narrator_llm: function(prompt) -> JSON string from LLM
        crisis_state: dict tracking current crisis type, severity, turn number
        """
        self.G = G
        self.narrator_llm = narrator_llm
        self.crisis_state = crisis_state

    def generate_narrator_event(self):
        """
        Calls the LLM narrator to generate a JSON crisis event.
        """
        system_prompt = self._build_system_prompt()
        raw_output = self.narrator_llm(system_prompt)

        try:
            narrator_json = json.loads(raw_output)
        except json.JSONDecodeError:
            raise ValueError("Narrator output is not valid JSON.")

        return narrator_json

    def _build_system_prompt(self):
        """
        Build the system prompt for the narrator based on crisis state.
        """
        crisis_type = self.crisis_state.get("type", "Unknown")
        severity = self.crisis_state.get("severity", 1)
        turn = self.crisis_state.get("turn", 0)

