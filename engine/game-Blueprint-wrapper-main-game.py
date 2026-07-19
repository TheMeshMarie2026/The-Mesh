import numpy as np

class HeterarchyNode:
    def __init__(self, node_id: str, capabilities: dict, coordinates: tuple):
        """
        In a heterarchy, nodes have no static rank. They only have attributes.
        capabilities: dict of asset types and their values (e.g., {"medical": 0.8, "water": 0.2})
        coordinates: (x, y) grid location representing physical or systemic distance
        """
        self.node_id = node_id
        self.capabilities = capabilities
        self.coordinates = coordinates
        
    def calculate_priority_score(self, crisis_context: dict) -> float:
        """
        Calculates the node's power/priority for the current situation dynamically.
        Power emerges mathematically from the alignment of attributes to context.
        """
        # 1. Map node skills to current crisis demands
        node_vector = np.array([self.capabilities.get(k, 0.0) for k in crisis_context["demands"].keys()])
        crisis_vector = np.array(list(crisis_context["demands"].values()))
        
        # Avoid division by zero if vectors are empty
        if len(crisis_vector) == 0:
            return 0.0
            
        # 2. Contextual Fit: High dot product means this node has exactly what the network needs right now
        capability_fit = np.dot(node_vector, crisis_vector)
        
        # 3. Distance Penalty: Nodes closer to the epicentre react faster
        dx = self.coordinates[0] - crisis_context["location"][0]
        dy = self.coordinates[1] - crisis_context["location"][1]
        distance = np.sqrt(dx**2 + dy**2) or 1.0  # Prevent division by zero
        
        # 4. Final Shifting Priority Score
        priority_score = capability_fit / distance
        return round(priority_score, 2)

class HeterarchicalNetwork:
    def __init__(self):
        self.nodes = []
        
    def add_node(self, node: HeterarchyNode):
        self.nodes.append(node)
        
    def resolve_turn_leadership(self, active_crisis: dict) -> list:
        """
        The central dynamic of heterarchy: The network self-organizes every turn.
        The temporary 'Lead Node' is chosen purely by current utility score.
        """
        leaderboard = []
        for node in self.nodes:
            score = node.calculate_priority_score(active_crisis)
            leaderboard.append({"node_id": node.node_id, "priority_score": score})
            
        # Sort network from highest contextual power to lowest
        leaderboard.sort(key=lambda x: x["priority_score"], reverse=True)
        return leaderboard

# ==========================================
# SIMULATION DEMO (How gameplay shifts power)
# ==========================================
if __name__ == "__main__":
    # Create the horizontal players (Human & AI nodes mixed)
    network = HeterarchicalNetwork()
    network.add_node(HeterarchyNode("AI_Medic_Agent", {"medical": 0.9, "logistics": 0.2}, (2, 2)))
    network.add_node(HeterarchyNode("Human_Player_1", {"water": 0.8, "medical": 0.1}, (10, 10)))
    network.add_node(HeterarchyNode("AI_Logistics_Bot", {"logistics": 0.9, "water": 0.5}, (5, 5)))

    # --- TURN 1: A Severe Fire Breaks Out near Human Player 1 ---
    turn_1_crisis = {
        "name": "Industrial Forest Fire",
        "demands": {"water": 0.9, "logistics": 0.4, "medical": 0.1},
        "location": (9, 9)
    }
    
    print("--- TURN 1: FOREST FIRE AT (9,9) ---")
    rankings_t1 = network.resolve_turn_leadership(turn_1_crisis)
    for rank, item in enumerate(rankings_t1, 1):
        print(f"Rank {rank}: {item['node_id']} | Power Score: {item['priority_score']}")
    # OUTPUT: Human_Player_1 leads because they have water and are physically closest.

    print("\n" + "="*40 + "\n")

    # --- TURN 2: The Fire is out, but a Toxic Gas Leak poisons an urban sector near the Medic ---
    turn_2_crisis = {
        "name": "Chemical Gas Leak",
        "demands": {"medical": 0.9, "logistics": 0.2, "water": 0.0},
        "location": (3, 2)
    }
    
    print("--- TURN 2: TOXIC LEAK AT (3,2) ---")
    rankings_t2 = network.resolve_turn_leadership(turn_2_crisis)
    for rank, item in enumerate(rankings_t2, 1):
        print(f"Rank {rank}: {item['node_id']} | Power Score: {item['priority_score']}")
    # OUTPUT: AI_Medic_Agent instantly usurps power because human attributes are useless here.
