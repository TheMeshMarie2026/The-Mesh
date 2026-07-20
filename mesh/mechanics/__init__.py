"""
mechanics/

Action implementations for The Mesh. Every mechanic in this package
registers itself automatically when the package is imported - just
subclass Mechanic, decorate with @register_mechanic, and drop the file
anywhere under mechanics/. No manual registration list to maintain.

Usage elsewhere (e.g. engine/ or main.py):

    from mechanics import registry

    mechanic = registry.get("evacuate")
    result = mechanic.execute(graph, action)
"""

from mechanics.base import Mechanic, MechanicResult
from mechanics.registry import registry, register_mechanic

# Import every module under mechanics/ so @register_mechanic decorators run.
registry.discover(__name__, __path__)

__all__ = ["Mechanic", "MechanicResult", "registry", "register_mechanic"]
