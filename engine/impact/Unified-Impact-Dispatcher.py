# ---------------------------------------------------------
# UNIFIED IMPACT DISPATCHER
# ---------------------------------------------------------

IMPACT_HANDLERS = {
    "coalition_formation": apply_coalition_formation,
    "knowledge_exchange": apply_knowledge_exchange,

    "resource_pooling": apply_resource_pooling,
    "resource_bidding": apply_resource_bidding,

    "trust_pledge": apply_trust_pledge,
    "reputation_broadcast": apply_reputation_broadcast,

    "emergency_protocol": apply_emergency_protocol,
    "referendum": apply_referendum,

    "network_scan": apply_network_scan,
    "intelligence_sprint": apply_intelligence_sprint,

    "mediation": apply_mediation,
    "arbitration": apply_arbitration,

    "carbon_rebalance": apply_carbon_rebalance,
    "ethical_sourcing_audit": apply_ethical_sourcing_audit,

    "patch_deployment": apply_patch_deployment,
    "protocol_rewrite": apply_protocol_rewrite,

    "crisis_forecast": apply_crisis_forecast,
    "node_merge": apply_node_merge,

    "team_negotiation": apply_team_negotiation,
    "knowledge_pooling": apply_knowledge_pooling
}


def dispatch_action(G, action_json):
    """
    Unified dispatcher that selects the correct impact model
    based on action_type and applies it to the graph.

    action_json schema:
    {
      "action_type": "",
      "description": "",
      ... (category-specific fields)
      "impact": {
        "node_id": "",
        "resource_change": 0,
        "trust_change": 0,
        "edge_weight_change": 0
      }
    }
    """

    action_type = action_json.get("action_type")

    if action_type not in IMPACT_HANDLERS:
        raise ValueError(f"Unknown action_type '{action_type}'")

    handler = IMPACT_HANDLERS[action_type]
    return handler(G, action_json)
