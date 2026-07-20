import networkx as nx

NEGOTIATION_TRUST_THRESHOLD = 0.3

def route_resources(G, source, via, target, amount):
    """
    Simulate decentralized resource routing from source -> via -> target.
    If trust at 'via' is low, trigger a negotiation event.
    """

    # Ensure nodes exist
    if source not in G.nodes or via not in G.nodes or target not in G.nodes:
        raise ValueError("One or more nodes do not exist in the graph.")

    # Check trust level at the intermediary node
    trust_level = G.nodes[via].get("trust", 0.0)

    # Trigger negotiation if trust is low
    if trust_level < NEGOTIATION_TRUST_THRESHOLD:
        return negotiation_event(G, source, via, target, trust_level)

    # Otherwise, perform normal routing
    return perform_routing(G, source, via, target, amount)


def perform_routing(G, source, via, target, amount):
    """
    Normal resource routing without negotiation.
    """

    # Deduct from source
    G.nodes[source]["Resource_Capacity"] -= amount

    # Intermediary node B may take a small routing fee
    routing_fee = amount * 0.05
    G.nodes[via]["Resource_Capacity"] += routing_fee

    # Deliver to target
    G.nodes[target]["Resource_Capacity"] += (amount - routing_fee)

    return {
        "event": "routing_success",
        "source": source,
        "via": via,
        "target": target,
        "delivered": amount - routing_fee,
        "fee": routing_fee
    }


def negotiation_event(G, source, via, target, trust_level):
    """
    Trigger a text-based negotiation event when trust at Node B is too low.
    """

    narrative = (
        f"Resource routing from {source} to {target} must pass through {via}, "
        f"but trust at {via} is critically low ({trust_level:.2f}). "
        "A negotiation is required to secure passage. "
        "The intermediary demands assurances before allowing the transfer."
    )

    choices = [
        {
            "text": "Offer additional resources to build goodwill.",
            "impact": {
                "node_id": via,
                "resource_change": +2.0,
                "trust_change": +0.15,
                "edge_weight_change": +0.05
            }
        },
        {
            "text": "Promise future collaboration and shared intelligence.",
            "impact": {
                "node_id": via,
                "resource_change": 0.0,
                "trust_change": +0.25,
                "edge_weight_change": +0.02
            }
        },
        {
            "text": "Apply pressure and demand compliance.",
            "impact": {
                "node_id": via,
                "resource_change": -1.0,
                "trust_change": -0.20,
                "edge_weight_change": -0.10
            }
        }
    ]

    return {
        "event": "negotiation_required",
        "narrative": narrative,
        "choices": choices
    }


# -------------------------------
# Example Usage
# -------------------------------
if __name__ == "__main__":
    G = nx.DiGraph()

    # Example nodes
    G.add_node("Node_A", Resource_Capacity=10, trust=0.8)
    G.add_node("Node_B", Resource_Capacity=5, trust=0.2)  # Low trust triggers negotiation
    G.add_node("Node_C", Resource_Capacity=3, trust=0.7)

    result = route_resources(G, "Node_A", "Node_B", "Node_C", amount=4)
    print(result)
