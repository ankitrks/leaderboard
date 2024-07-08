from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status, views
from rest_framework.exceptions import ValidationError

from .models import User, Winner
from .serializers import (UserSerializer,
                            WinnerSerializer, PointsSerializer)
from drf_yasg.utils import swagger_auto_schema

from django.conf import settings
from django.core.files.storage import default_storage


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        users = User.objects.all().order_by('-points')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddPointsView(views.APIView):
    @swagger_auto_schema(request_body=PointsSerializer)
    def post(self, request, pk=None):
        serializer = PointsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        points = serializer.validated_data.get('points')

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.points += int(points)
        user.save()
        return Response({'status': 'points added', 'new_points': user.points}, status=status.HTTP_200_OK)

class SubtractPointsView(views.APIView):
    @swagger_auto_schema(request_body=PointsSerializer)
    def post(self, request, pk=None):
        serializer = PointsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        points = serializer.validated_data.get('points')

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.points -= int(points)
        user.save()
        return Response({'status': 'points subtracted', 'new_points': user.points}, status=status.HTTP_200_OK)

class WinnerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Winner.objects.all()
    serializer_class = WinnerSerializer

class GroupedUserView(viewsets.ViewSet):
    def list(self, request):
        grouped_data = {}
        users = User.objects.all()
        for user in users:
            if user.points not in grouped_data:
                grouped_data[user.points] = {
                    "average_age": 0,
                    "names": []
                }
            grouped_data[user.points]["names"].append(user.name)
            grouped_data[user.points]["average_age"] += user.age

        for points, data in grouped_data.items():
            data["average_age"] /= len(data["names"])

        return Response(grouped_data)
