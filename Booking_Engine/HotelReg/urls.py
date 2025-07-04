# hotel/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, RoomViewSet, BookingViewSet


router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'bookings', BookingViewSet)

hotel_router = DefaultRouter()
hotel_router.register(r'rooms', RoomViewSet, basename='hotel-rooms')

urlpatterns = [
    path('', include(router.urls)),
]
