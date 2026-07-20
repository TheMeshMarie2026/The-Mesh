def apply_crisis_forecast(G, action):
    forecasters = action["forecasting_nodes"]
    horizon = action["forecast_horizon"]
    impact = action["impact"]

    result = apply_base_impact(
        G,
        impact["node_id"],
        impact["resource_change"],
        impact["trust_change"],
        impact["edge_weight_change"]
    )

    for f in forecasters:
        G.nodes[f]["trust"] += 0.02

    result["forecast_horizon"] = horizon
    return result
