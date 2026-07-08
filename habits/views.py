from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginators import HabitPagination
from habits.serializers import HabitSerializer
from habits.tasks import send_reminder
from users.permissions import IsOwner


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("user",)
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
            send_reminder.delay()
            return Response(serializer.errors, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            self.permission_classes = (IsOwner,)
        return super().get_permissions()
