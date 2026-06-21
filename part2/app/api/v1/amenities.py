"""Amenity API endpoints."""

from flask_restx import Namespace, Resource, fields

from app.services import facade

api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model(
    "Amenity",
    {
        "name": fields.String(required=True, description="Name of the amenity"),
    },
)

amenity_update_model = api.model(
    "AmenityUpdate",
    {
        "name": fields.String,
    },
)


def serialize_amenity(amenity):
    """Return the amenity payload used by the API."""

    return {"id": amenity.id, "name": amenity.name}


@api.route("/")
class AmenityList(Resource):
    """Create and list amenities."""

    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Register a new amenity."""

        try:
            amenity = facade.create_amenity(api.payload or {})
        except ValueError as exc:
            return {"error": "Invalid input data"}, 400
        return serialize_amenity(amenity), 201

    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        """Retrieve a list of all amenities."""

        return [serialize_amenity(amenity) for amenity in facade.get_all_amenities()], 200


@api.route("/<string:amenity_id>")
@api.param("amenity_id", "Amenity identifier")
class AmenityResource(Resource):
    """Retrieve and update an amenity."""

    @api.response(200, "Amenity details retrieved successfully")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        """Get amenity details by ID."""

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return serialize_amenity(amenity), 200

    @api.expect(amenity_update_model, validate=True)
    @api.response(200, "Amenity updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(404, "Amenity not found")
    def put(self, amenity_id):
        """Update an amenity's information."""

        try:
            amenity = facade.update_amenity(amenity_id, api.payload or {})
        except ValueError as exc:
            return {"error": "Invalid input data"}, 400
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return {"message": "Amenity updated successfully"}, 200
