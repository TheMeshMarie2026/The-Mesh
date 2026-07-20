"""
mechanics/base.py

Defines the common interface every mechanic must implement, and the
result object mechanics return after execution.

A "mechanic" is a single action implementation (e.g. evacuate, quarantine,
deploy_resource). Each mechanic corresponds to one JSON schema under
schemas/actions/<id>.json, which describes the shape of the action payload
passed to `execute()`.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

# schemas/actions/ lives one level up from mechanics/
SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas" / "actions"


@dataclass
class MechanicResult:
    """Standard return value for every mechanic execution."""
    success: bool
    effects: dict[str, Any] = field(default_factory=dict)
    message: str = ""


class Mechanic(ABC):
    """
    Base class for all mechanics.

    Subclasses must set:
        id          - unique string, must match schemas/actions/<id>.json
        description - short human-readable summary (shows up in docs/CLI)

    Subclasses must implement:
        execute(graph, action, context) -> MechanicResult
    """

    id: str = ""
    description: str = ""

    @abstractmethod
    def execute(self, graph, action: dict, context: Optional[dict] = None) -> MechanicResult:
        """Apply this mechanic's effect to the graph and return a MechanicResult."""
        raise NotImplementedError

    def schema_path(self) -> Path:
        """Path to this mechanic's JSON action schema."""
        return SCHEMA_DIR / f"{self.id}.json"

    def validate(self, action: dict) -> bool:
        """
        Validate an action payload against this mechanic's JSON schema.
        Falls back to a no-op (True) if jsonschema isn't installed or no
        schema file exists yet, so this never blocks early development.
        """
        schema_file = self.schema_path()
        if not schema_file.exists():
            return True
        try:
            import json
            import jsonschema
            schema = json.loads(schema_file.read_text())
            jsonschema.validate(instance=action, schema=schema)
            return True
        except ImportError:
            return True
        except Exception:
            return False
