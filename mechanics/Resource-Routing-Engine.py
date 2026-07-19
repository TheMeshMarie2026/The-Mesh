import networkx as nx
import random
import math
from typing import Dict, Any, List, Optional

class HeterarchyEngine:
    def __init__(self):
        self.network = nx.DiGraph()
        
    def create_node(self, node_id: str, archetype: str, knowledge: float, resources: float) -> None:
        """Adds a node to the system."""
        self.network.add_node(
            node_id,
            archetype=archetype,
            knowledge=max(0.0, min(1.0, knowledge)),
            resources=max(0.0, resources),
            leadership_weight=0.0,
            is_active_leader=False
        )

    def establish_p2p_channel(self, node_a: str, node_b: str, trust_weight: float) -> None:
        """Creates a bidirectional channel. Edge weight is inversely proportional to trust for pathfinding."""
        trust = max(0.01, min(1.0, trust_weight)) # Prevent divide by zero
        # NetworkX shortest_path uses weights as costs; high trust must equal low cost
        routing_cost = round(1.0 / trust, 3)
        
        self.network.add_edge(node_a, node_b, trust=trust, cost=routing_cost)
        self.network.add_edge(node_b, node_a, trust=trust, cost=routing_cost)

    def shift_leadership_weights(self, crisis_type: str, crisis_demands: Dict[str, float]) -> Dict[str, Any]:
        """Calculates dynamic leadership weights based on crisis requirements."""
        centrality = nx.degree_centrality(self.network)
        highest_score = -1.0
        current_leader = None
        all_scores = {}

        for node_id, data in self.network.nodes(data=True):
            knowledge_match = data['knowledge'] * crisis_demands.get(crisis_type, 0.5)
            resource_factor = math.log1p(data['resources']) * 0.1 
            network_factor = centrality[node_id] * 0.3
            
            fitness_score = knowledge_match + resource_factor + network_factor
            self.network.nodes[node_id]['leadership_weight'] = round(fitness_score, 3)
            self.network.nodes[node_id]['is_active_leader'] = False
            all_scores[node_id] = round(fitness_score, 3)
            
            if fitness_score > highest_score:
                highest_score = fitness_score
                current_leader = node_id

        if current_leader:
            self.network.nodes[current_leader]['is_active_leader'] = True

        return {"crisis_processed": crisis_type, "emergent_leader": current_leader, "all_node_fitness": all_scores}

    # =====================================================================
    # NEW FEATURE: P2P RESOURCE ROUTING ENGINE WITH FRICTION
    # =====================================================================
    def route_resources(self, sender: str, receiver: str, amount: float) -> Dict[str, Any]:
        """
        Routes resources through the most trusted decentralized path.
        Friction is calculated using the collective lack of trust across the route.
        """
        if sender not in self.network or receiver not in self.network:
            return {"status": "FAILED", "reason": "Sender or Receiver node does not exist."}
            
        if self.network.nodes[sender]['resources'] < amount:
            return {"status": "FAILED", "reason": f"Insufficient resources. {sender} only has {self.network.nodes[sender]['resources']}."}

        try:
            # Find the path optimized for highest trust (lowest routing cost)
            path = nx.shortest_path(self.network, source=sender, target=receiver, weight='cost')
        except nx.NetworkXNoPath:
            return {"status": "FAILED", "reason": f"No active P2P channel pathways found between {sender} and {receiver}."}

        # Deduct initial capital from sender
        self.network.nodes[sender]['resources'] -= amount
        
        current_amount = amount
        path_friction_events = []
        rpg_trigger_node = None

        # Traverse the route to compute localized friction drops
        for i in range(len(path) - 1):
            current_node = path[i]
            next_node = path[i+1]
            
            edge_data = self.network.get_edge_data(current_node, next_node)
            trust_factor = edge_data['trust']
            
            # Friction penalty: Lower trust = higher loss of resources during transit
            loss_percentage = 1.0 - trust_factor
            loss_amount = current_amount * loss_percentage
            current_amount -= loss_amount
            
            path_friction_events.append({
                "segment": f"{current_node} -> {next_node}",
                "edge_trust": trust_factor,
                "loss": round(loss_amount, 2)
            })

            # CRITICAL TRIGGER FOR TEXT RPG: If trust falls below a threshold, trigger an intervention event
            if trust_factor < 0.65 and not rpg_trigger_node:
                rpg_trigger_node = next_node

        # Credit the remaining resources to the receiver
        self.network.nodes[receiver]['resources'] += round(current_amount, 2)

        return {
            "status": "SUCCESS",
            "optimal_path": path,
            "shipped_amount": amount,
            "received_amount": round(current_amount, 2),
            "total_friction_loss": round(amount - current_amount, 2),
            "segment_breakdown": path_friction_events,
            "trigger_rpg_event": rpg_trigger_node is not None,
            "rpg_bottleneck_node": rpg_trigger_node
        }


# =====================================================================
# SIMULATION RUN: ROUTING AND RPG EVENT TRIGGERS
# =====================================================================
if __name__ == "__main__":
    game_engine = HeterarchyEngine()

    # Create distinct nodes
    game_engine.create_node("MIT_Lab", "University", knowledge=0.9, resources=0.0)
    game_engine.create_node("Logistics_Corp", "Corporate", knowledge=0.5, resources=100.0)
    game_engine.create_node("Unstable_Middleman", "Middleman", knowledge=0.2, resources=10.0)
    game_engine.create_node("Refugee_Camp", "Community", knowledge=0.8, resources=0.0)

    # High-trust corporate-to-university line
    game_engine.establish_p2p_channel("Logistics_Corp", "MIT_Lab", trust_weight=0.95)
    # Low-trust channel leading down to local distribution nodes
    game_engine.establish_p2p_channel("Logistics_Corp", "Unstable_Middleman", trust_weight=0.50) # Danger point!
    game_engine.establish_p2p_channel("Unstable_Middleman", "Refugee_Camp", trust_weight=0.90)

    print("--- Heterarchical Network Mesh Active ---")
    
    # Executing a complex multi-hop route
    print("\n[COMMAND]: Logistics_Corp is routing 50.0 resources to Refugee_Camp via the network...")
    route_result = game_engine.route_resources("Logistics_Corp", "Refugee_Camp", amount=50.0)
    
    print(f"Status: {route_result['status']}")
    print(f"Calculated Path: { ' -> '.join(route_result['optimal_path']) }")
    print(f"Sent: {route_result['shipped_amount']} | Received: {route_result['received_amount']}")
    print(f"Friction Loss: {route_result['total_friction_loss']}")
    
    # Check if our Python logic caught the bottleneck to pass to our LLM text RPG phase
    if route_result['trigger_rpg_event']:
        print(f"\n⚠️  [GAME ENGINE ALERT]: RPG Event Triggered! Friction threshold crossed at node: '{route_result['rpg_bottleneck_node']}'.")
        print("-> Action Required: Pause engine loop and generate text dialogue negotiation prompt for the player.")
