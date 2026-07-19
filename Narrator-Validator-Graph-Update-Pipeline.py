import json
import networkx as nx

# ---------- Validator ----------

class NarratorJSONValidationError(Exception):
    pass


def validate_narrator_json(json_obj):
    if not isinstance(json_obj, dict):
        raise NarratorJSONValidationError("Top-level JSON must be an object.")

    required_top_keys = {"narrative", "choices"}
    missing = required_top_keys - json_obj.keys()
    if missing:
        raise NarratorJSONValidationError(f"Missing keys: {missing}")

    if not isinstance(json_obj["narrative"], str):
        raise NarratorJSONValidationError("'narrative' must be a string.")

    choices = json_obj["choices"]
    if not isinstance(choices, list) or len(choices) == 0:
        raise NarratorJSONValidationError("'choices' must be a non-empty list.")

    for idx, choice in enumerate(choices):
        if not isinstance(choice, dict):
            raise NarratorJSONValidationError(f"Choice {idx} must be an object.")
        if "text" not in choice or "impact" not in choice:
            raise NarratorJSONValidationError(f"Choice {idx} missing 'text' or 'impact'.")
        if not isinstance(choice["text"], str):
            raise NarratorJSONValidationError(f"Choice {idx} 'text' must be a string.")
        impact = choice["impact"]
        if not isinstance(impact, dict):
            raise NarratorJSONValidationError(f"Choice {idx} 'impact' must be an object.")
        required_impact = {"node_id", "resource_change", "trust_change", "edge_weight_change"}
        missing_imp = required_impact - impact.keys()
        if missing_imp:
            raise NarratorJSONValidationError(f"Choice {idx} impact missing: {missing_imp}")
        if not isinstance(impact["node_id"], str):
            raise NarratorJSONValidationError(f"Choice {idx} 'node_id' must be a string.")
        for field in ["resource_change", "trust_change", "edge_weight_change"]:
            if not isinstance(impact[field], (int, float)):
                raise NarratorJSONValidationError(f"Choice {idx} '{field}' must be numeric.")

    return True


# ---------- Graph update ----------

def apply_choice_impact(G: nx.DiGraph, impact: dict) -> dict:
    node_id = impact["node_id"]
    if node_id not in G.nodes:
        raise ValueError(f"Node '{node_id}' not found in graph.")

    r_delta = impact["resource_change"]
    t_delta = impact["trust_change"]
    e_delta = impact["edge_weight_change"]

    current_r = G.nodes[node_id].get("Resource_Capacity", 0.0)
    current_t = G.nodes[node_id].get("trust", 0.0)

    G.nodes[node_id]["Resource_Capacity"] = current_r + r_delta
    G.nodes[node_id]["trust"] = current_t + t_delta

    updated_edges = []
    for _, tgt, attrs in G.out_edges(node_id, data=True):
        w = attrs.get("influence_weight", 0.0)
        new_w = w + e_delta
        G[node_id][tgt]["influence_weight"] = new_w
        updated_edges.append((node_id, tgt, new_w))

    return {
        "node": node_id,
        "new_resource_capacity": G.nodes[node_id]["Resource_Capacity"],
        "new_trust": G.nodes[node_id]["trust"],
        "updated_edges": updated_edges
    }


def apply_selected_choice(G: nx.DiGraph, narrator_json: dict, choice_index: int) -> dict:
    choices = narrator_json["choices"]
    if not (0 <= choice_index < len(choices)):
        raise ValueError("Invalid choice index.")

    choice = choices[choice_index]
    impact_result = apply_choice_impact(G, choice["impact"])

    return {
        "narrative": narrator_json["narrative"],
        "selected_choice": choice,
        "impact_result": impact_result
    }


# ---------- Narrator stub (replace with real LLM) ----------

def fake_llm(prompt: str) -> str:
    return json.dumps({
        "narrative": "A campus microgrid proposal needs cross-disciplinary collaboration to succeed.",
        "choices": [
            {
                "text": "Form a microgrid consortium of engineers, climate scientists, and business students.",
                "impact": {
                    "node_id": "Microgrid_Consortium",
                    "resource_change": 2.0,
                    "trust_change": 0.5,
                    "edge_weight_change": 0.2
                }
            },
            {
                "text": "Run a hackathon to prototype microgrid designs.",
                "impact": {
                    "node_id": "Microgrid_Hackathon_Team",
                    "resource_change": 1.2,
                    "trust_change": 0.35,
                    "edge_weight_change": 0.15
                }
            },
            {
                "text": "Create an advocacy group to pitch the microgrid to facilities.",
                "impact": {
                    "node_id": "Microgrid_Advocacy_Group",
                    "resource_change": 1.0,
                    "trust_change": 0.4,
                    "edge_weight_change": 0.13
                }
            }
        ]
    })


# ---------- Pipeline ----------

def run_narrator_pipeline(G: nx.DiGraph, prompt: str, choice_index: int) -> dict:
    raw = fake_llm(prompt)  # replace with real LLM call
    data = json.loads(raw)

    validate_narrator_json(data)
    result = apply_selected_choice(G, data, choice_index)

    return result


# ---------- Example ----------

if __name__ == "__main__":
    G = nx.DiGraph()
    G.add_node("Microgrid_Consortium", Resource_Capacity=5.0, trust=0.6)
    G.add_node("Microgrid_Hackathon_Team", Resource_Capacity=3.0, trust=0.5)
    G.add_node("Microgrid_Advocacy_Group", Resource_Capacity=2.0, trust=0.4)
    G.add_edge("Microgrid_Consortium", "Microgrid_Hackathon_Team", influence_weight=0.1)

    result = run_narrator_pipeline(G, "Generate a microgrid crisis event.", choice_index=0)
    print(json.dumps(result, indent=2))
