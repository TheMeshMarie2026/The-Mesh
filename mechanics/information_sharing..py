def apply_network_scan(G, action):
    scanner = action["scanning_node"]
    targets = action["scan_targets"]
    impact = action["impact"]

    result = apply_base_impact(
        G,
        scanner,
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    # Scanning increases influence over targets
    for t in targets:
        if G.has_edge(scanner, t):
            G[scanner][t]["influence_weight"] += 0.07

    result["targets"] = targets
    return result
