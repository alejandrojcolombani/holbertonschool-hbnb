"""API tests for HBnB Part 2."""

import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app("testing")
    return app.test_client()


def create_user(client, email="ada@example.com"):
    response = client.post(
        "/api/v1/users/",
        json={
            "first_name": "Ada",
            "last_name": "Lovelace",
            "email": email,
        },
    )
    assert response.status_code == 201
    return response.get_json()


def create_amenity(client, name="WiFi"):
    response = client.post("/api/v1/amenities/", json={"name": name})
    assert response.status_code == 201
    return response.get_json()


def create_place(client, email="ada@example.com", amenity_name="WiFi"):
    user = create_user(client, email=email)
    amenity = create_amenity(client, name=amenity_name)
    response = client.post(
        "/api/v1/places/",
        json={
            "title": "Beach House",
            "description": "Ocean view",
            "price": 125.0,
            "latitude": 18.4655,
            "longitude": -66.1057,
            "owner_id": user["id"],
            "amenities": [amenity["id"]],
        },
    )
    assert response.status_code == 201
    return response.get_json(), user


def test_user_crud_and_email_uniqueness(client):
    user = create_user(client)
    assert "password" not in user
    assert "is_admin" not in user

    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert len(response.get_json()) == 1

    response = client.get(f"/api/v1/users/{user['id']}")
    assert response.status_code == 200
    assert response.get_json()["email"] == user["email"]

    response = client.get("/api/v1/users/not-found")
    assert response.status_code == 404

    duplicate = client.post(
        "/api/v1/users/",
        json={"first_name": "Grace", "last_name": "Hopper", "email": user["email"]},
    )
    assert duplicate.status_code == 400

    response = client.put(
        f"/api/v1/users/{user['id']}",
        json={"first_name": "Augusta"},
    )
    assert response.status_code == 200
    assert response.get_json()["first_name"] == "Augusta"

    response = client.put(
        "/api/v1/users/not-found",
        json={"first_name": "Nobody", "last_name": "Here", "email": "no@one.com"},
    )
    assert response.status_code == 404


def test_amenity_crud(client):
    amenity = create_amenity(client)
    response = client.get("/api/v1/amenities/")
    assert response.status_code == 200
    assert len(response.get_json()) == 1

    response = client.get(f"/api/v1/amenities/{amenity['id']}")
    assert response.status_code == 200
    assert response.get_json()["name"] == "WiFi"

    response = client.put(f"/api/v1/amenities/{amenity['id']}", json={"name": "Pool"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Amenity updated successfully"}

    response = client.get("/api/v1/amenities/not-found")
    assert response.status_code == 404

    response = client.put("/api/v1/amenities/not-found", json={"name": "Pool"})
    assert response.status_code == 404

    response = client.post("/api/v1/amenities/", json={"name": ""})
    assert response.status_code == 400


def test_place_crud_and_nested_serialization(client):
    place, user = create_place(client, email="review-owner@example.com")

    response = client.get("/api/v1/places/")
    assert response.status_code == 200
    assert response.get_json()[0]["title"] == "Beach House"

    response = client.get(f"/api/v1/places/{place['id']}")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["owner"]["id"] == user["id"]
    assert payload["amenities"][0]["name"] == "WiFi"

    response = client.put(f"/api/v1/places/{place['id']}", json={"price": 150})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Place updated successfully"}

    response = client.get("/api/v1/places/not-found")
    assert response.status_code == 404

    response = client.put("/api/v1/places/not-found", json={"price": 150})
    assert response.status_code == 404

    response = client.post(
        "/api/v1/places/",
        json={
            "title": "Ghost House",
            "price": 50.0,
            "latitude": 0.0,
            "longitude": 0.0,
            "owner_id": "not-found",
        },
    )
    assert response.status_code == 400


def test_review_crud_and_place_reviews(client):
    place, user = create_place(
        client,
        email="validation-owner@example.com",
        amenity_name="Validation WiFi",
    )
    response = client.post(
        "/api/v1/reviews/",
        json={
            "rating": 5,
            "text": "Excellent stay",
            "place_id": place["id"],
            "user_id": user["id"],
        },
    )
    assert response.status_code == 201
    review = response.get_json()

    response = client.get("/api/v1/reviews/")
    assert response.status_code == 200
    assert response.get_json()[0]["text"] == "Excellent stay"

    response = client.get(f"/api/v1/reviews/{review['id']}")
    assert response.status_code == 200
    assert response.get_json()["place_id"] == place["id"]

    response = client.get(f"/api/v1/places/{place['id']}/reviews")
    assert response.status_code == 200
    assert len(response.get_json()) == 1

    response = client.put(f"/api/v1/reviews/{review['id']}", json={"rating": 4})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Review updated successfully"}

    response = client.put("/api/v1/reviews/not-found", json={"rating": 4})
    assert response.status_code == 404

    response = client.delete(f"/api/v1/reviews/{review['id']}")
    assert response.status_code == 200

    response = client.get(f"/api/v1/reviews/{review['id']}")
    assert response.status_code == 404

    response = client.delete("/api/v1/reviews/not-found")
    assert response.status_code == 404

    response = client.get("/api/v1/places/not-found/reviews")
    assert response.status_code == 404


def test_validation_errors(client):
    response = client.post(
        "/api/v1/users/",
        json={"first_name": "", "last_name": "", "email": "invalid-email"},
    )
    assert response.status_code == 400

    user = create_user(client)
    response = client.post(
        "/api/v1/places/",
        json={
            "title": "Invalid Place",
            "price": -1,
            "latitude": 91,
            "longitude": 0,
            "owner_id": user["id"],
        },
    )
    assert response.status_code == 400

    place, user = create_place(
        client,
        email="validation-place-owner@example.com",
        amenity_name="Validation Place WiFi",
    )
    invalid_review_payloads = [
        {"rating": 6, "text": "Too high", "place_id": place["id"], "user_id": user["id"]},
        {"rating": 0, "text": "Too low", "place_id": place["id"], "user_id": user["id"]},
        {"rating": 5, "text": "", "place_id": place["id"], "user_id": user["id"]},
        {"rating": 5, "text": "Bad user", "place_id": place["id"], "user_id": "bad"},
        {"rating": 5, "text": "Bad place", "place_id": "bad", "user_id": user["id"]},
    ]
    for payload in invalid_review_payloads:
        response = client.post("/api/v1/reviews/", json=payload)
        assert response.status_code == 400


def test_delete_only_supported_for_reviews(client):
    user = create_user(client)
    amenity = create_amenity(client)
    place, _ = create_place(
        client,
        email="delete-owner@example.com",
        amenity_name="Delete WiFi",
    )

    assert client.delete(f"/api/v1/users/{user['id']}").status_code == 405
    assert client.delete(f"/api/v1/amenities/{amenity['id']}").status_code == 405
    assert client.delete(f"/api/v1/places/{place['id']}").status_code == 405
