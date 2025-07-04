# hotel/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from .models import Hotel, Room, Booking
from .serializers import HotelSerializer, RoomSerializer, BookingSerializer
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


    def perform_create(self, serializer):
        hotel_bin = serializer.validated_data.pop('hotel_bin')
        try:
            hotel = Hotel.objects.get(bin=hotel_bin)
        except Hotel.DoesNotExist:
            raise ValidationError("Hotel with the provided bin does not exist.")
        
        room_number = serializer.validated_data.get('room_number')
        if Room.objects.filter(hotel=hotel, room_number=room_number).exists():
            raise ValidationError("This room number already exists for the hotel.")
        
        serializer.save(hotel=hotel)

    # Add a custom method to retrieve rooms by hotel
    def list(self, request, *args, **kwargs):
        hotel_bin = request.query_params.get('hotel_bin')
        if hotel_bin:
            queryset = self.get_queryset().filter(hotel__bin=hotel_bin)
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        room = self.get_object()
        check_in_str = request.query_params.get('check_in')
        check_out_str = request.query_params.get('check_out')

        if not check_in_str or not check_out_str:
            return Response({'error': 'Check-in and check-out dates are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            check_in = parse_datetime(check_in_str)
            check_out = parse_datetime(check_out_str)
        except ValueError:
            return Response({'error': 'Invalid date format.'}, status=status.HTTP_400_BAD_REQUEST)

        if not check_in or not check_out:
            return Response({'error': 'Invalid date format.'}, status=status.HTTP_400_BAD_REQUEST)

        conflicting_bookings = Booking.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in,
            is_active=True
        )

        if conflicting_bookings.exists():
            return Response({'available': False})
        else:
            return Response({'available': True})

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        room = serializer.validated_data['room']
        check_in = serializer.validated_data['check_in']
        check_out = serializer.validated_data['check_out']

        conflicting_bookings = Booking.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in,
            is_active=True
        )

        if conflicting_bookings.exists():
            raise ValidationError("Room is not available for the selected dates.")
        
        serializer.save()

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        booking.is_active = False
        booking.save()
        return Response({'status': 'booking cancelled'})
