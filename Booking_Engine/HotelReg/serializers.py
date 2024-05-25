from rest_framework import serializers
from .models import Hotel

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'phone_number', 'bin', 'owner_name', 'owner_email']
        read_only_fields = ['bin']
