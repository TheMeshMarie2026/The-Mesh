def apply_referendum(G, action):
    voters = action["voting_nodes"]
    options = action["options"]
    impact = action["impact"]

    result = apply_base_impact(
        G,
        impact["node_id"],
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    # Voters gain small trust boosts
    for v in voters:
        G.nodes[v]["trust"] += 0.05

    result["options"] = options
    return result
