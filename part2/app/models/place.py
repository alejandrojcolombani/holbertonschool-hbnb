"""Place domain model."""

from app.models.base_model import BaseModel


class Place(BaseModel):
    """Property listing."""

    def __init__(
        self,
        title,
        price,
        latitude,
        longitude,
        owner,
        description="",
        amenities=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.amenities = []
        self.reviews = []

        if self not in owner.places:
            owner.places.append(self)
        for amenity in amenities or []:
            self.add_amenity(amenity)

    @staticmethod
    def _validate_title(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("title is required")
        value = value.strip()
        if len(value) > 100:
            raise ValueError("title must be 100 characters or fewer")
        return value

    @staticmethod
    def _validate_price(value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("price must be a number")
        if value < 0:
            raise ValueError("price must be positive")
        return float(value)

    @staticmethod
    def _validate_coordinate(value, field, minimum, maximum):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{field} must be a number")
        if value < minimum or value > maximum:
            raise ValueError(f"{field} must be between {minimum} and {maximum}")
        return float(value)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = self._validate_title(value)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value or ""

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = self._validate_price(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        self._latitude = self._validate_coordinate(value, "latitude", -90, 90)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        self._longitude = self._validate_coordinate(value, "longitude", -180, 180)

    @property
    def owner_id(self):
        return self.owner.id

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()

    def add_review(self, review):
        """Add a review to this place."""

        if review not in self.reviews:
            self.reviews.append(review)
            self.save()

    def update(self, data):
        clean_data = {}
        if "title" in data:
            clean_data["title"] = self._validate_title(data["title"])
        if "description" in data:
            clean_data["description"] = data["description"] or ""
        if "price" in data:
            clean_data["price"] = self._validate_price(data["price"])
        if "latitude" in data:
            clean_data["latitude"] = self._validate_coordinate(
                data["latitude"], "latitude", -90, 90
            )
        if "longitude" in data:
            clean_data["longitude"] = self._validate_coordinate(
                data["longitude"], "longitude", -180, 180
            )
        if "owner" in data:
            new_owner = data["owner"]
            if self in self.owner.places:
                self.owner.places.remove(self)
            if self not in new_owner.places:
                new_owner.places.append(self)
            clean_data["owner"] = new_owner
        if "amenities" in data:
            clean_data["amenities"] = []
            for amenity in data["amenities"]:
                if amenity not in clean_data["amenities"]:
                    clean_data["amenities"].append(amenity)
        super().update(clean_data)

    def to_dict(self, detailed=False):
        data = super().to_dict()
        data.update(
            {
                "title": self.title,
                "description": self.description,
                "price": self.price,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "owner_id": self.owner_id,
                "amenities": [amenity.to_dict() for amenity in self.amenities],
            }
        )
        if detailed:
            data["owner"] = {
                "id": self.owner.id,
                "first_name": self.owner.first_name,
                "last_name": self.owner.last_name,
                "email": self.owner.email,
            }
            data["reviews"] = [
                review.to_dict(include_place=False) for review in self.reviews
            ]
        return data
