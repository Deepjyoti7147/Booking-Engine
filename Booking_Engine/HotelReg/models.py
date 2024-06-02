# hotel/models.py
from django.db import models
from django.utils import timezone

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    bin = models.CharField(max_length=100, unique=True)
    owner_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.bin:
            self.bin = self.generate_bin()
        super().save(*args, **kwargs)

    def generate_bin(self):
        import uuid
        return str(uuid.uuid4())

class Room(models.Model):
    hotel = models.ForeignKey('Hotel', related_name='rooms', on_delete=models.CASCADE, to_field='bin')
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    current_booking = models.OneToOneField('Booking', related_name='room_booking', null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        unique_together = ('hotel', 'room_number')

    def __str__(self):
        return f'{self.hotel.name} - Room {self.room_number}'

class Booking(models.Model):
    room = models.ForeignKey(Room, related_name='bookings', on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=255)
    guest_email = models.EmailField()
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.guest_name} - {self.room.room_number}'

    def save(self, *args, **kwargs):
        if self.room.current_booking is None or self.check_in > self.room.current_booking.check_out:
            super().save(*args, **kwargs)
            self.room.current_booking = self
            self.room.is_available = False
            self.room.save()
        else:
            raise ValueError("The room is already booked for the selected dates.")

    def delete(self, *args, **kwargs):
        room = self.room
        super().delete(*args, **kwargs)
        if room.current_booking == self:
            room.current_booking = None
            room.is_available = True
            room.save()
