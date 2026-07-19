import networkx as nx

def apply_narrator_impacts(G, narrator_json):
    """
    Apply narrator-generated JSON impacts directly to the NetworkX Mesh graph.

    Expected JSON schema:
    {
      "narrative": "",
      "choices": [
        {
          "text": "",
          "impact": {
            "node_id": "",
            "resource_change": 0,
            "trust_change": 0,
            "edge_weight_change": 0
          }
        }
      ]
    }

    Returns a dict summarizing the applied changes.
    """

    results = []

    for choice in narrator_json["choices"]:
        impact = choice["impact"]

        node_id = impact["node_id"]
        resource_delta = impact["resource_change"]
        trust_delta = impact["trust_change"]
        edge_delta = impact["edge_weight_change"]

        if node_id not in G.nodes:
            raise ValueError(f"Node '{node_id}' does not exist in the graph.")

        # --- Apply resource change ---
        current_resources = G.nodes[node_id].get("Resource_Capacity", 0.0)
        G.nodes[node_id]["Resource_Capacity"] = current_resources + resource_delta

        # --- Apply trust change ---
        current_trust = G.nodes[node_id].get("trust", 0.0)
        G.nodes[node_id]["trust"] = current_trust + trust_delta

        # --- Apply edge weight changes ---
        # Here we apply the delta to ALL outgoing edges from the node.
        # You can customize this to target specific edges.
        updated_edges = []
        for _, target, attrs in G.out_edges(node_id, data=True):
            current_weight = attrs.get("influence_weight", 0.0)
            new_weight = current_weight + edge_delta
            G[node_id][target]["influence_weight"] = new_weight
            updated_edges.append((node_id, target, new_weight))

        # Collect results for logging or UI
        results.append({
            "node": node_id,
            "new_resource_capacity": G.nodes[node_id]["Resource_Capacity"],
            "new_trust": G.nodes[node_id]["trust"],
            "updated_edges": updated_edges
        })

    return {
        "event": "impacts_applied",
        "details": results
    }
