"""Flask application factory."""


def create_app(config_name="default"):
    """Create and configure the Flask application."""

    from flask import Flask
    from flask_restx import Api

    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.users import api as users_ns
    from app.services import facade
    from config import config

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    api = Api(
        app,
        title="HBnB API",
        version="1.0",
        description="HBnB Business Logic and API",
        doc="/api/v1/",
    )
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")

    if app.config.get("TESTING"):
        facade.reset()

    return app
