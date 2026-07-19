"""
The Mesh — Unified Main Entry Point
-----------------------------------
This file initializes the full Mesh engine:

1. Load scenario JSON
2. Build the dynamic graph
3. Register mechanics
4. Load action + protocol schemas
5. Initialize narrator + impact systems
6. Run the crisis loop
"""

import json
import os
import networkx as nx

# -----------------------------
# Engine Imports
# -----------------------------
from engine.graph.asset-features import apply_asset_features
from engine.graph.Node-Merge import merge_nodes
from engine.graph.Cross-Node-Coordination-Model import apply_coordination_model
from engine.graph.Technical-Infrastructure-Models import apply_infrastructure_models

from engine.impact.Difficulty-Levels import apply_difficulty_level
from engine.impact.Difficulty-Scaling import scale_impacts
from engine.impact.Balance-Carbon-Units import balance_carbon
from engine.impact.Turns-ThreatDecay-NarrativeHooks import apply_threat_decay

from engine.narrator.Python-Prompt-Loader import load_narrator_prompts
from engine.narrator.SR-PROMPT-VERIFICATION-AT-MULTIPLE-GRAPH-LEVELS import validate_narrator_output

from engine.Protocol-Dynamics import execute_protocol
from engine.Phase-2-LLM-Connector import call_llm_narrator
from engine.Student-VS-Corporate-Overlay import apply_overlay


# -----------------------------
# Mechanics Imports
# -----------------------------
from mechanics.Classroom-Team-Negotiation import classroom_team_negotiation
from mechanics.Conflict-Negotiation import conflict_negotiation
from mechanics.Information-Sharing import information_sharing
from mechanics.Intelligence import intelligence_action
from mechanics.Knowledge-Pooling-Mechanic import knowledge_pooling
from mechanics.Resource-Routing-Engine import resource_routing
from mechanics.Resource-Routing-Negotiation-Trigger import routing_negotiation_trigger
from mechanics.Crisis-Forecast import crisis_forecast
from mechanics.PROCUREMENT-Data-DRIVERS import procurement_drivers
from mechanics.Rules-Checklist import rules_checklist


# -----------------------------
# Schema Loading
# -----------------------------
SCHEMA_DIR = "schemas"

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def load_schemas():
    actions = {}
    protocols = {}
    scenarios = {}

    # Load action schemas
    actions_dir = os.path.join(SCHEMA_DIR, "actions")
    for file in os.listdir(actions_dir):
        if file.endswith(".json"):
            actions[file] = load_json(os.path.join(actions_dir, file))

    # Load protocol schemas
    protocols_dir = os.path.join(SCHEMA_DIR, "protocols")
    for file in os.listdir(protocols_dir):
        if file.endswith(".json"):
            protocols[file] = load_json(os.path.join(protocols_dir, file))

    # Load scenario schemas
    scenarios_dir = os.path.join(SCHEMA_DIR, "scenarios")
    for file in os.listdir(scenarios_dir):
        if file.endswith(".json"):
            scenarios[file] = load_json(os.path.join(scenarios_dir, file))

    return actions, protocols, scenarios


# -----------------------------
# Graph Initialization
# -----------------------------
def initialize_graph(scenario):
    G = nx.Graph()

    # Load nodes
    for node in scenario.get("nodes", []):
        G.add_node(node["id"], **node)

    # Load edges
    for edge in scenario.get("edges", []):
        G.add_edge(edge["source"], edge["target"], **edge)

    # Apply graph-level models
    apply_asset_features(G)
    apply_coordination_model(G)
    apply_infrastructure_models(G)

    return G


# -----------------------------
# Mechanic Registry
# -----------------------------
MECHANICS = {
    "classroom_team_negotiation": classroom_team_negotiation,
    "conflict_negotiation": conflict_negotiation,
    "information_sharing": information_sharing,
    "intelligence": intelligence_action,
    "knowledge_pooling": knowledge_pooling,
    "resource_routing": resource_routing,
    "routing_negotiation_trigger": routing_negotiation_trigger,
    "crisis_forecast": crisis_forecast,
    "procurement_drivers": procurement_drivers,
}


# -----------------------------
# Crisis Loop
# -----------------------------
def run_crisis_loop(G, scenario, actions, protocols):
    narrator_prompts = load_narrator_prompts()

    for turn in range(scenario.get("turns", 5)):
        print(f"\n--- TURN {turn + 1} ---")

        # Apply difficulty + threat decay
        apply_difficulty_level(G)
        apply_threat_decay(G)

        # Execute scheduled protocols
        for protocol_name in scenario.get("protocols", []):
            protocol_schema = protocols.get(protocol_name)
            if protocol_schema:
                execute_protocol(G, protocol_schema)

        # Execute actions
        for action_event in scenario.get("actions", []):
            action_type = action_event["action_type"]
            mechanic = MECHANICS.get(action_type)

            if mechanic:
                mechanic(G, action_event)

        # Narrator step
        narrator_output = call_llm_narrator(G, narrator_prompts)
        validate_narrator_output(G, narrator_output)

        # Apply impact scaling
        scale_impacts(G)
        balance_carbon(G)

    return G


# -----------------------------
# Main Entry Point
# -----------------------------
if __name__ == "__main__":
    print("Loading Mesh schemas...")
    actions, protocols, scenarios = load_schemas()

    # Pick the first scenario for now
    scenario_name = list(scenarios.keys())[0]
    scenario = scenarios[scenario_name]

    print(f"Initializing scenario: {scenario_name}")
    G = initialize_graph(scenario)

    print("Applying overlays...")
    apply_overlay(G)

    print("Starting crisis loop...")
    final_graph = run_crisis_loop(G, scenario, actions, protocols)

    print("\nSimulation complete.")
    print("Final graph state:")
    print(final_graph.nodes(data=True))
    print(final_graph.edges(data=True))
