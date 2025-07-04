# hotel/serializers.py
from rest_framework import serializers
from .models import Hotel, Room, Booking

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'phone_number', 'bin', 'owner_name']
        read_only_fields = ['bin']

class RoomSerializer(serializers.ModelSerializer):
    hotel_bin = serializers.CharField(write_only=True)
    class Meta:
        model = Room
        fields = ['id', 'hotel_bin', 'room_number', 'room_type', 'price']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'room', 'guest_name', 'guest_email', 'check_in', 'check_out', 'created_at', 'is_active']
        read_only_fields = ['created_at']
