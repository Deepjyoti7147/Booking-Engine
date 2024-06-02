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

room_router = DefaultRouter()
room_router.register(r'bookings', BookingViewSet, basename='room-bookings')

urlpatterns = [
    path('', include(router.urls)),
    path('hotels/<int:hotel_pk>/', include(hotel_router.urls)),
    path('rooms/<int:room_pk>/', include(room_router.urls)),
]
