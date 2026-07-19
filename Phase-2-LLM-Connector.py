import json
import os
from typing import Dict, Any, List

class LLMNarrativeBridge:
    def __init__(self, target_profile: str):
        """Initializes the narrative engine with context on who is playing."""
        self.target_profile = target_profile
        
    def generate_system_prompt(self) -> str:
        """
        Creates a strict system prompt that instructs the LLM to act as a 
        game engine sub-routine, enforcing a rigid output contract.
        """
        return (
            "You are an embedded Narrative Engine for a heterarchical strategy game.\n"
            f"The target audience playing this game is: {self.target_profile}.\n\n"
            "CRITICAL EXPORT CONSTRAINT:\n"
            "You must respond ONLY with a raw, valid JSON object. Do not include introductory text, "
            "do not include markdown codeblocks (e.g., ```json), and do not include postscript notes. "
            "Your output must be perfectly parseable by Python's json.loads().\n\n"
            "JSON SCHEMA EXPECTED:\n"
            "{\n"
            '  "title": "Short, striking title of the event",\n'
            '  "scenario": "A descriptive 3-4 sentence text-based roleplaying scenario tailored to the player profile.",\n'
            '  "choices": [\n'
            "    {\n"
            '      "id": 1,\n'
            '      "text": "Action text detailing how they exercise heterarchical or collaborative power.",\n'
            '      "justification": "Educational text explaining why this aligns or misaligns with heterarchical power.",\n'
            '      "impact": {"trust_delta": float, "knowledge_delta": float, "resource_delta": float}\n'
            "    }\n"
            "  ]\n"
            "}"
        )

    def compile_user_prompt(self, turn_report: Dict[str, Any]) -> str:
        """
        Translates raw Python graph variables and turn logs into an actionable, 
        context-heavy prompt for the LLM.
        """
        emergent_leader = turn_report.get("emergent_leader", "None")
        decay_events = turn_report.get("decay_events", [])
        
        # Flatten structural anomalies into a plain-text prompt variable
        anomaly_summary = ""
        for event in decay_events:
            if event["type"] == "TRUST_DECAY_WARNING":
                anomaly_summary += f"- Critical trust collapse between nodes: {event['channel']}.\n"
            elif event["type"] == "RESOURCE_DRAIN":
                anomaly_summary += f"- Resource drain on node '{event['node']}' due to a deficit of shared knowledge.\n"

        if not anomaly_summary:
            anomaly_summary = "- System is operating at stable decentralization parameters. Minor administrative drag."

        user_prompt = (
            f"GENERATE AN INTERACTIVE CRISIS EVENT MATRIX BASED ON THE FOLLOWING PYTHON STATE:\n\n"
            f"Current Game Turn: {turn_report['turn_number']}\n"
            f"Active Systemic Emergent Leader Node: {emergent_leader}\n"
            f"Detected Graph Anomalies & Friction Points:\n{anomaly_summary}\n\n"
            "INSTRUCTIONS:\n"
            "1. Generate exactly 3 interactive options.\n"
            "2. Make Option 1 an elegant decentralized solution (rewards high trust, shares knowledge).\n"
            "3. Make Option 2 a tempting top-down, command-and-control trap (gains immediate resources, but penalizes trust long-term).\n"
            "4. Ensure that the numerical values inside 'impact' reflect these strategic consequences accurately.\n"
            "5. Tailor the professional tone directly to the player profile context."
        )
        return user_prompt

    def mock_llm_api_call(self, system_prompt: str, user_prompt: str) -> str:
        """
        Simulates an API call to an LLM provider (like OpenAI or Anthropic).
        Returns a raw JSON string matching the required format.
        """
        # In production, replace this block with your active client:
        # response = client.chat.completions.create(model="...", messages=[...])
        # return response.choices[0].message.content
        
        if "corporate" in self.target_profile.lower():
            mock_json = {
                "title": "The Proprietary Knowledge Chokehold",
                "scenario": f"A trust decay warning has hit the communications channel. Your core corporate team wants to classify your node's proprietary data to protect intellectual property from the university lab network node. However, this creates a major informational breakdown, and resources are draining because downstream community actors cannot access the coordination coordinates.",
                "choices": [
                    {
                        "id": 1,
                        "text": "Establish an Open-Source Knowledge Commons platform to clear data filters.",
                        "justification": "Fluidly allocating knowledge builds structural trust and stops localized resource drains across the network topography.",
                        "impact": {"trust_delta": 0.25, "knowledge_delta": 0.15, "resource_delta": -10.0}
                    },
                    {
                        "id": 2,
                        "text": "Enforce strict top-down compliance and execute a command-and-control inventory seize.",
                        "justification": "This provides immediate resources, but relying on centralized power structures breaks horizontal trust and accelerates system isolation.",
                        "impact": {"trust_delta": -0.30, "knowledge_delta": -0.05, "resource_delta": 40.0}
                    },
                    {
                        "id": 3,
                        "text": "Maintain status quo and delegate the communication bottleneck to a middleman node.",
                        "justification": "Bypassing responsibility avoids immediate friction but causes long-term operational inefficiency and slow decay.",
                        "impact": {"trust_delta": -0.05, "knowledge_delta": 0.0, "resource_delta": -5.0}
                    }
                ]
            }
        else:
            # Student-biased narrative focusing on organization and logistical drain
            mock_json = {
                "title": "Decentralized Disorganization Fatigue",
                "scenario": "Your campus activism nodes are highly communicative, but a lack of logistical structure has triggered a resource drain. Student volunteers are burnt out from endless peer-to-peer consensus meetings, and vital water supplies are sitting unrouted in your warehouse.",
                "choices": [
                    {
                        "id": 1,
                        "text": "Designate temporary logistics execution authority to the Logistics_Corp node.",
                        "justification": "Passing leadership to the node with the highest situational capacity is a core mechanic of effective, fluid heterarchy.",
                        "impact": {"trust_delta": 0.10, "knowledge_delta": 0.20, "resource_delta": 15.0}
                    },
                    {
                        "id": 2,
                        "text": "Appoint a single permanent Student Chairman to mandate distribution rules.",
                        "justification": "Falling back into rigid institutional setups relieves short-term chaos but kills horizontal initiative and long-term adaptation.",
                        "impact": {"trust_delta": -0.20, "knowledge_delta": -0.10, "resource_delta": 5.0}
                    },
                    {
                        "id": 3,
                        "text": "Crowdsource a new open planning forum to let volunteers vote on every single box.",
                        "justification": "Over-democratizing low-level logistical tasks wastes valuable time and resources during active global crises.",
                        "impact": {"trust_delta": 0.05, "knowledge_delta": 0.0, "resource_delta": -25.0}
                    }
                ]
            }
        return json.dumps(mock_json, indent=2)

    def execute_narrative_generation(self, turn_report: Dict[str, Any]) -> Dict[str, Any]:
        """Runs the entire pipeline step: building prompts, calling the AI, and parsing the structured data back into Python."""
        sys_p = self.generate_system_prompt()
        user_p = self.compile_user_prompt(turn_report)
        
        # Execute communication with LLM
        raw_response = self.mock_llm_api_call(sys_p, user_p)
        
        try:
            # Secure execution entry point into Python game arrays
            parsed_rpg_event = json.loads(raw_response)
            return parsed_rpg_event
        except json.JSONDecodeError:
            # Built-in recovery fallback block if an LLM outputs malformed characters
            return {
                "title": "Systemic Gridlock",
                "scenario": "A catastrophic network formatting failure has occurred. Communications are down.",
                "choices": [{"id": 1, "text": "Reboot protocols manually.", "justification": "System backup safe state initialization.", "impact": {"trust_delta": -0.05, "knowledge_delta": 0.0, "resource_delta": 0.0}}]
            }


# =====================================================================
# SIMULATION RUN: CONNECTING THE PYTHON BACKEND TO THE NARRATIVE LAYER
# =====================================================================
if __name__ == "__main__":
    # Mock a turn report from your TurnController containing system errors
    simulated_turn_report = {
        "turn_number": 4,
        "emergent_leader": "Research_Uni",
        "decay_events": [
            {"type": "TRUST_DECAY_WARNING", "channel": "Tech_Corp <-> Medical_Camp"},
            {"type": "RESOURCE_DRAIN", "node": "Medical_Camp"}
        ]
    }

    print("--- Testing Corporate Leader RPG Pipeline ---")
    corp_bridge = LLMNarrativeBridge(target_profile="Corporate Leaders and Executives")
