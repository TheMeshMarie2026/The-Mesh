"""
The Mesh — Unified Main Entry Point
-----------------------------------
Boots the full Mesh engine end to end:

1. Load action / protocol / scenario schemas from schemas/
2. Pick a scenario and build its graph
3. Apply graph-level models (asset features, coordination, infrastructure)
4. Run the multi-turn crisis loop (protocols -> actions -> narrator -> impact)
5. Print final graph state

NOTE ON IMPORTS BELOW: these assume every hyphenated filename in engine/
and mechanics/ has been renamed to snake_case (e.g. asset-features.py ->
asset_features.py). Python module names cannot contain hyphens - the
original hyphenated imports are a SyntaxError, not just a style issue.
"""

import json
import os
import networkx as nx

# -----------------------------
# Engine Imports
# -----------------------------
# Graph-level models: applied once, right after a scenario's raw nodes/edges
# are loaded into a networkx graph.
from engine.graph.asset_features import apply_asset_features
from engine.graph.node_merge import merge_nodes
from engine.graph.cross_node_coordination_model import apply_coordination_model
from engine.graph.technical_infrastructure_models import apply_infrastructure_models

# Impact models: applied every turn inside the crisis loop.
from engine.impact.difficulty_levels import apply_difficulty_level
from engine.impact.difficulty_scaling import scale_impacts
from engine.impact.balance_carbon_units import balance_carbon
from engine.impact.turns_threatdecay_narrativehooks import apply_threat_decay

# Narrator: builds prompts once, then generates + validates output each turn.
from engine.narrator.python_prompt_loader import load_narrator_prompts
from engine.narrator.sr_prompt_verification_at_multiple_graph_levels import validate_narrator_output

# Core orchestrators (top-level engine/, not a subfolder).
from engine.protocol_dynamics import execute_protocol
from engine.phase_2_llm_connector import call_llm_narrator
from engine.student_vs_corporate_overlay import apply_overlay


# -----------------------------
# Mechanics Registry
# -----------------------------
# Every mechanic - native Mechanic subclasses (e.g. mechanics/evacuate.py)
# and the legacy plain-function mechanics wrapped in
# mechanics/legacy_registrations.py - registers itself automatically the
# moment this package is imported. No manual per-mechanic import list and
# no hand-maintained id -> callable dict to keep in sync (see run_action()
# below for the dispatch itself).
from mechanics import registry as mechanics_registry

# ASSUMPTION: rules_checklist reads as a rule-based validation gate rather
# than something a scenario dispatches by action_type - so it's wired into
# run_action() below as a pre-execution check, not registered in the
# mechanics registry alongside evacuate/resource_routing/etc. Its exact
# signature is unconfirmed; this assumes rules_checklist(graph, action)
# -> bool (True = allowed to proceed). If the real signature or behavior
# differs, update both this import and the single call site in
# run_action() - that's the only place it's used.
from mechanics.rules_checklist import rules_checklist


# -----------------------------
# Schema Loading
# -----------------------------
SCHEMA_DIR = "schemas"


def load_json(path):
    """Read and parse a single JSON file."""
    with open(path, "r") as f:
        return json.load(f)


def _load_json_dir(path):
    """
    Load every .json file in a directory into a dict keyed by the file's
    base name with '.json' stripped (e.g. 'evacuate.json' -> 'evacuate').
    This keeps schema/protocol/scenario keys consistent with the plain
    action-type strings used everywhere else (MECHANICS dict, scenario
    action lists, etc.) instead of mixing in the '.json' suffix.

    Sorted so scenario/schema selection is deterministic across runs and
    operating systems - os.listdir() order is NOT guaranteed.
    """
    result = {}
    if not os.path.isdir(path):
        # Don't hard-fail if e.g. schemas/protocols/ doesn't exist yet -
        # some schema categories may not be populated this early.
        return result
    for file in sorted(os.listdir(path)):
        if file.endswith(".json"):
            key = file[: -len(".json")]
            result[key] = load_json(os.path.join(path, file))
    return result


def load_schemas():
    """Load all action, protocol, and scenario schemas from schemas/."""
    actions = _load_json_dir(os.path.join(SCHEMA_DIR, "actions"))
    protocols = _load_json_dir(os.path.join(SCHEMA_DIR, "protocols"))
    scenarios = _load_json_dir(os.path.join(SCHEMA_DIR, "scenarios"))
    return actions, protocols, scenarios


# -----------------------------
# Graph Initialization
# -----------------------------
def initialize_graph(scenario):
    """Build a networkx graph from a scenario's node/edge definitions,
    then apply the graph-level models that need to run once, up front."""
    G = nx.Graph()

    for node in scenario.get("nodes", []):
        G.add_node(node["id"], **node)

    for edge in scenario.get("edges", []):
        G.add_edge(edge["source"], edge["target"], **edge)

    # Graph-level models. Order matters if any of these depend on features
    # set by an earlier one - verify against each function's docstring.
    apply_asset_features(G)
    apply_coordination_model(G)
    apply_infrastructure_models(G)

    return G


