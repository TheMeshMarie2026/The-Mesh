import networkx as nx
import math
from typing import Dict, Any, List, Set, Optional

class HeterarchyEngine:
    def __init__(self):
        self.network = nx.DiGraph()
        # The Knowledge Commons: Shared public repository accessible by high-trust nodes
        self.knowledge_commons: Dict[str, float] = {} 
        
    def create_node(self, node_id: str, archetype: str, max_capacity: float) -> None:
        """Adds a node with structured knowledge domain profiles and physical inventory tracking."""
        self.network.add_node(
            node_id,
            archetype=archetype,
            # Specialized Knowledge Matrix (domain: mastery_level_0_to_1)
            knowledge_domains: Dict[str, float] = {},
            # Asset Inventory Ledger (item_type: current_quantity)
            inventory: Dict[str, float] = {},
            max_capacity=max_capacity,                     # Storage constraints for corporate vs grass-roots nodes
            leadership_weight=0.0,
            is_active_leader=False
        )

    def set_node_knowledge(self, node_id: str, domain: str, level: float) -> None:
        """Sets or updates a specific knowledge asset level inside a node."""
        if node_id in self.network:
            if 'knowledge_domains' not in self.network.nodes[node_id]:
                self.network.nodes[node_id]['knowledge_domains'] = {}
            self.network.nodes[node_id]['knowledge_domains'][domain] = max(0.0, min(1.0, level))

    def adjust_node_inventory(self, node_id: str, item_type: str, delta: float) -> bool:
        """Safely mutates physical warehouse assets while adhering to structural capacity caps."""
        node = self.network.nodes[node_id]
        if 'inventory' not in node:
            node['inventory'] = {}
            
        current_total_weight = sum(node['inventory'].values())
        current_item_qty = node['inventory'].get(item_type, 0.0)
        
        # Test bounds
        if current_item_qty + delta < 0:
            return False # Insufficient stock
        if current_total_weight + delta > node['max_capacity']:
            return False # Out of storage space (Forces players to share/route instead of hoard)
            
        node['inventory'][item_type] = round(current_item_qty + delta, 2)
        return True

    def establish_p2p_channel(self, node_a: str, node_b: str, trust_weight: float) -> None:
        """Creates a bidirectional network channel."""
        trust = max(0.01, min(1.0, trust_weight))
        routing_cost = round(1.0 / trust, 3)
        self.network.add_edge(node_a, node_b, trust=trust, cost=routing_cost)
        self.network.add_edge(node_b, node_a, trust=trust, cost=routing_cost)

    # =====================================================================
    # NEW FEATURE: KNOWLEDGE COMMONS & POOLING MECHANIC
    # =====================================================================
    def sync_to_knowledge_commons(self, node_id: str) -> Dict[str, Any]:
        """
        A node publishes its expertise to the global pool. 
        Network trust levels determine how accurately data translates without distortion.
        """
        node = self.network.nodes[node_id]
        # Calculate node's average outgoing channel trust
        outgoing_edges = self.network.out_edges(node_id, data=True)
        if not outgoing_edges:
            return {"status": "FAILED", "reason": f"{node_id} is isolated and cannot sync data."}
            
        avg_network_trust = sum([data['trust'] for _, _, data in outgoing_edges]) / len(outgoing_edges)
        synced_domains = []

        for domain, level in node.get('knowledge_domains', {}).items():
            # Distortion factor: Low trust creates noise, diminishing structural transmission value
            effective_contribution = level * avg_network_trust
            current_global_level = self.knowledge_commons.get(domain, 0.0)
            
            # Non-linear accumulation: Pooling data from multiple nodes yields diminishing returns
            new_global_level = current_global_level + (effective_contribution * (1.0 - current_global_level))
            self.knowledge_commons[domain] = round(new_global_level, 3)
            synced_domains.append({domain: round(new_global_level, 3)})

        return {"status": "SUCCESS", "synced_by": node_id, "network_cohesion": round(avg_network_trust, 2), "updated_commons": synced_domains}

    # =====================================================================
    # UPGRADED MECHANIC: MULTI-RESOURCE INTEGRATED ROUTING
    # =====================================================================
    def route_inventory(self, sender: str, receiver: str, item_type: str, amount: float) -> Dict[str, Any]:
        """Routes tangible assets from node inventories across the P2P mesh network."""
        if sender not in self.network or receiver not in self.network:
            return {"status": "FAILED", "reason": "Nodes not found."}
            
        # 1. Pathfinding
        try:
            path = nx.shortest_path(self.network, source=sender, target=receiver, weight='cost')
        except nx.NetworkXNoPath:
            return {"status": "FAILED", "reason": "No valid route available."}

        # 2. Local Friction Calculations
        total_friction_multiplier = 1.0
        for i in range(len(path) - 1):
            edge_data = self.network.get_edge_data(path[i], path[i+1])
            total_friction_multiplier *= edge_data['trust']

        arrival_amount = round(amount * total_friction_multiplier, 2)

        # 3. Deduct from Sender and verify Receiver storage capacity limitations
        if not self.adjust_node_inventory(sender, item_type, -amount):
            return {"status": "FAILED", "reason": f"Deduction failed: Insufficient item '{item_type}' at source."}
            
        if not self.adjust_node_inventory(receiver, item_type, arrival_amount):
            # Rollback transaction on sender side if receiver overflows capacity bounds
            self.adjust_node_inventory(sender, item_type, amount)
            return {"status": "FAILED", "reason": f"Routing blocked: Receiver network storage overflow for '{item_type}'."}

        return {
            "status": "SUCCESS",
            "path": path,
            "dispatched": amount,
            "delivered": arrival_amount,
            "wastage": round(amount - arrival_amount, 2)
        }


