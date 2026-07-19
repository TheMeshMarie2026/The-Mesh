import json
import networkx as nx

# Assume these exist from previous work:
# - validate_narrator_json(json_obj)
# - apply_narrator_impacts(G, narrator_json)
# - MeshTurnEngine

class ClassroomMeshSession:
    """
    Orchestrates a full classroom session of The Mesh.
    Teacher sets parameters, students choose actions each turn.
    """

    def __init__(self, G, narrator_llm, crisis_state, num_turns=5):
        self.G = G
        self.engine = MeshTurnEngine(G, narrator_llm, crisis_state)
        self.num_turns = num_turns
        self.turn_log = []

    def present_turn_to_class(self, turn_result):
        """
        Present narrative and choices to the class.
        In production, this would be UI; here it's just printing.
        """
        print(f"\n=== TURN {turn_result['turn']} ===")
        print("Crisis State:", turn_result["crisis_state"])
        print("\nNarrative:")
        print(turn_result["narrative"])
        print("\nChoices:")
        for idx, choice in enumerate(turn_result["choices"]):
            print(f"  [{idx}] {choice['text']}")

    def get_class_choice_index(self, turn_result):
        """
        Get the class's chosen option.
        In production, this would be collected via UI.
        Here we use simple input().
        """
        num_choices = len(turn_result["choices"])
        while True:
            try:
                choice_idx = int(input(f"Select a choice [0-{num_choices-1}]: "))
                if 0 <= choice_idx < num_choices:
                    return choice_idx
            except ValueError:
                pass
            print("Invalid selection. Try again.")

    def apply_selected_choice(self, turn_result, choice_idx):
        """
        Apply only the selected choice's impact to the graph.
        """
        selected_choice = turn_result["choices"][choice_idx]
        narrator_json = {
            "narrative": turn_result["narrative"],
            "choices": [selected_choice]  # single choice impact
        }

        # Validate and apply
        validate_narrator_json(narrator_json)
        impact_result = apply_narrator_impacts(self.G, narrator_json)

        # Log
        self.turn_log.append({
            "turn": turn_result["turn"],
            "crisis_state": turn_result["crisis_state"],
            "narrative": turn_result["narrative"],
            "selected_choice": selected_choice,
            "impact_result": impact_result
        })

        return impact_result

    def run_session(self):
        """
        Run the full classroom session for num_turns.
        """
        print("\n=== Starting Mesh Classroom Session ===")
        for _ in range(self.num_turns):
            # 1. Engine runs a turn (generates narrative + choices)
            turn_result = self.engine.run_turn()

            # 2. Present to class
            self.present_turn_to_class(turn_result)

            # 3. Get class choice
            choice_idx = self.get_class_choice_index(turn_result)

            # 4. Apply selected choice impact
            impact_result = self.apply_selected_choice(turn_result, choice_idx)

            print("\nImpact Applied:")
            print(json.dumps(impact_result, indent=2))

        print("\n=== Session Complete ===")
        return self.turn_log


# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    # Example graph
    G = nx.DiGraph()
    G.add_node("Corp_A", Resource_Capacity=10, trust=0.5)
    G.add_node("Student_1", Resource_Capacity=5, trust=0.7)
    G.add_edge("Corp_A", "Student_1", influence_weight=0.2)

    # Fake LLM for demo
    def fake_llm(prompt):
        return json.dumps({
            "narrative": "A cross-border supply chain blockage threatens your ESG commitments.",
            "choices": [
                {
                    "text": "Empower logistics interns to reroute shipments.",
                    "impact": {
                        "node_id": "Student_1",
                        "resource_change": -1.0,
                        "trust_change": 0.2,
                        "edge_weight_change": 0.05
                    }
                },
                {
                    "text": "Give regional managers autonomy over procurement.",
                    "impact": {
                        "node_id": "Corp_A",
                        "resource_change": -2.0,
                        "trust_change": 0.1,
                        "edge_weight_change": 0.03
                    }
                },
                {
                    "text": "Invite university fellows to co-design a decentralized routing protocol.",
                    "impact": {
                        "node_id": "Student_1",
                        "resource_change": -0.5,
                        "trust_change": 0.3,
                        "edge_weight_change": 0.1
                    }
                }
            ]
        })

    crisis_state = {
        "type": "SupplyChain_ESG",
        "severity": 1.0,
        "turn": 0
    }

    session = ClassroomMeshSession(G, fake_llm, crisis_state, num_turns=3)
    log = session.run_session()

    print("\n=== Session Log ===")
    print(json.dumps(log, indent=2))
