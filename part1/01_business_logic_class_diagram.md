# Task 1: Detailed Class Diagram for Business Logic Layer

## Diagram

```mermaid
classDiagram
    class BaseModel {
        +UUID4 id
        +datetime created_at
        +datetime updated_at
        +save()
        +update()
        +delete()
    }

    class User {
        +string first_name
        +string last_name
        +string email
        +string password
        +boolean is_admin
        +register()
        +update_profile()
        +delete_user()
    }

    class Place {
        +string title
        +string description
        +float price
        +float latitude
        +float longitude
        +User owner
        +List~Amenity~ amenities
        +create_place()
        +update_place()
        +delete_place()
        +list_place()
    }

    class Review {
        +int rating
        +string comment
        +User user
        +Place place
        +create_review()
        +update_review()
        +delete_review()
        +list_by_place()
    }

    class Amenity {
        +string name
        +string description
        +create_amenity()
        +update_amenity()
        +delete_amenity()
        +list_amenities()
    }

    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity

    User "1" --> "0..*" Place : owns
    User "1" --> "0..*" Review : writes
    Place "1" --> "0..*" Review : receives
    Place "0..*" --> "0..*" Amenity : has
```

## Description

The BaseModel class contains attributes shared by all entities, including a UUID4 id, created_at, and updated_at. User, Place, Review, and Amenity inherit from BaseModel.

The User class represents registered users and administrators. A user can own many places and write many reviews.

The Place class represents a property listing. Each place belongs to one user and can receive many reviews. A place can also have many amenities.

The Review class represents feedback submitted by a user for a place. Each review belongs to one user and one place.

The Amenity class represents features that can be attached to places, such as WiFi, parking, or a pool. The relationship between Place and Amenity is many-to-many.
