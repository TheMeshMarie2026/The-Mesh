import networkx as nx
import random
from typing import Dict, Any, List

class HeterarchyEngine:
    def __init__(self):
        # Initialize an empty directed graph to map connections and fluid weights
        self.network = nx.DiGraph()
        
    def create_node(self, node_id: str, archetype: str, knowledge: float, resources: float) -> None:
        """Adds a node (Community, Corporate Entity, University Lab) to the system."""
        self.network.add_node(
            node_id,
            archetype=archetype,
            knowledge=max(0.0, min(1.0, knowledge)),     # Expertise scale: 0.0 to 1.0
            resources=max(0.0, resources),                # Raw materials / funds
            leadership_weight=0.0,                        # Fluid authority score
            is_active_leader=False
        )

    def establish_p2p_channel(self, node_a: str, node_b: str, trust_weight: float) -> None:
        """Creates a bidirectional communication/resource channel with a trust factor."""
        # Channels are bidirectional but modeled as two directed edges for complex asymmetric routing later
        self.network.add_edge(node_a, node_b, trust=max(0.0, min(1.0, trust_weight)))
        self.network.add_edge(node_b, node_a, trust=max(0.0, min(1.0, trust_weight)))

    def shift_leadership_weights(self, crisis_type: str, crisis_demands: Dict[str, float]) -> Dict[str, Any]:
        """
        Core Heterarchical Algorithm: Calculates which node naturally commands 
        the network based on crisis demands and network connectivity.
        
        Formula: 
        Score = (Node Knowledge * Crisis Weight) + Log(Resources + 1) + Network Centrality
        """
        # 1. Calculate Network Centrality (How well connected is this node to the heterarchy?)
        # Degree centrality measures how many direct P2P connections a node has.
        centrality = nx.degree_centrality(self.network)
        
        highest_score = -1.0
        current_leader = None
        all_scores = {}

        # 2. Evaluate every node's situational fitness
        for node_id, data in self.network.nodes(data=True):
            # Calculate knowledge alignment with the specific crisis type
            knowledge_match = data['knowledge'] * crisis_demands.get(crisis_type, 0.5)
            
            # Resources offer diminishing returns to scale, modeled via a logarithmic function
            import math
            resource_factor = math.log1p(data['resources']) * 0.1 
            
            # Centrality acts as a multiplier for effective coordination speed
            network_factor = centrality[node_id] * 0.3
            
            # Total emergent score
            fitness_score = knowledge_match + resource_factor + network_factor
            
            # Store calculated metrics back into the node state
            self.network.nodes[node_id]['leadership_weight'] = round(fitness_score, 3)
            self.network.nodes[node_id]['is_active_leader'] = False
            
            all_scores[node_id] = round(fitness_score, 3)
            
            # Elect the emergent leader dynamically
            if fitness_score > highest_score:
                highest_score = fitness_score
                current_leader = node_id

        # Set active flag on the winning node
        if current_leader:
            self.network.nodes[current_leader]['is_active_leader'] = True

        return {
            "crisis_processed": crisis_type,
            "emergent_leader": current_leader,
            "all_node_fitness": all_scores
        }

    def get_network_state(self) -> List[Dict[str, Any]]:
        """Utility function to view the complete mathematical state of the system."""
        state = []
        for node, data in self.network.nodes(data=True):
            state.append({"node": node, **data})
        return state


# =====================================================================
# SIMULATION / DEMONSTRATION RUN
# =====================================================================
if __name__ == "__main__":
    # 1. Initialize our Python engine
    game_engine = HeterarchyEngine()

    # 2. Seed the network with mixed corporate and university tester nodes
    # Parameters: Node ID, Archetype, Knowledge Level (0-1), Starting Resources
    game_engine.create_node("MIT_Lab", "University", knowledge=0.95, resources=10.0)
    game_engine.create_node("Logistics_Corp", "Corporate", knowledge=0.40, resources=95.0)
    game_engine.create_node("NGO_Local", "Community", knowledge=0.70, resources=5.0)

    # 3. Establish Peer-to-Peer channels (Trust scales from 0.0 to 1.0)
    game_engine.establish_p2p_channel("MIT_Lab", "Logistics_Corp", trust_weight=0.8)
    game_engine.establish_p2p_channel("Logistics_Corp", "NGO_Local", trust_weight=0.9)
    game_engine.establish_p2p_channel("NGO_Local", "MIT_Lab", trust_weight=0.5)

    print("--- Initial Network Configured ---")
    
    # 4. Trigger Crisis 1: A Pandemic (Demands pure scientific knowledge)
    print("\n[CRISIS 1]: Global Pathogen Outbreak detected.")
    pandemic_demands = {"Medical_Science": 0.9, "Supply_Chain": 0.2}
    result_1 = game_engine.shift_leadership_weights("Medical_Science", pandemic_demands)
    print(f"Emergent Network Leader: {result_1['emergent_leader']}")
    print(f"Full Fitness Scores: {result_1['all_node_fitness']}")

    # 5. Trigger Crisis 2: Supply Chain Freeze (Demands execution infrastructure and scale)
    print("\n[CRISIS 2]: Global shipping lanes blocked.")
    supply_demands = {"Medical_Science": 0.1, "Supply_Chain": 0.95}
    result_2 = game_engine.shift_leadership_weights("Supply_Chain", supply_demands)
    print(f"Emergent Network Leader: {result_2['emergent_leader']}")
    print(f"Full Fitness Scores: {result_2['all_node_fitness']}")
