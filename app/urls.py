from django.urls import path
from . import views

urlpatterns = [
    # User Routes
    path('users/', views.getUsers, name='get_users'),
    path('users/<int:pk>/', views.getUser, name='get_user'),
    path('users/create/', views.addUser, name='add_user'),
    path('users/update/<int:pk>/', views.updateUser, name='update_user'),
    path('users/delete/<int:pk>/', views.deleteUser, name='delete_user'),

    # Room Routes
    path('rooms/', views.getRooms, name='get_rooms'),
    path('rooms/create/', views.addRoom, name='add_room'),
    path('rooms/<int:pk>/availability/start_time=<str:start_time>&end_time=<str:end_time>', views.checkRoomAvailability, name='check_room_availability'),

    # Reservation Routes
    path('reservations/', views.addReservation, name='add_reservation'),
    path('reservations/<int:pk>/cancel/<str:token>', views.cancelReservation, name='cancel_reservation'),
    path('rooms/<int:pk>/reservations/', views.getReservationsByRoom, name='get_reservations_by_room'),
]
