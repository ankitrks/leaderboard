from rest_framework import serializers
from .models import User, Winner

class UserSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False, allow_empty_file=True, use_url=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'age', 'points', 'address', 'photo']

class PointsSerializer(serializers.Serializer):
    points = serializers.IntegerField()

class WinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Winner
        fields = ['user', 'timestamp', 'points']
