import networkx as nx
from typing import Dict, Any, List, Optional

class TurnController:
    def __init__(self, engine: Any):
        self.engine = engine  # Reference to our HeterarchyEngine
        self.current_turn = 1
        self.active_crisis: Optional[Dict[str, Any]] = None
        self.turn_history: List[Dict[str, Any]] = []

    def set_crisis(self, crisis_type: str, severity: float, demands: Dict[str, float]) -> None:
        """Injects a systemic crisis that the heterarchy must collectively absorb."""
        self.active_crisis = {
            "type": crisis_type,
            "severity": severity,          # Scale 0.0 to 1.0 (Impact multiplier)
            "demands": demands,            # Domain requirements (e.g., {"Virology": 0.8})
            "turns_active": 0
        }

    def process_network_decay(self) -> List[Dict[str, Any]]:
        """
        Simulates natural systemic decay. Crises drain isolated resources, 
        and unmaintained P2P links lose trust over time.
        """
        decay_events = []
        if not self.active_crisis:
            return decay_events

        severity = self.active_crisis["severity"]
        crisis_type = self.active_crisis["type"]

        # 1. Resource Drain: Nodes suffer resource drops if their knowledge doesn't match the crisis
        for node_id, data in self.engine.network.nodes(data=True):
            # Check the global knowledge commons to see if the network has solved this domain
            global_protection = self.engine.knowledge_commons.get(crisis_type, 0.0)
            
            # If the network lacks shared knowledge, resources are burned/lost fighting the crisis
            if global_protection < self.active_crisis["demands"].get(crisis_type, 0.5):
                drain_amount = round(severity * 5.0, 2)
                # Apply drain, ensuring inventory doesn't drop below zero
                for item in data['inventory']:
                    if data['inventory'][item] > 0:
                        actual_drain = min(data['inventory'][item], drain_amount)
                        data['inventory'][item] = round(data['inventory'][item] - actual_drain, 2)
                        decay_events.append({
                            "type": "RESOURCE_DRAIN",
                            "node": node_id,
                            "item": item,
                            "loss": actual_drain,
                            "reason": "Low global network knowledge to defend against crisis"
                        })

        # 2. Trust Decay: Outlying or heavily strained P2P connections degrade
        for u, v, data in self.engine.network.edges(data=True):
            # Friction modifier: High routing cost strains trust further over time
            decay_factor = 0.02 * (1.0 / data['trust'])
            new_trust = max(0.1, round(data['trust'] - decay_factor, 2))
            
            if new_trust != data['trust']:
                self.engine.establish_p2p_channel(u, v, trust_weight=new_trust)
                if new_trust < 0.4:  # Flag critical breakdown
                    decay_events.append({
                        "type": "TRUST_DECAY_WARNING",
                        "channel": f"{u} <-> {v}",
                        "current_trust": new_trust
                    })

        return decay_events

    def evaluate_victory_conditions(self) -> Dict[str, Any]:
        """Evaluates whether the heterarchical system has stabilized, collapsed, or held steady."""
        if not self.active_crisis:
            return {"status": "CONTINUE"}

        crisis_type = self.active_crisis["type"]
        global_knowledge = self.engine.knowledge_commons.get(crisis_type, 0.0)
        target_knowledge = self.active_crisis["demands"].get(crisis_type, 0.5)

        # Total resources remaining in the entire system
        total_system_resources = 0.0
        for _, data in self.engine.network.nodes(data=True):
            total_system_resources += sum(data['inventory'].values())

        # Win: Heterarchy successfully pooled enough decentralized data to nullify the threat
        if global_knowledge >= target_knowledge:
            return {"status": "VICTORY", "reason": f"Knowledge Commons stabilized the {crisis_type} event."}

        # Lose: System runs completely dry of materials due to structural hoarding/friction
        if total_system_resources <= 0:
            return {"status": "COLLAPSE", "reason": "Systemic bankruptcy. All nodes depleted their logistical reserves."}

        return {"status": "CONTINUE", "remaining_resources": total_system_resources}

    def advanced_turn_loop(self) -> Dict[str, Any]:
        """
        Executes the macro state transition logic for the current turn.
        Merges backend math with system flags to trigger text-based RPG layers.
        """
        # 1. Increment chronological tracking
        self.current_turn += 1
        if self.active_crisis:
            self.active_crisis["turns_active"] += 1

        # 2. Run background simulation math
        decay_logs = self.process_network_decay()

        # 3. Dynamically re-evaluate and shift network leadership authority based on current threat
        leadership_update = {}
        if self.active_crisis:
            leadership_update = self.engine.shift_leadership_weights(
                self.active_crisis["type"], 
                self.active_crisis["demands"]
            )

        # 4. Check for system anomalies to build narrative RPG hooks
        rpg_triggers = []
        for event in decay_logs:
            if event["type"] == "TRUST_DECAY_WARNING":
                rpg_triggers.append({
                    "context": "NETWORK_ISOLATION_RISK",
                    "target_channel": event["channel"],
                    "prompt_hook": "Local actors are blocking communication lines due to top-down negligence."
                })

        # 5. Determine game state termination
        game_evaluation = self.evaluate_victory_conditions()

        turn_snapshot = {
            "turn_number": self.current_turn,
            "game_status": game_evaluation["status"],
            "emergent_leader": leadership_update.get("emergent_leader"),
            "decay_events": decay_logs,
            "rpg_prompts_required": rpg_triggers
        }
        
        self.turn_history.append(turn_snapshot)
        return turn_snapshot


# =====================================================================
# SIMULATION RUN: TURNS, THREAT DECAY, AND NARRATIVE HOOKS
# =====================================================================
if __name__ == "__main__":
    from heterarchy_engine import HeterarchyEngine # Assumes prior code layer exists
    
    # Setup baseline network configurations
    engine = HeterarchyEngine()
    engine.create_node("Tech_Corp", archetype="Corporate", max_capacity=1000.0)
    engine.create_node("Medical_Camp", archetype="Community", max_capacity=100.0)
    engine.adjust_node_inventory("Tech_Corp", "Water_Filters", 50.0)
    engine.set_node_knowledge("Medical_Camp", "Logistics", level=0.8)
    
    # Establish a weak connection to demonstrate decay mechanics
    engine.establish_p2p_channel("Tech_Corp", "Medical_Camp", trust_weight=0.45)

    # Initialize Turn Controller
    controller = TurnController(engine)
    
    # Target condition: System needs 0.75 Logistics knowledge pooled to win
    controller.set_crisis(crisis_type="Logistics", severity=0.6, demands={"Logistics": 0.75})

    print(f"=== Starting Turn {controller.current_turn} ===")
    print(f"Active Threat: {controller.active_crisis['type']} | Severity: {controller.active_crisis['severity']}")

    # Process to next turn
    turn_report = controller.advanced_turn_loop()
    
    print(f"\n=== Turn {turn_report['turn_number']} Report ===")
    print(f"System State: {turn_report['game_status']}")
    print(f"Emergent Leader: {turn_report['emergent_leader']}")
    
    print("\nDecay Events Evaluated:")
    for decay in turn_report['decay_events']:
        print(f" - {decay['type']} on {decay.get('node', decay.get('channel'))} | Metric Drop Detected")

    if turn_report['rpg_prompts_required']:
        print("\n⚠️ RPG Prompts Flags Raised for Developer Interface Engine:")
        for trigger in turn_report['rpg_prompts_required']:
            print(f" - Trigger [{trigger['context']}]: {trigger['prompt_hook']}")
