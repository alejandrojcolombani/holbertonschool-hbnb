"""Repository abstractions and in-memory implementation."""

from abc import ABC, abstractmethod


class Repository(ABC):
    """Repository interface."""

    @abstractmethod
    def add(self, obj):
        """Store an object."""

    @abstractmethod
    def get(self, obj_id):
        """Return an object by id."""

    @abstractmethod
    def get_all(self):
        """Return all stored objects."""

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object."""

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object."""

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Return the first object matching an attribute."""


class InMemoryRepository(Repository):
    """Simple in-memory repository used before database persistence."""

    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
        return obj

    def delete(self, obj_id):
        return self._storage.pop(obj_id, None) is not None

    def get_by_attribute(self, attr_name, attr_value):
        for obj in self._storage.values():
            if getattr(obj, attr_name, None) == attr_value:
                return obj
        return None

    def clear(self):
        self._storage.clear()
