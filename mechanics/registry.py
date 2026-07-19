"""
mechanics/registry.py

Central registry for all mechanics. New mechanics register themselves
automatically via the @register_mechanic decorator - no manual list to
maintain. On import, the package walks every module under mechanics/ so
those decorators actually run (see discover() and mechanics/__init__.py).
"""

import importlib
import pkgutil
from typing import Iterable

from mechanics.base import Mechanic


class MechanicRegistry:
    def __init__(self):
        self._mechanics: dict[str, Mechanic] = {}

    def register(self, mechanic_cls: type[Mechanic]) -> type[Mechanic]:
        if not (isinstance(mechanic_cls, type) and issubclass(mechanic_cls, Mechanic)):
            raise TypeError(f"{mechanic_cls!r} must subclass Mechanic")

        instance = mechanic_cls()

        if not instance.id:
            raise ValueError(f"{mechanic_cls.__name__} must define a non-empty 'id'")

        if instance.id in self._mechanics:
            existing = type(self._mechanics[instance.id]).__name__
            raise ValueError(
                f"Duplicate mechanic id '{instance.id}': "
                f"already registered by {existing}, conflicts with {mechanic_cls.__name__}"
            )

        self._mechanics[instance.id] = instance
        return mechanic_cls

    def get(self, mechanic_id: str) -> Mechanic:
        try:
            return self._mechanics[mechanic_id]
        except KeyError:
            known = ", ".join(sorted(self._mechanics)) or "(none registered)"
            raise KeyError(f"No mechanic registered with id '{mechanic_id}'. Known: {known}")

    def all(self) -> dict[str, Mechanic]:
        return dict(self._mechanics)

    def to_manifest(self) -> list[dict]:
        """JSON-serializable summary of every registered mechanic (for docs/CLI/debug tools)."""
        return [
            {
                "id": m.id,
                "description": m.description,
                "class": type(m).__name__,
                "schema": str(m.schema_path()),
                "schema_exists": m.schema_path().exists(),
            }
            for m in sorted(self._mechanics.values(), key=lambda m: m.id)
        ]

    def discover(self, package_name: str, package_path: Iterable[str]) -> None:
        """
        Import every module under the mechanics package so that any
        @register_mechanic decorators inside them execute.
        Skips registry.py and base.py themselves.
        """
        for _, name, _is_pkg in pkgutil.walk_packages(package_path, prefix=f"{package_name}."):
            leaf = name.rsplit(".", 1)[-1]
            if leaf in ("registry", "base"):
                continue
            importlib.import_module(name)


registry = MechanicRegistry()


def register_mechanic(mechanic_cls: type[Mechanic]) -> type[Mechanic]:
    """Class decorator: put @register_mechanic above every Mechanic subclass."""
    return registry.register(mechanic_cls)
