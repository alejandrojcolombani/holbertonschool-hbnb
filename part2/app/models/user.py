"""User domain model."""

import re

from app.models.base_model import BaseModel


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User(BaseModel):
    """Application user."""

    def __init__(
        self,
        first_name,
        last_name,
        email,
        password=None,
        is_admin=False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = bool(is_admin)
        self.places = []
        self.reviews = []

    @staticmethod
    def _validate_name(value, field):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} is required")
        value = value.strip()
        if len(value) > 50:
            raise ValueError(f"{field} must be 50 characters or fewer")
        return value

    @staticmethod
    def _validate_email(value):
        if not isinstance(value, str) or not EMAIL_PATTERN.match(value.strip()):
            raise ValueError("Invalid email")
        return value.strip().lower()

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = self._validate_name(value, "first_name")

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = self._validate_name(value, "last_name")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = self._validate_email(value)

    def update(self, data):
        clean_data = {}
        if "first_name" in data:
            clean_data["first_name"] = self._validate_name(
                data["first_name"], "first_name"
            )
        if "last_name" in data:
            clean_data["last_name"] = self._validate_name(data["last_name"], "last_name")
        if "email" in data:
            clean_data["email"] = self._validate_email(data["email"])
        if "password" in data:
            clean_data["password"] = data["password"]
        if "is_admin" in data:
            clean_data["is_admin"] = bool(data["is_admin"])
        super().update(clean_data)

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "is_admin": self.is_admin,
            }
        )
        return data
