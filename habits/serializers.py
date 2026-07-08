from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):
        # Если метод — PATCH, пропускаем валидацию
        if self.context["request"].method == "PATCH":
            return data

        award = data.get("award")
        habit_pleasant = data.get("habit_pleasant")
        durations = data.get("durations")
        is_pleasant = data.get("is_pleasant")
        periodicity = data.get("periodicity")

        if is_pleasant:
            if award or habit_pleasant:
                raise serializers.ValidationError(
                    "У приятной привычки не должно быть вознаграждения или связанной привычки."
                )
        else:
            if not award and not habit_pleasant:
                raise serializers.ValidationError(
                    "Хотя бы одно из поле должно быть заполнено."
                )

            if award and habit_pleasant:
                raise serializers.ValidationError(
                    "Нельзя заполнить и вознаграждение, и связанную привычку одновременно."
                )

        if durations:
            if durations > 120:
                raise serializers.ValidationError(
                    "Время выполнения должно быть не более 120 секунд."
                )

        if habit_pleasant:
            # print(habit_pleasant.is_pleasant)
            if not habit_pleasant.is_pleasant:
                raise serializers.ValidationError(
                    "В связанные привычки могут попадать только привычки с признаком приятной привычки."
                )

        if periodicity:
            if periodicity > 7:
                raise serializers.ValidationError(
                    "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
                )

        return data
