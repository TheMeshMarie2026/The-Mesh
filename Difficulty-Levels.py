

import Dict, Any

class DifficultyTuner:
    """
    Configures and injects biased network parameters into the HeterarchyEngine.
    Balances the simulation to target specific behavioral flaws in corporate and student players.
    """
    
    @staticmethod
    def get_profile_config(audience_profile: str) -> Dict[str, Any]:
        """Returns structural game parameters tuned to specific behavioral player profiles."""
        
        # Normalize profile inputs
        profile = audience_profile.lower().strip()
        
        if "corporate" in profile or "leader" in profile:
            return {
                "profile_name": "Asymmetric Corporate Hierarchy Challenge",
                # Anti-Hoarding Friction: High penalties for resource consolidation
                "trust_decay_rate": 0.04,          # Double decay rate for unmaintained links
                "base_routing_friction": 1.15,      # 15% baseline structural loss on material transits
                "knowledge_pooling_diminishing_returns": 0.85, # Harder to build shared data commons
                "starting_capacity_multiplier": {
                    "Corporate": 1.5,               # Huge starting storage capacity
                    "Community": 0.6,               # Tiny community nodes (forces them to distribute assets)
                    "University": 0.9
                },
                "crisis_severity_multiplier": 1.2,  # Faster escalation loops if hierarchy forms
                "educational_focus": "Teaches decentralization, power delegation, and trust building over asset hoarding."
            }
            
        elif "student" in profile or "university" in profile:
            return {
                "profile_name": "Logistical Scalability & Resource Scarcity Challenge",
                # Logistical Bottleneck Friction: High penalties for careless resource spending
                "trust_decay_rate": 0.015,         # Slower relationship decay (students build trust fast)
                "base_routing_friction": 1.02,      # Minimal baseline shipping loss
                "knowledge_pooling_diminishing_returns": 0.40, # Highly efficient open-source sharing
                "starting_capacity_multiplier": {
                    "Corporate": 0.8,
                    "Community": 1.0,
                    "University": 1.0               # Standard, even storage limits across nodes
                },
                "crisis_severity_multiplier": 0.9,
                # The Core Constraint for Students: Strict resource consumption rates
                "resource_burn_rate_modifier": 1.5, # 50% faster resource burn rate during structural crises
                "educational_focus": "Teaches logistics management, physical limits, and sustainable supply routing."
            }
            
        else:
            # Baseline sandbox default configuration
            return {
                "profile_name": "Standard Equilibrium Sandbox",
                "trust_decay_rate": 0.02,
                "base_routing_friction": 1.0,
                "knowledge_pooling_diminishing_returns": 0.60,
                "starting_capacity_multiplier": {"Corporate": 1.0, "Community": 1.0, "University": 1.0},
                "crisis_severity_multiplier": 1.0,
                "educational_focus": "Standard game balance verification loop."
            }

    @classmethod
    def apply_tuning(cls, engine: Any, controller: Any, profile_type: str) -> Dict[str, Any]:
        """Injects configuration variables directly into active engine and turn controller objects."""
        config = cls.get_profile_config(profile_type)
        
        # 1. Update Turn Controller Decay Rates
        if hasattr(controller, 'trust_decay_rate'):
            # Modifies the internal mathematical decay formula
            controller.trust_decay_rate = config["trust_decay_rate"]
        
        # 2. Inject resource consumption modifiers into the active crisis metrics
        if hasattr(controller, 'active_crisis') and controller.active_crisis:
            controller.active_crisis["severity"] *= config["crisis_severity_multiplier"]
            if "resource_burn_rate_modifier" in config:
                controller.active_crisis["burn_modifier"] = config["resource_burn_rate_modifier"]

        # 3. Dynamic adjustment of global Knowledge Commons absorption coefficients
        # High diminishing returns = nodes must upload flawless data or it's ignored
        engine.pooling_coefficient = config["knowledge_pooling_diminishing_returns"]

        return config


# =====================================================================
# SIMULATION RUN: TUNING THE HETERARCHY IN REALTIME
# =====================================================================
if __name__ == "__main__":
    from heterarchy_engine import HeterarchyEngine
    from turn_controller import TurnController

    # Initialize generic engine structural arrays
    game_engine = HeterarchyEngine()
    turn_loop = TurnController(game_engine)
    
    print("--- Heterarchy Configuration Initialized ---")
    
    # CASE A: Tuning the engine for Corporate Factions
    print("\n[CONFIGURING]: Initializing Profile for: 'Executive Leadership Cohort 2026'...")
    corp_specs = DifficultyTuner.apply_tuning(game_engine, turn_loop, profile_type="Corporate Leaders")
    
    print(f"Active Rule Matrix: {corp_specs['profile_name']}")
    print(f"Target Educational Objective: {corp_specs['educational_focus']}")
    print(f"System Baseline Trust Decay Factor: {corp_specs['trust_decay_rate']} per turn.")
    
    # CASE B: Tuning the engine for University Factions
    print("\n[CONFIGURING]: Adjusting Pipeline for: 'Undergraduate Systems Engineering Lab'...")
    student_specs = DifficultyTuner.apply_tuning(game_engine, turn_loop, profile_type="University Students")
    
    print(f"Active Rule Matrix: {student_specs['profile_name']}")
    print(f"Target Educational Objective: {student_specs['educational_focus']}")
    print(f"System Baseline Knowledge Pooling Diminishing Penalty: {student_specs['knowledge_pooling_diminishing_returns']}")
