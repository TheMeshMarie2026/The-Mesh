from typing import Dict, Any

class DifficultyTuner:
    """
    Configures network topology constraints, scale parameters, and audience biases.
    Easy = Local Community, Medium = National Community, Hard = Global Community.
    """
    
    @staticmethod
    def get_scale_config(scale_level: str) -> Dict[str, Any]:
        """Calculates geographic scope multipliers based on network distance principles."""
        scale = scale_level.lower().strip()
        
        if "easy" in scale or "local" in scale:
            return {
                "scale_name": "Local Community Scope",
                "base_network_nodes": 5,           # Small, easily coordinated cluster
                "geographic_trust_penalty": 0.0,   # High local trust / shared accountability
                "routing_distance_cost": 1.0,      # Compact localized routing hops
                "global_multiplier": 1.0
            }
            
        elif "medium" in scale or "national" in scale:
            return {
                "scale_name": "National Community Scope",
                "base_network_nodes": 15,          # Mid-sized complex network mesh
                "geographic_trust_penalty": 0.15,  # Bureaucratic/regional friction cuts baseline trust
                "routing_distance_cost": 1.35,     # Increased physical hops degrade inventory speed
                "global_multiplier": 1.4
            }
            
        elif "hard" in scale or "global" in scale:
            return {
                "scale_name": "Global Community Scope",
                "base_network_nodes": 40,          # Massive asymmetric global graph topography
                "geographic_trust_penalty": 0.35,  # Geopolitical/linguistic gaps drop baseline trust
                "routing_distance_cost": 2.0,      # Global shipping lanes experience severe friction
                "global_multiplier": 2.0
            }
            
        else:
            raise ValueError(f"Unknown scope scale selection: {scale_level}")

    @classmethod
    def apply_combined_tuning(cls, engine: Any, controller: Any, audience_profile: str, scale_level: str) -> Dict[str, Any]:
        """
        Merges audience profiles (Corporate vs Student) with scope modifiers (Local, National, Global)
        and injects the resulting mathematical constraints directly into the network.
        """
        # Fetch individual baseline configurations
        scale_config = cls.get_scale_config(scale_level)
        
        # Pull original logic parameters from previous step configuration
        if "corporate" in audience_profile.lower():
            base_decay = 0.04
            base_friction = 1.15
        else:
            base_decay = 0.015
            base_friction = 1.02
            
        # Composite Math: Scale levels magnify original operational friction coefficients
        final_trust_decay = base_decay + scale_config["geographic_trust_penalty"] * 0.05
        final_friction = base_friction * scale_config["routing_distance_cost"]
        
        # Inject directly back into runtime controllers
        controller.trust_decay_rate = round(final_trust_decay, 4)
        if hasattr(controller, 'active_crisis') and controller.active_crisis:
            controller.active_crisis["severity"] *= scale_config["global_multiplier"]
            
        # Store metadata inside engine structure for tracking
        engine.active_scale_metrics = scale_config
        engine.base_routing_friction_multiplier = round(final_friction, 2)

        return {
            "applied_scale": scale_config["scale_name"],
            "nodes_to_generate": scale_config["base_network_nodes"],
            "calculated_trust_decay": round(final_trust_decay, 4),
            "calculated_routing_friction": round(final_friction, 2)
        }


# =====================================================================
# SIMULATION RUN: MATRIX INJECTION BASED ON SCALE AND USER INTERFACE
# =====================================================================
if __name__ == "__main__":
    from heterarchy_engine import HeterarchyEngine
    from turn_controller import TurnController

    engine = HeterarchyEngine()
    controller = TurnController(engine)
    controller.set_crisis(crisis_type="CONFLICT", severity=0.5, demands={"CONFLICT": 0.6})

    print("--- Executing Matrix Scale Tuning Test ---")

    # Scenario 1: Corporate leaders playing on Medium (National Scale)
    config_1 = DifficultyTuner.apply_combined_tuning(
        engine, controller, 
        audience_profile="Corporate Leaders", 
        scale_level="medium"
    )
    print(f"\nTest 1 (Corporate + National):")
    print(f" -> Chosen Scope: {config_1['applied_scale']}")
    print(f" -> Network Node Density: {config_1['nodes_to_generate']}")
    print(f" -> Injected Step Decay Rate: {config_1['calculated_trust_decay']}")
    print(f" -> Composite Route Friction Modifier: {config_1['calculated_routing_friction']}x")

    # Scenario 2: University Students playing on Hard (Global Scale)
    config_2 = DifficultyTuner.apply_combined_tuning(
        engine, controller, 
        audience_profile="University Students", 
        scale_level="hard"
    )
    print(f"\nTest 2 (Students + Global):")
    print(f" -> Chosen Scope: {config_2['applied_scale']}")
    print(f" -> Network Node Density: {config_2['nodes_to_generate']}")
    print(f" -> Injected Step Decay Rate: {config_2['calculated_trust_decay']}")
    print(f" -> Composite Route Friction Modifier: {config_2['calculated_routing_friction']}x")
