def apply_node_merge(G, action):
    n1, n2 = action["nodes_merged"]
    new_id = action["new_node_id"]
    impact = action["impact"]

    # Create new merged node
    G.add_node(new_id)
    G.nodes[new_id]["Resource_Capacity"] = (
        G.nodes[n1].get("Resource_Capacity", 0) +
        G.nodes[n2].get("Resource_Capacity", 0)
    )
    G.nodes[new_id]["trust"] = (
        G.nodes[n1].get("trust", 0) +
        G.nodes[n2].get("trust", 0)
    ) / 2

    # Apply base impact to merged node
    result = apply_base_impact(
        G,
        new_id,
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    result["merged_from"] = [n1, n2]
    return result
