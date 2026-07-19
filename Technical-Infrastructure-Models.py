def apply_patch_deployment(G, action):
    devs = action["dev_nodes"]
    patch_id = action["patch_id"]
    impact = action["impact"]

    result = apply_base_impact(
        G,
        impact["node_id"],
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    for d in devs:
        G.nodes[d]["trust"] += 0.04

    result["patch_id"] = patch_id
    return result
