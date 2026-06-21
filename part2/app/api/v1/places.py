"""Place API endpoints."""

from flask_restx import Namespace, Resource, fields

from app.services import facade

api = Namespace("places", description="Place operations")

amenity_model = api.model(
    "PlaceAmenity",
    {
        "id": fields.String(description="Amenity ID"),
        "name": fields.String(description="Name of the amenity"),
    },
)

user_model = api.model(
    "PlaceUser",
    {
        "id": fields.String(description="User ID"),
        "first_name": fields.String(description="First name of the owner"),
        "last_name": fields.String(description="Last name of the owner"),
        "email": fields.String(description="Email of the owner"),
    },
)

review_model = api.model(
    "PlaceReview",
    {
        "id": fields.String(description="Review ID"),
        "text": fields.String(description="Text of the review"),
        "rating": fields.Integer(description="Rating of the place (1-5)"),
        "user_id": fields.String(description="ID of the user"),
    },
)

place_model = api.model(
    "Place",
    {
        "title": fields.String(required=True, description="Title of the place"),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(required=True, description="Price per night"),
        "latitude": fields.Float(required=True, description="Latitude of the place"),
        "longitude": fields.Float(required=True, description="Longitude of the place"),
        "owner_id": fields.String(description="ID of the owner"),
        "owner": fields.Nested(user_model, description="Owner of the place"),
        "amenities": fields.List(
            fields.Nested(amenity_model), description="List of amenities"
        ),
        "reviews": fields.List(fields.Nested(review_model), description="List of reviews"),
    },
)

place_input_model = api.model(
    "PlaceInput",
    {
        "title": fields.String(required=True, description="Title of the place"),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(required=True, description="Price per night"),
        "latitude": fields.Float(required=True, description="Latitude of the place"),
        "longitude": fields.Float(required=True, description="Longitude of the place"),
        "owner_id": fields.String(required=True, description="ID of the owner"),
        "amenities": fields.List(
            fields.String, required=False, description="List of amenity IDs"
        ),
    },
)

place_update_model = api.model(
    "PlaceUpdate",
    {
        "title": fields.String,
        "description": fields.String,
        "price": fields.Float,
        "latitude": fields.Float,
        "longitude": fields.Float,
        "owner_id": fields.String,
        "amenities": fields.List(fields.String),
    },
)


def serialize_amenity(amenity):
    """Return the amenity shape nested in a place."""

    return {"id": amenity.id, "name": amenity.name}


def serialize_owner(owner):
    """Return the owner shape nested in a place."""

    return {
        "id": owner.id,
        "first_name": owner.first_name,
        "last_name": owner.last_name,
        "email": owner.email,
    }


def serialize_review(review, detailed=False):
    """Return a review payload for place responses."""

    data = {"id": review.id, "text": review.text, "rating": review.rating}
    if detailed:
        data["user_id"] = review.user.id
    return data


def serialize_place_created(place):
    """Return the place payload used after creation."""

    return {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner_id": place.owner.id,
    }


def serialize_place_summary(place):
    """Return the place payload used in list responses."""

    return {
        "id": place.id,
        "title": place.title,
        "latitude": place.latitude,
        "longitude": place.longitude,
    }


def serialize_place_detail(place):
    """Return a place with owner, amenities, and reviews."""

    return {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner": serialize_owner(place.owner),
        "amenities": [serialize_amenity(amenity) for amenity in place.amenities],
        "reviews": [serialize_review(review, detailed=True) for review in place.reviews],
    }


@api.route("/")
class PlaceList(Resource):
    """Create and list places."""

    @api.expect(place_input_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @api.response(404, "Related resource not found")
    def post(self):
        """Register a new place."""

        try:
            place = facade.create_place(dict(api.payload or {}))
        except LookupError as exc:
            return {"error": "Invalid input data"}, 400
        except ValueError as exc:
            return {"error": "Invalid input data"}, 400
        return serialize_place_created(place), 201

    @api.response(200, "List of places retrieved successfully")
    def get(self):
        """Retrieve a list of all places."""

        return [serialize_place_summary(place) for place in facade.get_all_places()], 200


@api.route("/<string:place_id>")
@api.param("place_id", "Place identifier")
class PlaceResource(Resource):
    """Retrieve and update a place."""

    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get place details by ID."""

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return serialize_place_detail(place), 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, "Place updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(404, "Resource not found")
    def put(self, place_id):
        """Update a place's information."""

        try:
            place = facade.update_place(place_id, dict(api.payload or {}))
        except LookupError as exc:
            return {"error": "Invalid input data"}, 400
        except ValueError as exc:
            return {"error": "Invalid input data"}, 400
        if not place:
            return {"error": "Place not found"}, 404
        return {"message": "Place updated successfully"}, 200


@api.route("/<string:place_id>/reviews")
@api.param("place_id", "Place identifier")
class PlaceReviewList(Resource):
    """List reviews for a place."""

    @api.response(200, "List of reviews for the place retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get all reviews for a specific place."""

        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {"error": "Place not found"}, 404
        return [serialize_review(review) for review in reviews], 200
