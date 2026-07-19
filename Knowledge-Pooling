def apply_knowledge_pooling(G, action):
    teams = action["teams_contributing"]
    assets = action["knowledge_assets"]
    impact = action["impact"]

    result = apply_base_impact(
        G,
        impact["node_id"],
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    for t in teams:
        G.nodes[t]["trust"] += 0.04

    result["assets"] = assets
    return result
