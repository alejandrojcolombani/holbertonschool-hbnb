"""Shared model behavior."""

from datetime import datetime, timezone
from uuid import uuid4


class BaseModel:
    """Base class for HBnB domain entities."""

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", str(uuid4()))
        self.created_at = kwargs.get("created_at", self._utcnow())
        self.updated_at = kwargs.get("updated_at", self.created_at)

    @staticmethod
    def _utcnow():
        """Return a timezone-aware UTC timestamp."""

        return datetime.now(timezone.utc)

    def save(self):
        """Refresh the update timestamp."""

        self.updated_at = self._utcnow()

    def update(self, data):
        """Update public attributes from a mapping."""

        for key, value in data.items():
            if key not in {"id", "created_at", "updated_at"} and hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Serialize common model attributes."""

        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
