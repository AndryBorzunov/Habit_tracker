from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields ="__all__"

        def validate(self, data):
            award = data.get('award')
            habit_pleasant = data.get('habit_pleasant')
            if award and habit_pleasant:
                raise serializers.ValidationError(
                    "Нельзя заполнить и вознаграждение, и связанную привычку одновременно."
                )
            return data
