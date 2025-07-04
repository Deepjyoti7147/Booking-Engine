### Make sure your server is running
```
python manage.py runserver

```

## API Endpoints

### Hotels

*   **`GET /api/hotels/`**: Retrieve a list of all hotels.
*   **`POST /api/hotels/`**: Create a new hotel.
*   **`GET /api/hotels/{id}/`**: Retrieve a specific hotel by its ID.
*   **`PUT /api/hotels/{id}/`**: Update a specific hotel.
*   **`DELETE /api/hotels/{id}/`**: Delete a specific hotel.

### Rooms

*   **`GET /api/rooms/`**: Retrieve a list of all rooms.
*   **`GET /api/rooms/?hotel_bin={hotel_bin}`**: Retrieve a list of rooms for a specific hotel.
*   **`POST /api/rooms/`**: Create a new room.
*   **`GET /api/rooms/{id}/`**: Retrieve a specific room by its ID.
*   **`PUT /api/rooms/{id}/`**: Update a specific room.
*   **`DELETE /api/rooms/{id}/`**: Delete a specific room.
*   **`GET /api/rooms/{id}/availability/?check_in={check_in}&check_out={check_out}`**: Check the availability of a specific room for a given date range.

### Bookings

*   **`GET /api/bookings/`**: Retrieve a list of all bookings.
*   **`POST /api/bookings/`**: Create a new booking.
*   **`GET /api/bookings/{id}/`**: Retrieve a specific booking by its ID.
*   **`PUT /api/bookings/{id}/`**: Update a specific booking.
*   **`DELETE /api/bookings/{id}/`**: Delete a specific booking.
*   **`POST /api/bookings/{id}/cancel/`**: Cancel a specific booking.

### Creating New Request in POSTMAN

```
Set Up the Request:

* Method: POST
* URL: http://127.0.0.1:8000/api/hotels/
* Headers: Content-Type: application/json



```

### Authentication

To authenticate with the API, you'll need to obtain an authentication token. You can do this by sending a POST request to the `/api-token-auth/` endpoint with your username and password.

```
* Method: POST
* URL: http://127.0.0.1:8000/api-token-auth/
* Body:
{
    "username": "your-username",
    "password": "your-password"
}
```

The API will respond with a token that you can use to authenticate subsequent requests. To authenticate, you'll need to include the token in the `Authorization` header of your requests.

```
* Headers:
    * Content-Type: application/json
    * Authorization: Token your-token
```
