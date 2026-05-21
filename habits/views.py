from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from habits.models import Habit
from habits.serializers import HabitSerializer


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            habit = serializer.save()
            habit.user = self.request.user
            habit.save()
            return Response(serializer.errors, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
