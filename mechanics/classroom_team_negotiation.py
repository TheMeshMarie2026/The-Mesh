def apply_team_negotiation(G, action):
    teams = action["teams_involved"]
    topic = action["negotiation_topic"]
    impact = action["impact"]

    result = apply_base_impact(
        G,
        impact["node_id"],
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    for t in teams:
        G.nodes[t]["trust"] += 0.03

    result["topic"] = topic
    return result
