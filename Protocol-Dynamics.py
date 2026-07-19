def apply_protocol_rewrite(G, action):
    contributors = action["contributors"]
    version = action["protocol_version"]
    impact = action["impact"]

    result = apply_base_impact(
        G,
        impact["node_id"],
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    for c in contributors:
        for _, tgt in G.out_edges(c):
            G[c][tgt]["influence_weight"] += 0.08

    result["protocol_version"] = version
    return result
