"""Amenity domain model."""

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Feature available at a place."""

    def __init__(self, name, description="", **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description or ""

    @staticmethod
    def _validate_name(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("name is required")
        value = value.strip()
        if len(value) > 50:
            raise ValueError("name must be 50 characters or fewer")
        return value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = self._validate_name(value)

    def update(self, data):
        clean_data = {}
        if "name" in data:
            clean_data["name"] = self._validate_name(data["name"])
        if "description" in data:
            clean_data["description"] = data["description"] or ""
        super().update(clean_data)

    def to_dict(self):
        data = super().to_dict()
        data.update({"name": self.name, "description": self.description})
        return data
