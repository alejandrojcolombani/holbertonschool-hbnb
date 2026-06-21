"""Facade between the API and business logic layers."""

from app.models import Amenity, Place, Review, User
from app.persistence import InMemoryRepository


class HBnBFacade:
    """Coordinate business logic and persistence operations."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all in-memory repositories."""

        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        email = user_data.get("email", "")
        if self.user_repo.get_by_attribute("email", email.strip().lower()):
            raise ValueError("Email already registered")
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email.strip().lower())

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None
        if "email" in user_data:
            existing = self.get_user_by_email(user_data["email"])
            if existing and existing.id != user_id:
                raise ValueError("Email already registered")
        user.update(user_data)
        return user

    def create_amenity(self, amenity_data):
        existing = self.amenity_repo.get_by_attribute(
            "name", amenity_data.get("name", "").strip()
        )
        if existing:
            raise ValueError("Amenity already exists")
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        if "name" in amenity_data:
            existing = self.amenity_repo.get_by_attribute(
                "name", amenity_data["name"].strip()
            )
            if existing and existing.id != amenity_id:
                raise ValueError("Amenity already exists")
        amenity.update(amenity_data)
        return amenity

    def _resolve_amenities(self, amenity_ids):
        amenities = []
        for amenity_id in amenity_ids or []:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise LookupError("Amenity not found")
            amenities.append(amenity)
        return amenities

    def create_place(self, place_data):
        owner = self.get_user(place_data.get("owner_id"))
        if not owner:
            raise LookupError("Owner not found")

        amenity_ids = place_data.pop("amenities", place_data.pop("amenity_ids", []))
        amenities = self._resolve_amenities(amenity_ids)
        place = Place(owner=owner, amenities=amenities, **place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None

        clean_data = dict(place_data)
        if "owner_id" in clean_data:
            owner = self.get_user(clean_data.pop("owner_id"))
            if not owner:
                raise LookupError("Owner not found")
            clean_data["owner"] = owner
        if "amenities" in clean_data or "amenity_ids" in clean_data:
            amenity_ids = clean_data.pop("amenities", clean_data.pop("amenity_ids", []))
            clean_data["amenities"] = self._resolve_amenities(amenity_ids)
        place.update(clean_data)
        return place

    def create_review(self, review_data):
        place = self.get_place(review_data.get("place_id"))
        if not place:
            raise LookupError("Place not found")
        user = self.get_user(review_data.get("user_id"))
        if not user:
            raise LookupError("User not found")

        payload = dict(review_data)
        payload.pop("place_id", None)
        payload.pop("user_id", None)
        review = Review(place=place, user=user, **payload)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return None
        return list(place.reviews)

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False
        if review in review.place.reviews:
            review.place.reviews.remove(review)
        if review in review.user.reviews:
            review.user.reviews.remove(review)
        return self.review_repo.delete(review_id)


facade = HBnBFacade()
