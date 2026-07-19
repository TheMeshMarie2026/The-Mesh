import json
import networkx as nx

# ---------------------------------------------------------
# 1. VALIDATOR
# ---------------------------------------------------------

class NarratorJSONValidationError(Exception):
    pass

def validate_narrator_json(json_obj):
    required_top = {"narrative", "choices"}
    if not isinstance(json_obj, dict):
        raise NarratorJSONValidationError("Top-level JSON must be an object.")
    if not required_top.issubset(json_obj.keys()):
        raise NarratorJSONValidationError("Missing required fields.")

    if not isinstance(json_obj["narrative"], str):
        raise NarratorJSONValidationError("'narrative' must be a string.")

    choices = json_obj["choices"]
    if not isinstance(choices, list) or len(choices) != 3:
        raise NarratorJSONValidationError("'choices' must be a list of exactly 3 items.")

    for idx, choice in enumerate(choices):
        if "text" not in choice or "impact" not in choice:
            raise NarratorJSONValidationError(f"Choice {idx} missing required fields.")
        if not isinstance(choice["text"], str):
            raise NarratorJSONValidationError(f"Choice {idx} text must be a string.")

        impact = choice["impact"]
        required_impact = {"node_id", "resource_change", "trust_change", "edge_weight_change"}
        if not required_impact.issubset(impact.keys()):
            raise NarratorJSONValidationError(f"Choice {idx} impact missing fields.")

        if not isinstance(impact["node_id"], str):
            raise NarratorJSONValidationError(f"Choice {idx} node_id must be a string.")

        for field in ["resource_change", "trust_change", "edge_weight_change"]:
            if not isinstance(impact[field], (int, float)):
                raise NarratorJSONValidationError(f"Choice {idx} {field} must be numeric.")

    return True


# ---------------------------------------------------------
# 2. GRAPH IMPACT APPLICATION
# ---------------------------------------------------------

def apply_choice_impact(G: nx.DiGraph, impact: dict):
    node_id = impact["node_id"]
    if node_id not in G.nodes:
        raise ValueError(f"Node '{node_id}' not found in graph.")

    # Node-level updates
    G.nodes[node_id]["Resource_Capacity"] = G.nodes[node_id].get("Resource_Capacity", 0.0) + impact["resource_change"]
    G.nodes[node_id]["trust"] = G.nodes[node_id].get("trust", 0.0) + impact["trust_change"]

    # Edge-level updates (outgoing edges)
    updated_edges = []
    for _, tgt, attrs in G.out_edges(node_id, data=True):
        new_w = attrs.get("influence_weight", 0.0) + impact["edge_weight_change"]
        G[node_id][tgt]["influence_weight"] = new_w
        updated_edges.append((node_id, tgt, new_w))

    return {
        "node": node_id,
        "new_resource_capacity": G.nodes[node_id]["Resource_Capacity"],
        "new_trust": G.nodes[node_id]["trust"],
        "updated_edges": updated_edges
    }


# ---------------------------------------------------------
# 3. TURN ENGINE
# ---------------------------------------------------------

class CrisisEngine:
    def __init__(self, G, narrator_llm, crisis_state):
        self.G = G
        self.llm = narrator_llm
        self.crisis_state = crisis_state
        self.turn_log = []

    def generate_event(self):
        prompt = (
            f"Generate a crisis event for turn {self.crisis_state['turn']}. "
            f"Crisis type: {self.crisis_state['type']}. "
            f"Severity: {self.crisis_state['severity']}. "
            "Output ONLY valid JSON."
        )
        raw = self.llm(prompt)
        return json.loads(raw)

    def update_crisis_state(self):
        self.crisis_state["turn"] += 1
        self.crisis_state["severity"] *= 1.05
        return self.crisis_state

    def process_turn(self, choice_index):
        narrator_json = self.generate_event()
        validate_narrator_json(narrator_json)

        choice = narrator_json["choices"][choice_index]
        impact_result = apply_choice_impact(self.G, choice["impact"])
        new_state = self.update_crisis_state()

        turn_record = {
            "turn": new_state["turn"],
            "crisis_state": new_state,
            "narrative": narrator_json["narrative"],
            "selected_choice": choice,
            "impact_result": impact_result
        }

        self.turn_log.append(turn_record)
        return turn_record


# ---------------------------------------------------------
# 4. FULL CRISIS-PROCESSING LOOP
# ---------------------------------------------------------

def run_crisis_loop(G, narrator_llm, crisis_state, num_turns=5, choice_selector=None):
    """
    choice_selector: function(turn_number, narrator_json) -> choice_index
    Allows classroom UI, random selection, or AI-driven selection.
    """

    engine = CrisisEngine(G, narrator_llm, crisis_state)
    session_log = []

    for t in range(num_turns):
        narrator_json = engine.generate_event()
        validate_narrator_json(narrator_json)

        # Determine choice (UI, random, or rule-based)
        if choice_selector:
            choice_index = choice_selector(t, narrator_json)
        else:
            choice_index = 0  # default: always pick first choice

        # Apply impact + update crisis
        result = engine.process_turn(choice_index)
        session_log.append(result)

    return session_log


# ---------------------------------------------------------
# 5. EXAMPLE USAGE
# ---------------------------------------------------------

if __name__ == "__main__":
    G = nx.DiGraph()
    G.add_node("Microgrid_Consortium", Resource_Capacity=5.0, trust=0.6)
    G.add_node("Microgrid_Hackathon_Team", Resource_Capacity=3.0, trust=0.5)
    G.add_edge("Microgrid_Consortium", "Microgrid_Hackathon_Team", influence_weight=0.1)

    def fake_llm(prompt):
        return json.dumps({
            "narrative": "A renewable microgrid proposal requires cross-disciplinary collaboration.",
            "choices": [
                {
                    "text": "Form a microgrid consortium.",
                    "impact": {
                        "node_id": "Microgrid_Consortium",
                        "resource_change": 2.0,
                        "trust_change": 0.5,
                        "edge_weight_change": 0.2
                    }
                },
                {
                    "text": "Run a hackathon.",
                    "impact": {
                        "node_id": "Microgrid_Hackathon_Team",
                        "resource_change": 1.2,
                        "trust_change": 0.35,
                        "edge_weight_change": 0.15
                    }
                },
                {
                    "text": "Create an advocacy group.",
                    "impact": {
                        "node_id": "Microgrid_Advocacy_Group",
                        "resource_change": 1.0,
                        "trust_change": 0.4,
                        "edge_weight_change": 0.13
                    }
                }
            ]
        })

    crisis_state = {"type": "Microgrid", "severity": 1.0, "turn": 0}

    log = run_crisis_loop(G, fake_llm, crisis_state, num_turns=3)
    print(json.dumps(log, indent=2))
