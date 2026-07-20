def apply_intelligence_sprint(G, action):
    contributors = action["contributors"]
    domains = action["data_domains"]
    impact = action["impact"]

    result = apply_base_impact(
        G,
        impact["node_id"],
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    for c in contributors:
        G.nodes[c]["trust"] += 0.03

    result["domains"] = domains
    return result
