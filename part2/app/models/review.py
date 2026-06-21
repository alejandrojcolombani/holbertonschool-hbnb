"""Review domain model."""

from app.models.base_model import BaseModel


class Review(BaseModel):
    """User review for a place."""

    def __init__(self, rating, text=None, comment=None, place=None, user=None, **kwargs):
        super().__init__(**kwargs)
        self.place = place
        self.user = user
        self.rating = rating
        self.text = text if text is not None else comment

        place.add_review(self)
        if self not in user.reviews:
            user.reviews.append(self)

    @staticmethod
    def _validate_rating(value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("rating must be between 1 and 5")
        return value

    @staticmethod
    def _validate_text(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("text is required")
        return value.strip()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = self._validate_text(value)

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = self._validate_rating(value)

    @property
    def place_id(self):
        return self.place.id

    @property
    def user_id(self):
        return self.user.id

    @property
    def comment(self):
        return self.text

    @comment.setter
    def comment(self, value):
        self.text = self._validate_text(value)

    def update(self, data):
        clean_data = {}
        if "rating" in data:
            clean_data["rating"] = self._validate_rating(data["rating"])
        if "text" in data or "comment" in data:
            clean_data["text"] = self._validate_text(
                data.get("text", data.get("comment"))
            )
        super().update(clean_data)

    def to_dict(self, include_place=True):
        data = super().to_dict()
        data.update(
            {
                "rating": self.rating,
                "text": self.text,
                "comment": self.text,
                "user_id": self.user_id,
                "place_id": self.place_id,
            }
        )
        if include_place:
            data["place"] = {"id": self.place.id, "title": self.place.title}
        data["user"] = {
            "id": self.user.id,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
        }
        return data
