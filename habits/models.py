from django.db import models

from users.models import User


class Habit(models.Model):
    """Модель привычка"""

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
        related_name="habits",
    )

    place = models.CharField(
        max_length=128,
        verbose_name="Место выполнения",
        help_text="Укажите место выполнения",
    )

    time_action = models.TimeField(
        verbose_name="Время выполнения", help_text="Укажите время выполнения"
    )

    action = models.CharField(
        max_length=256, verbose_name="Действие", help_text="Укажите действие"
    )

    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Приятная привычка",
        help_text="Укажите, если привычка приятная",
    )

    periodicity = models.IntegerField(
        default=1,
        verbose_name="Периодичность выполнения в днях",
        help_text="Укажите периодичность выполнения в днях",
    )

    habit_pleasant = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children",
        verbose_name="Связанная привычка",
        help_text="Укажите связанную привычку",
    )

    award = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text="Укажите вознаграждение",
    )

    durations = models.IntegerField(
        default=120,
        verbose_name="Продолжительность выполнения привычки в секундах",
        help_text="Укажите продолжительность выполнения привычки в секундах",
    )

    is_public = models.BooleanField(
        default=False, verbose_name="Публичность", help_text="Укажите публичность"
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
