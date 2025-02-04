from rest_framework import serializers
from .models import User, Room, Reservation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']

class UserSerializerWithToken(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'auth_token']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'capacity', 'location']

class ReservationSerializer(serializers.ModelSerializer):
    room_name = serializers.ReadOnlyField(source='room.name')

    class Meta:
        model = Reservation
        fields = ['id', 'room', 'room_name', 'user_name', 'start_time', 'end_time']

    def validate(self, data):
        """Ensure start_time is before end_time."""
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time.")
        return data

