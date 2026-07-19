def apply_mediation(G, action):
    mediator = action["mediator"]
    parties = action["conflicting_nodes"]
    impact = action["impact"]

    result = apply_base_impact(
        G,
        mediator,
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    for p1 in parties:
        for p2 in parties:
            if p1 != p2 and G.has_edge(p1, p2):
                G[p1][p2]["influence_weight"] += 0.06

    result["parties"] = parties
    return result
