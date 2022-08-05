from rest_framework.serializers import ModelSerializer
from base.models import Room, Tour

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class TourSerializer(ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'