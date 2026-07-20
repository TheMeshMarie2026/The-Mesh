"""
tools/validate_schema_refs.py

Checks that every scenario's protocol and action references use bare ids
("evacuate") rather than filenames ("evacuate.json"), and that every id
referenced actually has a matching schema file. This is the exact class
of bug that made protocols.get(protocol_name) silently return None for
every protocol - this script catches it before you hit run.

Usage:
    python3 tools/validate_schema_refs.py

Exits 0 if everything checks out, 1 if any problems were found (so this
can be dropped into a pre-run check or CI later).
"""

import json
import os
import sys

SCHEMA_DIR = "schemas"


def _load_json_dir(path):
    """Same convention as main.py: keys are filenames with '.json' stripped."""
    result = {}
    if not os.path.isdir(path):
        return result
    for file in sorted(os.listdir(path)):
        if file.endswith(".json"):
            key = file[: -len(".json")]
            with open(os.path.join(path, file)) as f:
                result[key] = json.load(f)
    return result


def check_ref(ref: str, known_ids: set, ref_kind: str, scenario_name: str, problems: list):
    """Check a single protocol/action-type reference against known schema ids."""
    if ref.endswith(".json"):
        problems.append(
            f"[{scenario_name}] {ref_kind} '{ref}' includes '.json' - "
            f"should be '{ref[:-len('.json')]}' to match the bare-id convention."
        )
        return

    if ref not in known_ids:
        problems.append(
            f"[{scenario_name}] {ref_kind} '{ref}' has no matching schema file "
            f"in schemas/{'protocols' if ref_kind == 'protocol' else 'actions'}/."
        )


def main():
    actions = _load_json_dir(os.path.join(SCHEMA_DIR, "actions"))
    protocols = _load_json_dir(os.path.join(SCHEMA_DIR, "protocols"))
    scenarios = _load_json_dir(os.path.join(SCHEMA_DIR, "scenarios"))

    if not scenarios:
        print("No scenario files found under schemas/scenarios/ - nothing to check.")
        return 0

    action_ids = set(actions.keys())
    protocol_ids = set(protocols.keys())

    problems = []

    for scenario_name, scenario in scenarios.items():
        # Protocol references
        for protocol_ref in scenario.get("protocols", []):
            check_ref(protocol_ref, protocol_ids, "protocol", scenario_name, problems)

        # Action references (each action event's "action_type")
        for action_event in scenario.get("actions", []):
            action_type = action_event.get("action_type")
            if action_type is None:
                problems.append(
                    f"[{scenario_name}] action entry missing 'action_type' key: {action_event}"
                )
                continue
            check_ref(action_type, action_ids, "action", scenario_name, problems)

    print(f"Checked {len(scenarios)} scenario(s), "
          f"{len(action_ids)} action schema(s), {len(protocol_ids)} protocol schema(s).\n")

    if problems:
        print(f"Found {len(problems)} problem(s):\n")
        for p in problems:
            print(f"  - {p}")
        return 1

    print("All protocol and action references check out.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
