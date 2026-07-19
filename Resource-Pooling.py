def apply_resource_pooling(G, action):
    contributors = action["contributors"]
    pool_id = action["pool_id"]
    impact = action["impact"]

    # Apply base impact to pool node
    result = apply_base_impact(
        G,
        pool_id,
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    # Contributors lose small resource amounts
    for c in contributors:
        G.nodes[c]["Resource_Capacity"] -= 0.5

    result["contributors"] = contributors
    return result
