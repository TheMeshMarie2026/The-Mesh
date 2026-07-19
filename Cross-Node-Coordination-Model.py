def apply_coalition_formation(G, action):
    members = action["members"]
    impact = action["impact"]

    # Apply base impact to the initiating node
    result = apply_base_impact(
        G,
        impact["node_id"],
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    # Coalition trust boost between members
    for m1 in members:
        for m2 in members:
            if m1 != m2 and G.has_edge(m1, m2):
                G[m1][m2]["influence_weight"] += 0.05

    result["coalition_members"] = members
    return result
