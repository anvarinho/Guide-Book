from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room, Tour
from .serializers import RoomSerializer, TourSerializer

@api_view(['GET', 'POST', 'PUT'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/places',
        'GET /api/places/:id',
        'GET /api/tours',
        'GET /api/tours/:id',
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms=Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room=Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getTours(request):
    rooms=Tour.objects.all()
    serializer = TourSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTour(request, pk):
    room=Tour.objects.get(id=pk)
    serializer = TourSerializer(room, many=False)
    return Response(serializer.data)