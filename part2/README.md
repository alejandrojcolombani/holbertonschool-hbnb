# HBnB - Business Logic and API

This project implements the presentation and business logic layers for the HBnB application using Flask and Flask-RESTx.

## Project Structure

- `app/`: Core application package.
- `app/api/v1/`: Versioned REST API endpoints for users, amenities, places, and reviews.
- `app/models/`: Business logic classes and validation for `User`, `Place`, `Review`, and `Amenity`.
- `app/services/`: Facade layer used by the API to interact with business logic and repositories.
- `app/persistence/`: In-memory repository implementation used before database persistence is added.
- `config.py`: Environment configuration.
- `run.py`: Flask entry point.
- `tests/`: Automated endpoint tests.

## Business Logic Layer

The model layer implements the core HBnB entities and their relationships:

- `User`: registered users and administrators. A user can own many places and write many reviews.
- `Place`: property listings with title, description, price, coordinates, owner, amenities, and reviews.
- `Amenity`: reusable place features such as Wi-Fi, parking, or pool access.
- `Review`: feedback written by a user for a place, with required text and a rating from 1 to 5.

All entities inherit from `BaseModel`, which provides a UUID string `id`, `created_at`, `updated_at`, `save()`, `update()`, and `to_dict()`.

Example:

```python
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.user import User

owner = User("Ada", "Lovelace", "ada@example.com")
wifi = Amenity("Wi-Fi")
place = Place(
    title="Cozy Apartment",
    description="A nice place to stay",
    price=100.0,
    latitude=37.7749,
    longitude=-122.4194,
    owner=owner,
    amenities=[wifi],
)
review = Review(text="Great stay!", rating=5, place=place, user=owner)
```

The API layer does not access models or repositories directly. It communicates through the singleton `HBnBFacade`, which coordinates the in-memory repositories and business objects.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python run.py
```

## Implemented Endpoints

- `POST /api/v1/users/`
- `GET /api/v1/users/`
- `GET /api/v1/users/<user_id>`
- `PUT /api/v1/users/<user_id>`
- `POST /api/v1/amenities/`
- `GET /api/v1/amenities/`
- `GET /api/v1/amenities/<amenity_id>`
- `PUT /api/v1/amenities/<amenity_id>`
- `POST /api/v1/places/`
- `GET /api/v1/places/`
- `GET /api/v1/places/<place_id>`
- `PUT /api/v1/places/<place_id>`
- `POST /api/v1/reviews/`
- `GET /api/v1/reviews/`
- `GET /api/v1/reviews/<review_id>`
- `PUT /api/v1/reviews/<review_id>`
- `DELETE /api/v1/reviews/<review_id>`
- `GET /api/v1/places/<place_id>/reviews`

## Tests

```bash
pytest
```