def run_action(graph: nx.Graph, action: dict):
    """
    Execute a single action against the graph.

    Pulled out of the crisis loop's inner for-loop so a single action can
    be run in isolation - from a unit test, a future debugging/CLI tool,
    or the graph-validation tool on the roadmap - without spinning up a
    full scenario + crisis loop just to exercise one mechanic.

    Looks up the mechanic by action["action_type"] in the mechanics
    registry and calls its .execute(). Returns the MechanicResult (or
    None if the action was skipped due to a missing/unknown action_type).
    """
    action_type = action.get("action_type")
    if action_type is None:
        print("  [WARN] Action missing 'action_type' key, skipping:", action)
        return None

    try:
        mechanic = mechanics_registry.get(action_type)
    except KeyError as e:
        print(f"  [WARN] {e}")
        return None

    # Rule-based validation gate - separate from (and in addition to) any
    # JSON-schema validation the mechanic itself does. See the ASSUMPTION
    # note on the rules_checklist import above if this call site needs
    # to change.
    if not rules_checklist(graph, action):
        print(f"  [WARN] Action '{action_type}' failed rules_checklist, skipping: {action}")
        return None

    return mechanic.execute(graph, action)


def _iter_turns(scenario):
    """
    Yield (protocols_for_turn, actions_for_turn) once per turn.

    Preferred scenario shape - "turns" is a list, one entry per turn:
        {"turns": [
            {"protocols": [...], "actions": [...]},
            {"protocols": [...], "actions": [...]}
        ]}

    Legacy shape, still supported - "turns" is a count, and the same
    flat protocols/actions lists are replayed every turn:
        {"turns": 5, "protocols": [...], "actions": [...]}
    """
    turns = scenario.get("turns", [])

    if isinstance(turns, list):
        for turn in turns:
            yield turn.get("protocols", []), turn.get("actions", [])
    else:
        # turns is an int (or missing, defaulting to 5) - old flat shape.
        flat_protocols = scenario.get("protocols", [])
        flat_actions = scenario.get("actions", [])
        for _ in range(turns if isinstance(turns, int) else 5):
            yield flat_protocols, flat_actions


def run_crisis_loop(G, scenario, actions, protocols):
    """
    Advance the scenario turn by turn. Each turn:
      1. Apply difficulty scaling + threat decay to the graph
      2. Execute this turn's scheduled protocols
      3. Execute this turn's actions via run_action()
      4. Ask the narrator to describe what happened, and validate its output
      5. Rebalance impact/carbon totals

    Turn-by-turn protocols/actions come from _iter_turns(), which
    understands both the new per-turn scenario shape and the older flat
    shape (same actions/protocols replayed every turn) - see its
    docstring for both formats.
    """
    narrator_prompts = load_narrator_prompts()

    turns_list = list(_iter_turns(scenario))
    if not turns_list:
        print("  [WARN] Scenario has no turns defined - nothing to run.")

    for turn_index, (turn_protocols, turn_actions) in enumerate(turns_list):
        print(f"\n--- TURN {turn_index + 1} ---")

        # Step 1: difficulty + threat decay
        apply_difficulty_level(G)
        apply_threat_decay(G)

        # Step 2: this turn's protocols.
        # NOTE: protocols dict is keyed without '.json' (see
        # _load_json_dir), so protocol_name here must match that -
        # e.g. "resource_share_protocol", not "resource_share_protocol.json".
        for protocol_name in turn_protocols:
            protocol_schema = protocols.get(protocol_name)
            if protocol_schema is None:
                print(f"  [WARN] Unknown protocol '{protocol_name}', skipping.")
                continue
            execute_protocol(G, protocol_schema)

        # Step 3: this turn's actions, via the shared run_action() entry point.
        for action_event in turn_actions:
            run_action(G, action_event)

        # Step 4: narrator
        narrator_output = call_llm_narrator(G, narrator_prompts)
        validate_narrator_output(G, narrator_output)

        # Step 5: impact rebalancing
        scale_impacts(G)
        balance_carbon(G)

    return G


# -----------------------------
# Main Entry Point
# -----------------------------
if __name__ == "__main__":
    print("Loading Mesh schemas...")
    actions, protocols, scenarios = load_schemas()

    if not scenarios:
        raise SystemExit("No scenario files found in schemas/scenarios/ - nothing to run.")

    # Picks the first scenario alphabetically (deterministic, unlike the
    # previous os.listdir()-order version). Still a placeholder - swap
    # for real scenario selection (config file or CLI arg) per the
    # "scenario selection system" roadmap item.
    scenario_name = sorted(scenarios.keys())[0]
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
