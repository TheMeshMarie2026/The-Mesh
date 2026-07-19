from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import networkx as nx

# Import your existing functions
# validate_narrator_json
# apply_narrator_impacts
# MeshTurnEngine

app = FastAPI()

# -------------------------------
# Pydantic models for API payloads
# -------------------------------

class NarratorPayload(BaseModel):
    narrative: str
    choices: list

class TurnRequest(BaseModel):
    narrator_json: NarratorPayload

class CrisisState(BaseModel):
    type: str
    severity: float
    turn: int

# -------------------------------
# Initialize your Mesh graph + engine
# -------------------------------

G = nx.DiGraph()
G.add_node("Corp_A", Resource_Capacity=10, trust=0.5)
G.add_node("Student_1", Resource_Capacity=5, trust=0.7)
G.add_edge("Corp_A", "Student_1", influence_weight=0.2)

def fake_llm(prompt):
    """Replace with your real LLM call inside n8n."""
    return """
    {
      "narrative": "A decentralized routing failure threatens your ESG commitments.",
      "choices": [
        {
          "text": "Empower interns to redesign routing.",
          "impact": {
            "node_id": "Student_1",
            "resource_change": -1.0,
            "trust_change": 0.2,
            "edge_weight_change": 0.05
          }
        },
        {
          "text": "Give regional managers autonomy.",
          "impact": {
            "node_id": "Corp_A",
            "resource_change": -2.0,
            "trust_change": 0.1,
            "edge_weight_change": 0.03
          }
        },
        {
          "text": "Invite university fellows to co-design a decentralized protocol.",
          "impact": {
            "node_id": "Student_1",
            "resource_change": -0.5,
            "trust_change": 0.3,
            "edge_weight_change": 0.1
          }
        }
      ]
    }
    """

crisis_state = {
    "type": "SupplyChain_ESG",
    "severity": 1.0,
    "turn": 0
}

engine = MeshTurnEngine(G, fake_llm, crisis_state)

# -------------------------------
# API ENDPOINTS
# -------------------------------

@app.post("/mesh/run_turn")
def run_turn():
    """
    n8n calls this endpoint to execute a full turn:
    - narrator event
    - JSON validation
    - graph impact
    - crisis progression
    - return structured result for Lovable UI
    """

    try:
        turn_result = engine.run_turn()
        return turn_result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/mesh/apply_choice")
def apply_choice(payload: TurnRequest):
    """
    Lovable calls this endpoint after the class selects a choice.
    Payload contains the narrator JSON with only the selected choice.
    """

    try:
        narrator_json = payload.narrator_json.dict()
        validate_narrator_json(narrator_json)
        impact_result = apply_narrator_impacts(G, narrator_json)

        return {
            "status": "choice_applied",
            "impact_result": impact_result
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/mesh/state")
def get_state():
    """
    Lovable or n8n can call this to retrieve the current crisis state + graph snapshot.
    """

    return {
        "crisis_state": engine.crisis_state,
        "nodes": {n: G.nodes[n] for n in G.nodes()},
        "edges": [
            {"source": u, "target": v, "attrs": attrs}
            for u, v, attrs in G.edges(data=True)
        ]
    }
