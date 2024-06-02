# hotel/serializers.py
from rest_framework import serializers
from .models import Hotel, Room, Booking

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'phone_number', 'bin', 'owner_name']
        read_only_fields = ['bin']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'room_type', 'price', 'is_available', 'current_booking']
    
    def create(self, validated_data):
        hotel_bin = validated_data.pop('hotel_bin')
        hotel = Hotel.objects.get(bin=hotel_bin)
        room_number = validated_data.get('room_number')

        # Check if the room with the same number already exists for the hotel
        if Room.objects.filter(hotel=hotel, room_number=room_number).exists():
            raise serializers.ValidationError("This room number already exists for the hotel.")

        room = Room.objects.create(hotel=hotel, **validated_data)
        return room

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['room', 'guest_name', 'check_in', 'check_out', 'is_active']