# =====================================================================
# SIMULATION RUN: RESOURCE MANAGEMENT AND EXPERTISE POOLING
# =====================================================================
if __name__ == "__main__":
    game = HeterarchyEngine()

    # Create network nodes with diverse capabilities and storage sizes
    game.create_node("Tech_Corp", archetype="Corporate", max_capacity=1000.0)
    game.create_node("Medical_Camp", archetype="Community", max_capacity=100.0)
    game.create_node("Research_Uni", archetype="University", max_capacity=200.0)

    # Distribute heterogeneous inventory positions
    game.adjust_node_inventory("Tech_Corp", "Water_Filters", 500.0)
    game.adjust_node_inventory("Medical_Camp", "Water_Filters", 10.0)

    # Assign internal skill domain strengths
    game.set_node_knowledge("Research_Uni", "Virology", level=0.90)
    game.set_node_knowledge("Medical_Camp", "Virology", level=0.40)

    # Establish an uneven trust topography
    game.establish_p2p_channel("Tech_Corp", "Research_Uni", trust_weight=0.90)
    game.establish_p2p_channel("Research_Uni", "Medical_Camp", trust_weight=0.60) # Strained pipeline

    print("--- Initializing State Systems ---")
    print(f"Tech_Corp Stock: {game.network.nodes['Tech_Corp']['inventory']}")
    print(f"Initial Knowledge Commons State: {game.knowledge_commons}")

    # Step 1: Decentralized Knowledge Integration Phase
    print("\n[EVENT]: Factions are uploading research logs into the Knowledge Commons...")
    print(game.sync_to_knowledge_commons("Research_Uni"))
    print(game.sync_to_knowledge_commons("Medical_Camp"))
    print(f"Resulting Global Knowledge Commons Core: {game.knowledge_commons}")

    # Step 2: Resource Push across structural limits
    print("\n[EVENT]: Tech_Corp attempts to route 80 Water_Filters directly to the medical camp...")
    routing_receipt = game.route_inventory("Tech_Corp", "Medical_Camp", "Water_Filters", 80.0)
    print(f"Delivery Assessment: {routing_receipt['status']}")
    if routing_receipt['status'] == "SUCCESS":
        print(f"Delivered through path: {routing_receipt['path']}")
        print(f"Arrived intact: {routing_receipt['delivered']} items.")
    else:
         print(f"Error Diagnostic: {routing_receipt['reason']}")
         
    print(f"\nFinal Medical_Camp Stock Room Ledger: {game.network.nodes['Medical_Camp']['inventory']}")
