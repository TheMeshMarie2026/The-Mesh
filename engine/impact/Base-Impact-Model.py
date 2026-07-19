def apply_base_impact(G, node_id, resource_delta, trust_delta, edge_delta):
    if node_id not in G.nodes:
        raise ValueError(f"Node '{node_id}' not found in graph.")

    # Node-level updates
    G.nodes[node_id]["Resource_Capacity"] = G.nodes[node_id].get("Resource_Capacity", 0.0) + resource_delta
    G.nodes[node_id]["trust"] = G.nodes[node_id].get("trust", 0.0) + trust_delta

    # Edge-level updates (outgoing)
    updated_edges = []
    for _, tgt, attrs in G.out_edges(node_id, data=True):
        new_w = attrs.get("influence_weight", 0.0) + edge_delta
        G[node_id][tgt]["influence_weight"] = new_w
        updated_edges.append((node_id, tgt, new_w))

    return {
        "node": node_id,
        "new_resource_capacity": G.nodes[node_id]["Resource_Capacity"],
        "new_trust": G.nodes[node_id]["trust"],
        "updated_edges": updated_edges
    }
