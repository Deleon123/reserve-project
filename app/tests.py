from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User, Room, Reservation
from datetime import timedelta
from django.utils import timezone

class APITestCases(APITestCase):
    def setUp(self):
        """Create initial test data"""
        self.user = User.objects.create(name="João da Silva", email="joao@gmail.com")
        self.room = Room.objects.create(name="Sala A", capacity=10, location="Andar 1")
        self.reservation = Reservation.objects.create(
            room=self.room,
            user_name=self.user.name,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=2)
        )
    
    def test_get_users(self):
        url = reverse('get_users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_user(self):
        url = reverse('get_user', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_user(self):
        url = reverse('add_user')
        data = {"name": "Pedro I", "email": "pedro@hotmail.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_user(self):
        url = reverse('update_user', args=[self.user.id])
        data = {"name": "Pedro II", "email": "pedro@hotmail.com"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        url = reverse('delete_user', args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_get_rooms(self):
        url = reverse('get_rooms')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_room(self):
        url = reverse('add_room')
        data = {"name": "Meeting Room", "capacity": 5, "location": "2nd Floor"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_check_room_availability(self):
        url = reverse('check_room_availability', args=[self.room.id])
        params = {"start_time": timezone.now() + timedelta(days=1, hours=5), "end_time": timezone.now() + timedelta(days=1, hours=7)}
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_add_reservation(self):
        url = reverse('add_reservation')
        data = {
            "room": self.room.id,
            "user_name": self.user.name,
            "start_time": "2025-02-02 17:00:00",
            "end_time": "2025-02-02 18:00:00"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_cancel_reservation(self):
        url = reverse('cancel_reservation', args=[self.reservation.id, self.user.auth_token])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
