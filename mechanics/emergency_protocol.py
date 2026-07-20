def apply_emergency_protocol(G, action):
    authors = action["authors"]
    protocol_id = action["protocol_id"]
    impact = action["impact"]

    result = apply_base_impact(
        G,
        impact["node_id"],
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    # Authors gain influence
    for a in authors:
        for _, tgt in G.out_edges(a):
            G[a][tgt]["influence_weight"] += 0.05

    result["protocol_id"] = protocol_id
    return result
