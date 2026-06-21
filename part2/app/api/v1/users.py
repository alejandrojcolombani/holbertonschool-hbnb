"""User API endpoints."""

from flask_restx import Namespace, Resource, fields

from app.services import facade

api = Namespace("users", description="User operations")

user_model = api.model(
    "User",
    {
        "first_name": fields.String(required=True, description="First name of the user"),
        "last_name": fields.String(required=True, description="Last name of the user"),
        "email": fields.String(required=True, description="Email of the user"),
    },
)

user_update_model = api.model(
    "UserUpdate",
    {
        "first_name": fields.String,
        "last_name": fields.String,
        "email": fields.String,
    },
)


def serialize_user(user):
    """Return the public user payload used by the API."""

    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }


@api.route("/")
class UserList(Resource):
    """Create and list users."""

    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Email already registered")
    @api.response(400, "Invalid input data")
    def post(self):
        """Register a new user."""

        try:
            user = facade.create_user(api.payload or {})
        except ValueError as exc:
            if str(exc) == "Email already registered":
                return {"error": str(exc)}, 400
            return {"error": "Invalid input data"}, 400
        return serialize_user(user), 201

    @api.response(200, "List of users retrieved successfully")
    def get(self):
        """Retrieve a list of all users."""

        return [serialize_user(user) for user in facade.get_all_users()], 200


@api.route("/<string:user_id>")
@api.param("user_id", "User identifier")
class UserResource(Resource):
    """Retrieve and update a user."""

    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    def get(self, user_id):
        """Get user details by ID."""

        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return serialize_user(user), 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, "User successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(404, "User not found")
    def put(self, user_id):
        """Update a user's information."""

        try:
            user = facade.update_user(user_id, api.payload or {})
        except ValueError as exc:
            if str(exc) == "Email already registered":
                return {"error": str(exc)}, 400
            return {"error": "Invalid input data"}, 400
        if not user:
            return {"error": "User not found"}, 404
        return serialize_user(user), 200
