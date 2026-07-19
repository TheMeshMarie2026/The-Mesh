def apply_reputation_broadcast(G, action):
    origin = action["origin_node"]
    audience = action["audience_nodes"]
    impact = action["impact"]

    result = apply_base_impact(
        G,
        origin,
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    for a in audience:
        if G.has_edge(origin, a):
            G[origin][a]["influence_weight"] += 0.1

    result["audience"] = audience
    return result
