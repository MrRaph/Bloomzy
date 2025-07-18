# User Plants API Documentation

## Overview
This API provides endpoints for managing user plants, including CRUD operations and watering history tracking.

## Authentication
All endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### My Plants Management

#### GET /api/plants/my-plants
Get all plants owned by the current user.

**Response:**
```json
{
  "plants": [
    {
      "id": 1,
      "user_id": 1,
      "species_id": 1,
      "custom_name": "My Beautiful Ficus",
      "location": "Living Room",
      "pot_size": "Medium",
      "soil_type": "Potting mix",
      "acquired_date": "2023-01-15",
      "current_photo_url": null,
      "health_status": "healthy",
      "notes": "Bought from local nursery",
      "light_exposure": "Bright indirect",
      "local_humidity": 65,
      "ambient_temperature": 22,
      "last_repotting": null,
      "created_at": "2023-01-15T10:30:00",
      "updated_at": "2023-01-15T10:30:00",
      "species": {
        "id": 1,
        "scientific_name": "Ficus benjamina",
        "common_names": "Weeping Fig",
        "family": "Moraceae"
      }
    }
  ],
  "total": 1
}
```

#### POST /api/plants/my-plants
Create a new plant for the current user.

**Request Body:**
```json
{
  "species_id": 1,
  "custom_name": "My Beautiful Ficus",
  "location": "Living Room",
  "pot_size": "Medium",
  "soil_type": "Potting mix",
  "acquired_date": "2023-01-15",
  "health_status": "healthy",
  "notes": "Bought from local nursery",
  "light_exposure": "Bright indirect",
  "local_humidity": 65,
  "ambient_temperature": 22,
  "last_repotting": "2023-01-15"
}
```

**Required fields:**
- `species_id` (integer): Must reference an existing plant species
- `custom_name` (string): Name for the plant (max 100 characters)

**Response:** Created plant object (201 Created)

#### GET /api/plants/my-plants/{id}
Get a specific plant by ID.

**Response:** Plant object (200 OK) or 404 if not found

#### PUT /api/plants/my-plants/{id}
Update a specific plant.

**Request Body:** Same fields as POST (all optional)

**Response:** Updated plant object (200 OK)

#### DELETE /api/plants/my-plants/{id}
Delete a specific plant and its watering history.

**Response:** Success message (200 OK)

### Plant Photos

#### POST /api/plants/my-plants/{id}/photo
Upload a photo for a specific plant.

**Request:** Multipart form data with `photo` file

**Supported formats:** JPG, JPEG, PNG, GIF

**Response:**
```json
{
  "message": "Photo uploaded successfully",
  "photo_url": "/uploads/plants/1_photo.jpg"
}
```

### Watering Management

#### POST /api/plants/watering
Record a watering event for a plant.

**Request Body:**
```json
{
  "plant_id": 1,
  "watered_at": "2023-01-15 10:30:00",
  "amount_ml": 250,
  "water_type": "filtered",
  "notes": "Regular watering"
}
```

**Required fields:**
- `plant_id` (integer): Must reference a plant owned by the user

**Optional fields:**
- `watered_at` (datetime): Defaults to current time
- `amount_ml` (integer): Water amount in milliliters (0-10000)
- `water_type` (string): Type of water (tap, filtered, rainwater, distilled, other)
- `notes` (string): Additional notes

**Response:** Created watering record (201 Created)

#### GET /api/plants/{plant_id}/watering-history
Get watering history for a specific plant.

**Response:**
```json
{
  "plant_id": 1,
  "watering_history": [
    {
      "id": 1,
      "plant_id": 1,
      "watered_at": "2023-01-15T10:30:00",
      "amount_ml": 250,
      "water_type": "filtered",
      "notes": "Regular watering",
      "created_at": "2023-01-15T10:30:00"
    }
  ],
  "total": 1
}
```

#### PUT /api/plants/watering/{watering_id}
Update a watering record.

**Request Body:** Same fields as POST watering (all optional)

**Response:** Updated watering record (200 OK)

## Data Validation

### UserPlant Validation
- `custom_name`: Required, max 100 characters
- `health_status`: Must be one of: healthy, sick, dying, dead
- `local_humidity`: 0-100 if provided
- `ambient_temperature`: -20 to 50 degrees if provided

### WateringHistory Validation
- `watered_at`: Required if provided
- `amount_ml`: 0-10000 if provided
- `water_type`: Must be one of: tap, filtered, rainwater, distilled, other

## Error Responses

All endpoints return appropriate HTTP status codes and error messages:

```json
{
  "error": "Error message",
  "details": ["Validation error 1", "Validation error 2"]
}
```

Common status codes:
- 400: Bad Request (validation errors, missing fields)
- 401: Unauthorized (invalid or missing JWT token)
- 404: Not Found (plant or resource not found)
- 500: Internal Server Error

## Models

### UserPlant
- Represents a plant owned by a user
- Links to plant species and includes personalized information
- Tracks health status and environmental conditions

### WateringHistory
- Records watering events for plants
- Includes amount, water type, and notes
- Ordered by watering date (newest first)

## Security
- All endpoints require JWT authentication
- Users can only access their own plants
- Plant ownership is validated on all operations
- Cross-user access is prevented