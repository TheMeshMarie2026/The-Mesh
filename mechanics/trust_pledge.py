def apply_trust_pledge(G, action):
    pledgers = action["pledging_nodes"]
    impact = action["impact"]

    result = apply_base_impact(
        G,
        impact["node_id"],
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    # Pledgers gain trust with each other
    for p1 in pledgers:
        for p2 in pledgers:
            if p1 != p2 and G.has_edge(p1, p2):
                G[p1][p2]["influence_weight"] += 0.04

    result["pledgers"] = pledgers
    return result
