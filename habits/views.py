from django.db.models import Q
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from habits.models import Habit
from habits.serializers import HabitSerializer
from habits.paginators import HabitPagination
from users.permissions import IsOwner


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPagination


    def get_queryset(self):
        user = self.request.user

        queryset = Habit.objects.filter(Q(user=user) | Q(is_public=True))
        return queryset


    def perform_create(self, serializer):
        if serializer.is_valid():
            habit = serializer.save()
            habit.user = self.request.user
            habit.save()
            return Response(serializer.errors, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_permissions(self):
        if self.action in ["retrieve", "update", 'partial_update', "destroy"]:
            self.permission_classes = (IsOwner,)
        return super().get_permissions()
