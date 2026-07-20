def apply_resource_bidding(G, action):
    bidders = action["bidders"]
    resource_type = action["resource_type"]
    impact = action["impact"]

    result = apply_base_impact(
        G,
        impact["node_id"],
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    # Higher trust bidders get bonus influence
    for b in bidders:
        trust = G.nodes[b].get("trust", 0.0)
        if trust > 0.7:
            for _, tgt in G.out_edges(b):
                G[b][tgt]["influence_weight"] += 0.05

    result["resource_type"] = resource_type
    return result
