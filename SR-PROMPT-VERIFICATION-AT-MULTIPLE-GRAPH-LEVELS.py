import json
from typing import Dict, Any, List

class LLMNarrativeBridge:
    def __init__(self, target_profile: str, scale_level: str):
        """Initializes the narrative engine with context on who is playing and at what geographic scale."""
        self.target_profile = target_profile
        self.scale_level = scale_level.lower().strip()
        
        # Mapping vocabulary vectors directly to difficulty scopes to shape narrative aesthetics
        self.geo_vocabulary = {
            "local": {
                "spatial_context": "local neighborhood and town council bounds",
                "transit_node": "community distribution center",
                "regulatory_barrier": "municipal zoning permit block",
                "actor_type": "neighborhood volunteer groups",
                "friction_descriptor": "street-level coordination confusion"
            },
            "national": {
                "spatial_context": "interstate transport corridors and federal jurisdictions",
                "transit_node": "regional logistics hub",
                "regulatory_barrier": "domestic trade compliance audit",
                "actor_type": "state-level public agencies",
                "friction_descriptor": "inter-regional bureaucratic gridlock"
            },
            "global": {
                "spatial_context": "transnational maritime lanes and sovereign borders",
                "transit_node": "cross-border customs check-point",
                "regulatory_barrier": "multilateral embargo or tariff enforcement",
                "actor_type": "international NGOs and sovereign states",
                "friction_descriptor": "geopolitical and linguistic communication silos"
            }
        }

    def _get_vocab(self) -> Dict[str, str]:
        """Safely fetches geography terms, falling back to local if input is malformed."""
        for key in self.geo_vocabulary:
            if key in self.scale_level:
                return self.geo_vocabulary[key]
        return self.geo_vocabulary["local"]

    def generate_system_prompt(self) -> str:
        """Creates a system prompt instructing the LLM to write stories locked into the geographic vocabulary constraints."""
        vocab = self._get_vocab()
        
        return (
            "You are an embedded Narrative Engine for a heterarchical strategy game.\n"
            f"The target audience playing this game is: {self.target_profile}.\n"
            f"The current simulation is scaled strictly to a {self.scale_level.upper()} level.\n\n"
            
            "CRITICAL TEXT INJECTION CONSTRAINTS:\n"
            f"When detailing the scenario, you must weave in these exact structural terms appropriately:\n"
            f"- Spatial Context: '{vocab['spatial_context']}'\n"
            f"- Transit Bottleneck: '{vocab['transit_node']}'\n"
            f"- Friction Point: '{vocab['regulatory_barrier']}'\n"
            f"- Systemic Stakeholders: '{vocab['actor_type']}'\n"
            f"- Core Operational Friction: '{vocab['friction_descriptor']}'\n\n"
            
            "CRITICAL EXPORT CONSTRAINT:\n"
            "You must respond ONLY with a raw, valid JSON object. No markdown wrappers (like ```json), no conversation. "
            "Your output must be perfectly parseable by Python's json.loads().\n\n"
            "JSON SCHEMA EXPECTED:\n"
            "{\n"
            '  "title": "Short, striking title matching the scale context",\n'
            '  "scenario": "A descriptive 3-4 sentence text-based roleplaying scenario using the forced vocabulary constraints.",\n'
            '  "choices": [\n'
            "    {\n"
            '      "id": 1,\n'
            '      "text": "Action text detailing how they exercise heterarchical power to bypass the bottleneck.",\n'
            '      "justification": "Educational text explaining why this aligns or misaligns with heterarchical power.",\n'
            '      "impact": {"trust_delta": float, "knowledge_delta": float, "resource_delta": float}\n'
            "    }\n"
            "  ]\n"
            "}"
        )

    def compile_user_prompt(self, turn_report: Dict[str, Any]) -> str:
        """Translates raw turn anomalies into a contextualized request for the LLM."""
        emergent_leader = turn_report.get("emergent_leader", "None")
        decay_events = turn_report.get("decay_events", [])
        
        anomaly_summary = ""
        for event in decay_events:
            if event["type"] == "TRUST_DECAY_WARNING":
                anomaly_summary += f"- Critical trust collapse between nodes: {event['channel']}.\n"
            elif event["type"] == "RESOURCE_DRAIN":
                anomaly_summary += f"- Resource drain on node '{event['node']}' due to a deficit of shared knowledge.\n"

        if not anomaly_summary:
            anomaly_summary = "- Network operational limits are stable."

        user_prompt = (
            f"GENERATE AN INTERACTIVE CRISIS EVENT MATRIX BASED ON THE FOLLOWING STATE:\n\n"
            f"Current Game Turn: {turn_report['turn_number']}\n"
            f"Active Emergent Leader Node: {emergent_leader}\n"
            f"Detected Friction Points:\n{anomaly_summary}\n\n"
            "INSTRUCTIONS:\n"
            "1. Generate exactly 3 interactive options.\n"
            "2. Ensure the text fully reflects the constraints of the required scale-level vocabulary matrix."
        )
        return user_prompt

    def execute_narrative_generation(self, turn_report: Dict[str, Any]) -> Dict[str, Any]:
        """Compiles prompts ready to be shipped directly to an API call like openai.OpenAI()."""
        sys_prompt = self.generate_system_prompt()
        user_prompt = self.compile_user_prompt(turn_report)
        
        # Outputting the prompts generated to verify the spatial vocabulary injection
        return {
            "scale_verified": self.scale_level,
            "generated_system_prompt": sys_prompt,
            "generated_user_prompt": user_prompt
        }


# =====================================================================
# SIMULATION RUN: PROMPT VERIFICATION AT MULTIPLE GRAPH LEVELS
# =====================================================================
if __name__ == "__main__":
    simulated_turn_report = {
        "turn_number": 3,
        "emergent_leader": "Logistics_Hub_Delta",
        "decay_events": [{"type": "TRUST_DECAY_WARNING", "channel": "Node_A <-> Node_B"}]
    }

    print("=====================================================================")
    print("TESTING LOCAL MODE PROMPT COMPILATION (EASY)")
    print("=====================================================================")
    local_bridge = LLMNarrativeBridge(target_profile="University Students", scale_level="local")
    local_prompts = local_bridge.execute_narrative_generation(simulated_turn_report)
    print(local_prompts["generated_system_prompt"])

    print("\n=====================================================================")
    print("TESTING GLOBAL MODE PROMPT COMPILATION (HARD)")
    print("=====================================================================")
    global_bridge = LLMNarrativeBridge(target_profile="Corporate Leaders", scale_level="global")
    global_prompts = global_bridge.execute_narrative_generation(simulated_turn_report)
    print(global_prompts["generated_system_prompt"])
