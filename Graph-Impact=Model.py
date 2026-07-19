import networkx as nx
from typing import Dict, Any, List


def apply_choice_impact(
    G: nx.DiGraph,
    impact: Dict[str, Any],
    edge_scope: str = "outgoing"
) -> Dict[str, Any]:
    """
    Apply a single choice impact to the Mesh graph.

    impact schema:
    {
      "node_id": "Some_Node",
      "resource_change": float,
      "trust_change": float,
      "edge_weight_change": float
    }

    edge_scope:
      - "outgoing": apply to all edges from node_id
      - "incoming": apply to all edges to node_id
      - "both": apply to both directions
    """

    node_id = impact["node_id"]
    resource_delta = impact["resource_change"]
    trust_delta = impact["trust_change"]
    edge_delta = impact["edge_weight_change"]

    if node_id not in G.nodes:
        raise ValueError(f"Node '{node_id}' not found in graph.")

    # --- Node-level updates ---
    current_resources = G.nodes[node_id].get("Resource_Capacity", 0.0)
    current_trust = G.nodes[node_id].get("trust", 0.0)

    G.nodes[node_id]["Resource_Capacity"] = current_resources + resource_delta
    G.nodes[node_id]["trust"] = current_trust + trust_delta

    # --- Edge-level updates ---
    updated_edges: List[Any] = []

    if edge_scope in ("outgoing", "both"):
        for _, tgt, attrs in G.out_edges(node_id, data=True):
            w = attrs.get("influence_weight", 0.0)
            new_w = w + edge_delta
            G[node_id][tgt]["influence_weight"] = new_w
            updated_edges.append((node_id, tgt, new_w))

    if edge_scope in ("incoming", "both"):
        for src, _, attrs in G.in_edges(node_id, data=True):
            w = attrs.get("influence_weight", 0.0)
            new_w = w + edge_delta
            G[src][node_id]["influence_weight"] = new_w
            updated_edges.append((src, node_id, new_w))

    return {
        "node": node_id,
        "new_resource_capacity": G.nodes[node_id]["Resource_Capacity"],
        "new_trust": G.nodes[node_id]["trust"],
        "updated_edges": updated_edges
    }


def apply_scenario_choice(
    G: nx.DiGraph,
    scenario: Dict[str, Any],
    choice_index: int,
    edge_scope: str = "outgoing"
) -> Dict[str, Any]:
    """
    Apply a selected choice from a scenario JSON to the graph.

    scenario schema:
    {
      "narrative": "...",
      "choices": [
        {
          "text": "...",
          "impact": { ... }
        },
        ...
      ]
    }
    """

    choices = scenario["choices"]
    if not (0 <= choice_index < len(choices)):
        raise ValueError("Invalid choice index.")

    choice = choices[choice_index]
    impact = choice["impact"]

    impact_result = apply_choice_impact(G, impact, edge_scope=edge_scope)

    return {
        "narrative": scenario["narrative"],
        "selected_choice": choice,
        "impact_result": impact_result
    }


# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    G = nx.DiGraph()

    # Example nodes for a university scenario
    G.add_node("Lab_Council", Resource_Capacity=5.0, trust=0.6)
    G.add_node("Scheduling_Collective", Resource_Capacity=3.0, trust=0.5)
    G.add_edge("Lab_Council", "Scheduling_Collective", influence_weight=0.2)

    scenario = {
        "narrative": "Shared labs are overloaded; students must collaborate to redesign access.",
        "choices": [
            {
                "text": "Form a cross-disciplinary lab council.",
                "impact": {
                    "node_id": "Lab_Council",
                    "resource_change": 2.0,
                    "trust_change": 0.35,
                    "edge_weight_change": 0.15
                }
            },
            {
                "text": "Create a pooled booking system.",
                "impact": {
                    "node_id": "Scheduling_Collective",
                    "resource_change": 1.5,
                    "trust_change": 0.30,
                    "edge_weight_change": 0.12
                }
            }
        ]
    }

    result = apply_scenario_choice(G, scenario, choice_index=0)
    print(result)
