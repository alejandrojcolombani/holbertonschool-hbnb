"""Review API endpoints."""

from flask_restx import Namespace, Resource, fields

from app.services import facade

api = Namespace("reviews", description="Review operations")

review_model = api.model(
    "Review",
    {
        "text": fields.String(required=True, description="Text of the review"),
        "rating": fields.Integer(
            required=True, description="Rating of the place (1-5)"
        ),
        "user_id": fields.String(required=True, description="ID of the user"),
        "place_id": fields.String(required=True, description="ID of the place"),
    },
)

review_update_model = api.model(
    "ReviewUpdate",
    {
        "rating": fields.Integer,
        "text": fields.String,
    },
)


def serialize_review(review, detailed=True):
    """Return a review payload matching the task examples."""

    data = {"id": review.id, "text": review.text, "rating": review.rating}
    if detailed:
        data["user_id"] = review.user.id
        data["place_id"] = review.place.id
    return data


@api.route("/")
class ReviewList(Resource):
    """Create and list reviews."""

    @api.expect(review_model, validate=True)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    @api.response(404, "Related resource not found")
    def post(self):
        """Register a new review."""

        try:
            review = facade.create_review(dict(api.payload or {}))
        except LookupError as exc:
            return {"error": "Invalid input data"}, 400
        except ValueError as exc:
            return {"error": "Invalid input data"}, 400
        return serialize_review(review), 201

    @api.response(200, "List of reviews retrieved successfully")
    def get(self):
        """Retrieve a list of all reviews."""

        return [serialize_review(review, detailed=False) for review in facade.get_all_reviews()], 200


@api.route("/<string:review_id>")
@api.param("review_id", "Review identifier")
class ReviewResource(Resource):
    """Retrieve, update, and delete a review."""

    @api.response(200, "Review details retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """Get review details by ID."""

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return serialize_review(review), 200

    @api.expect(review_update_model, validate=True)
    @api.response(200, "Review updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(404, "Review not found")
    def put(self, review_id):
        """Update a review's information."""

        try:
            review = facade.update_review(review_id, api.payload or {})
        except ValueError as exc:
            return {"error": "Invalid input data"}, 400
        if not review:
            return {"error": "Review not found"}, 404
        return {"message": "Review updated successfully"}, 200

    @api.response(200, "Review successfully deleted")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        """Delete a review."""

        if not facade.delete_review(review_id):
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted successfully"}, 200
