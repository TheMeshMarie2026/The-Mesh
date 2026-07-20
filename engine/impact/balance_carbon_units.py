def apply_carbon_rebalance(G, action):
    nodes = action["nodes_involved"]
    units = action["carbon_units"]
    impact = action["impact"]

    result = apply_base_impact(
        G,
        impact["node_id"],
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    for n in nodes:
        G.nodes[n]["Resource_Capacity"] += units * 0.1

    result["carbon_units"] = units
    return result
