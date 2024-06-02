# hotel/views.py
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from .models import Hotel, Room, Booking
from .serializers import HotelSerializer, RoomSerializer, BookingSerializer
from rest_framework.response import Response

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_update(self, serializer):
        bin = self.request.data.get('hotel_bin')  # Assuming 'hotel_bin' is passed in the request data
        hotel = Hotel.objects.get(bin=bin)
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

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

'''    def perform_create(self, serializer):
        room = serializer.validated_data['room']
        if room.is_available:
            serializer.save()
        else:
            raise ValidationError("Room is not available for booking.")
'''