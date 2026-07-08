from datetime import datetime, timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_reminder():
    """Отправка напоминаний о необходимости выполнить привычку"""
    filter_date = timezone.now()
    habits_now = Habit.objects.filter(time_action__lte=filter_date)
    for habit in habits_now:
        # print(f"{habit.user} : {habit.time_action} : {habit.place} : {habit.action}")
        user = habit.user
        if user.tg_nick:
            # print(f"{user} : {user.tg_nick}")
            send_telegram_message(user.tg_nick, "hello, habit")

        habit.time_action = datetime.combine(
            timezone.now().date() + timedelta(days=habit.periodicity),
            habit.time_action.time(),
        )
        habit.save()
        # print(f"new_time: {habit.time_action}")
