def apply_arbitration(G, action):
    arbitrator = action["arbitrator"]
    parties = action["parties"]
    impact = action["impact"]

    result = apply_base_impact(
        G,
        arbitrator,
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    for p in parties:
        G.nodes[p]["trust"] += 0.04

    result["parties"] = parties
    return result
