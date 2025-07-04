from django.test import TestCase
from django.utils import timezone
from .models import Hotel, Room, Booking
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class HotelModelTest(TestCase):
    def test_hotel_creation(self):
        hotel = Hotel.objects.create(
            name="Test Hotel",
            address="123 Test St",
            phone_number="1234567890",
            owner_name="Test Owner"
        )
        self.assertIsInstance(hotel, Hotel)
        self.assertEqual(hotel.name, "Test Hotel")
        self.assertIsNotNone(hotel.bin)

class RoomModelTest(TestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            address="123 Test St",
            phone_number="1234567890",
            owner_name="Test Owner"
        )

    def test_room_creation(self):
        room = Room.objects.create(
            hotel=self.hotel,
            room_number="101",
            room_type="Standard",
            price=100.00
        )
        self.assertIsInstance(room, Room)
        self.assertEqual(room.hotel, self.hotel)
        self.assertEqual(room.room_number, "101")

class BookingModelTest(TestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            address="123 Test St",
            phone_number="1234567890",
            owner_name="Test Owner"
        )
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number="101",
            room_type="Standard",
            price=100.00
        )

    def test_booking_creation(self):
        booking = Booking.objects.create(
            room=self.room,
            guest_name="Test Guest",
            guest_email="test@example.com",
            check_in=timezone.now(),
            check_out=timezone.now() + timezone.timedelta(days=1)
        )
        self.assertIsInstance(booking, Booking)
        self.assertEqual(booking.guest_name, "Test Guest")

    def test_booking_conflict(self):
        check_in_time = timezone.now() + timezone.timedelta(days=2)
        check_out_time = check_in_time + timezone.timedelta(days=1)

        Booking.objects.create(
            room=self.room,
            guest_name="First Guest",
            guest_email="first@example.com",
            check_in=check_in_time,
            check_out=check_out_time
        )

        with self.assertRaises(ValueError):
            Booking.objects.create(
                room=self.room,
                guest_name="Second Guest",
                guest_email="second@example.com",
                check_in=check_in_time,
                check_out=check_out_time
            )

class HotelViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            address="123 Test St",
            phone_number="1234567890",
            owner_name="Test Owner"
        )
        self.url = reverse('hotel-list')

    def test_get_hotels(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_hotel(self):
        data = {
            "name": "New Hotel",
            "address": "456 New St",
            "phone_number": "0987654321",
            "owner_name": "New Owner"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hotel.objects.count(), 2)

class RoomViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            address="123 Test St",
            phone_number="1234567890",
            owner_name="Test Owner"
        )
        self.url = reverse('room-list')

    def test_create_room(self):
        data = {
            "hotel_bin": self.hotel.bin,
            "room_number": "102",
            "room_type": "Deluxe",
            "price": 200.00
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 1)

    def test_list_rooms_by_hotel(self):
        Room.objects.create(hotel=self.hotel, room_number="101", room_type="Standard", price=100.00)
        response = self.client.get(self.url, {'hotel_bin': self.hotel.bin})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_room_availability(self):
        room = Room.objects.create(hotel=self.hotel, room_number="101", room_type="Standard", price=100.00)
        url = reverse('room-availability', kwargs={'pk': room.pk})
        check_in = timezone.now() + timezone.timedelta(days=1)
        check_out = check_in + timezone.timedelta(days=1)
        response = self.client.get(url, {'check_in': check_in.isoformat(), 'check_out': check_out.isoformat()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['available'])

        Booking.objects.create(
            room=room,
            guest_name="Test Guest",
            guest_email="test@example.com",
            check_in=check_in,
            check_out=check_out
        )

        response = self.client.get(url, {'check_in': check_in.isoformat(), 'check_out': check_out.isoformat()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['available'])

    def test_room_availability_invalid_dates(self):
        room = Room.objects.create(hotel=self.hotel, room_number="101", room_type="Standard", price=100.00)
        url = reverse('room-availability', kwargs={'pk': room.pk})
        response = self.client.get(url, {'check_in': 'invalid-date', 'check_out': 'invalid-date'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class BookingViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            address="123 Test St",
            phone_number="1234567890",
            owner_name="Test Owner"
        )
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number="101",
            room_type="Standard",
            price=100.00
        )
        self.url = reverse('booking-list')

    def test_create_booking(self):
        data = {
            "room": self.room.id,
            "guest_name": "Test Guest",
            "guest_email": "test@example.com",
            "check_in": timezone.now().isoformat(),
            "check_out": (timezone.now() + timezone.timedelta(days=1)).isoformat()
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

    def test_cancel_booking(self):
        booking = Booking.objects.create(
            room=self.room,
            guest_name="Test Guest",
            guest_email="test@example.com",
            check_in=timezone.now(),
            check_out=timezone.now() + timezone.timedelta(days=1)
        )
        url = reverse('booking-cancel', kwargs={'pk': booking.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        booking.refresh_from_db()
        self.assertFalse(booking.is_active)
