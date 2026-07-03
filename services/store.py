from typing import Dict, List, Any


class InMemoryStore:
    def __init__(self):
        self.people: List[Dict[str, Any]] = []
        self.land: List[Dict[str, Any]] = []
        self.memory: List[Dict[str, Any]] = []
        self.risks: List[Dict[str, Any]] = []
        self.remittances: List[Dict[str, Any]] = []

    def add(self, collection: str, item: Dict[str, Any]):
        getattr(self, collection).append(item)
        return item


store = InMemoryStore()
