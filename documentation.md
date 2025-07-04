# Booking Engine API Documentation

This document provides documentation for the Booking Engine API.

## Authentication

To authenticate with the API, you need to obtain an authentication token. You can do this by sending a POST request to the `/api-token-auth/` endpoint with your username and password.

### Request

```
POST /api-token-auth/
{
    "username": "your-username",
    "password": "your-password"
}
```

### Response

```
{
    "token": "your-auth-token"
}
```

Once you have the token, you need to include it in the `Authorization` header of your requests.

```
Authorization: Token your-auth-token
```

## API Endpoints

### Hotels

- `GET /api/hotels/`: Get a list of all hotels.
- `POST /api/hotels/`: Create a new hotel.
- `GET /api/hotels/{id}/`: Get details of a specific hotel.
- `PUT /api/hotels/{id}/`: Update a specific hotel.
- `DELETE /api/hotels/{id}/`: Delete a specific hotel.

### Rooms

- `GET /api/rooms/`: Get a list of all rooms.
- `GET /api/rooms/?hotel_bin={hotel_bin}`: Get a list of rooms for a specific hotel.
- `POST /api/rooms/`: Create a new room.
- `GET /api/rooms/{id}/`: Get details of a specific room.
- `PUT /api/rooms/{id}/`: Update a specific room.
- `DELETE /api/rooms/{id}/`: Delete a specific room.
- `GET /api/rooms/{id}/availability/?check_in={check_in}&check_out={check_out}`: Check the availability of a room for a given date range.

### Bookings

- `GET /api/bookings/`: Get a list of all bookings.
- `POST /api/bookings/`: Create a new booking.
- `GET /api/bookings/{id}/`: Get details of a specific booking.
- `PUT /api/bookings/{id}/`: Update a specific booking.
- `DELETE /api/bookings/{id}/`: Delete a specific booking.
- `POST /api/bookings/{id}/cancel/`: Cancel a specific booking.
