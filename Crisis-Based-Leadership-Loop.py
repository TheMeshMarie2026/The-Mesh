import networkx as nx

def update_leadership_weights(G, crisis_type, crisis_attribute_map):
    """
    Update leadership weights based on the current crisis type.
    
    Parameters:
        G: networkx graph
        crisis_type: str (e.g., 'Financial', 'Logistical')
        crisis_attribute_map: dict mapping crisis types to node attributes
            Example:
                {
                    'Financial': 'Financial_Acuity',
                    'Logistical': 'Logistics_Skill',
                    'Social': 'Influence_Index'
                }
    """

    # Determine which node attribute is relevant for this crisis
    relevant_attr = crisis_attribute_map[crisis_type]

    # Extract all attribute values
    attr_values = {
        node: G.nodes[node].get(relevant_attr, 0.0)
        for node in G.nodes()
    }

    # Avoid division by zero
    total = sum(attr_values.values()) or 1.0

    # Apply the mathematical formula
    for node, value in attr_values.items():
        new_weight = value / total
        G.nodes[node]['Leadership_Weight'] = new_weight


def crisis_game_loop(G, crisis_sequence, crisis_attribute_map):
    """
    Simulate a game loop where crisis types change dynamically.
    
    Parameters:
        G: networkx graph
        crisis_sequence: list of crisis types in order
        crisis_attribute_map: dict mapping crisis types to node attributes
    """

    for crisis in crisis_sequence:
        print(f"\n=== Crisis Shift: {crisis} ===")

        # Update leadership weights
        update_leadership_weights(G, crisis, crisis_attribute_map)

        # Print updated leadership distribution
        for node, attrs in G.nodes(data=True):
            print(f"{node}: Leadership_Weight={attrs['Leadership_Weight']:.3f}")


# -------------------------------
# Example Usage
# -------------------------------
if __name__ == "__main__":
    # Create heterarchical graph
    G = nx.DiGraph()

    # Add nodes with crisis-relevant attributes
    G.add_node("Corp_A", Logistics_Skill=0.9, Financial_Acuity=0.3, Influence_Index=0.5)
    G.add_node("Corp_B", Logistics_Skill=0.4, Financial_Acuity=0.8, Influence_Index=0.6)
    G.add_node("Student_1", Logistics_Skill=0.7, Financial_Acuity=0.2, Influence_Index=0.9)
    G.add_node("Student_2", Logistics_Skill=0.2, Financial_Acuity=0.5, Influence_Index=0.4)

    # Crisis → attribute mapping
    crisis_attribute_map = {
        'Financial': 'Financial_Acuity',
        'Logistical': 'Logistics_Skill',
        'Social': 'Influence_Index'
    }

    # Crisis timeline
    crisis_sequence = ['Financial', 'Logistical', 'Social']

    # Run the game loop
    crisis_game_loop(G, crisis_sequence, crisis_attribute_map)
