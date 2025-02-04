from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import User, Room, Reservation
from .serializer import UserSerializer, RoomSerializer, ReservationSerializer, UserSerializerWithToken
import logging

logger = logging.getLogger(__name__)
# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# User Routes
@extend_schema(
    responses={
        200: UserSerializer(many=True),
    }
)
@api_view(['GET'])
def getUsers(request):
    users = User.objects.all().order_by('id')
    paginator = StandardResultsSetPagination()
    result_page = paginator.paginate_queryset(users, request)
    serializer = UserSerializerWithToken(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def getUser(request, pk):
    user = get_object_or_404(User, id=pk)
    serializer = UserSerializerWithToken(user)
    return Response(serializer.data)

@extend_schema(
    request=UserSerializer,
    responses={201: UserSerializer},
)
@api_view(['POST'])
def addUser(request):
    serializer = UserSerializer(data=request.data)
    serializer
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'auth_token': user.auth_token
        }, status=201)
    return Response(serializer.errors, status=400)

@extend_schema(
    request=UserSerializer,
    responses={201: UserSerializer},
)
@api_view(['PUT'])
def updateUser(request, pk):
    user = get_object_or_404(User, id=pk)
    serializer = UserSerializer(instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def deleteUser(request, pk):
    user = get_object_or_404(User, id=pk)
    user.delete()
    logger.info(f'Usuário {user.name} deletado.')

    return Response({'message': 'User deleted successfully'}, status=204)

# Room Routes
@extend_schema(
    request=RoomSerializer,
    responses={201: RoomSerializer},
)
@api_view(['POST'])
def addRoom(request):
    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info(f'Quarto {request.data['name']} criado.')

        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# Room Routes
@extend_schema(
    request=RoomSerializer,
    responses={201: RoomSerializer},
)
@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all().order_by('id')
    paginator = StandardResultsSetPagination()
    result_page = paginator.paginate_queryset(rooms, request)
    serializer = RoomSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def checkRoomAvailability(request, pk, start_time=None, end_time=None):
    room = get_object_or_404(Room, id=pk)
    
    if not start_time or not end_time:
        return Response({'error': 'start_time and end_time parameters are required'}, status=400)
    
    conflicts = Reservation.objects.filter(room=room, start_time__lt=end_time, end_time__gt=start_time).exists()

    return Response({'available': not conflicts})

# Reservation Routes
@extend_schema(
    request=ReservationSerializer,
    responses={201: ReservationSerializer},
)
@api_view(['POST'])
def addReservation(request):
    serializer = ReservationSerializer(data=request.data)
    if serializer.is_valid():
        room = get_object_or_404(Room, id=request.data['room'])
        user_name = request.data.get('user_name')
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']

        # Check if the room is available
        conflicts = Reservation.objects.filter(
            room=room, 
            start_time__lt=end_time, 
            end_time__gt=start_time
        ).exists()

        if conflicts:
            logger.warning(f'Usuário {user_name} tentou criar uma reserva, porém já existe reserva para o tempo.')

            return Response({'error': 'Room is already reserved for the given time slot'}, status=400)

        # Save the reservation with the extracted user_name
        reservation = Reservation.objects.create(
            room=room,
            user_name=user_name,
            start_time=start_time,
            end_time=end_time
        )
        logger.info(f'Reserva {reservation.id} criada por {user_name}')

        return Response(ReservationSerializer(reservation).data, status=201)
    logger.error(f'Erro ao cadastrar reserva: {serializer.errors}.')

    return Response(serializer.errors, status=400)


# Reservation Routes
@api_view(['DELETE'])
def cancelReservation(request, pk, token):
    reservation = get_object_or_404(Reservation, id=pk)
    try:
        user = User.objects.filter(auth_token = token)
    except:
        return Response({'error': 'Token invalid'}, status=403)

    if not user.exists():
        logger.warning(f'Token {token} não encontrado')
        return Response({'error': 'Token invalid'}, status=403)
    
    user = user.get()

    if reservation.user_name != user.name:
        logger.warning(f'Usuário {user.name} tentou cancelar uma reserva que não é dele.')
        return Response({'error': 'You can only cancel your own reservations'}, status=403)
    
    logger.info(f'Reserva {pk} cancelada por {user.name}')
    reservation.delete()
    return Response({'message': 'Reservation canceled successfully'}, status=204)

# Room Routes
@extend_schema(
    responses={201: ReservationSerializer},
)
@api_view(['GET'])
def getReservationsByRoom(request, pk):
    date_filter = request.GET.get('date')
    reservations = Reservation.objects.filter(room_id=pk)
    if date_filter:
        reservations = reservations.filter(start_time__date=date_filter)
    
    paginator = StandardResultsSetPagination()
    result_page = paginator.paginate_queryset(reservations, request)
    serializer = ReservationSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
