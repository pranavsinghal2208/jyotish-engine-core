from typing import Dict, Any, List, Callable

class CapabilityRegistry:
    """Registry for modular utilities/capabilities."""
    def __init__(self):
        self._capabilities: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable):
        self._capabilities[name] = func

    def execute(self, name: str, context: Any) -> Any:
        if name not in self._capabilities:
            return {"error": f"Capability {name} not found"}
        return self._capabilities[name](context)

    def get_all(self, context: Any) -> Dict[str, Any]:
        results = {}
        for name, func in self._capabilities.items():
            try:
                results[name] = func(context)
            except Exception as e:
                results[name] = {"error": str(e)}
        return results

registry = CapabilityRegistry()