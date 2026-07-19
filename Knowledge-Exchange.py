def apply_knowledge_exchange(G, action):
    nodes = action["nodes_involved"]
    domains = action["knowledge_domains"]
    impact = action["impact"]

    result = apply_base_impact(
        G,
        impact["node_id"],
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    # Knowledge exchange increases mutual trust
    for n1 in nodes:
        for n2 in nodes:
            if n1 != n2 and G.has_edge(n1, n2):
                G[n1][n2]["influence_weight"] += 0.03

    result["domains_shared"] = domains
    return result
