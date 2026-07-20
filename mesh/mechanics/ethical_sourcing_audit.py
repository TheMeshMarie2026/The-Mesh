def apply_ethical_sourcing_audit(G, action):
    auditors = action["auditors"]
    suppliers = action["supplier_nodes"]
    impact = action["impact"]

    result = apply_base_impact(
        G,
        impact["node_id"],
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    for s in suppliers:
        G.nodes[s]["trust"] += 0.05

    result["suppliers"] = suppliers
    return result
