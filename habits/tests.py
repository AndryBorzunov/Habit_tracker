from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.habit = Habit.objects.create(
            user=self.user,
            time_action="2026-06-09T10:15:00",
            action="попрыгать",
            place="дома",
            award="полежать на полу",
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("user"), self.user.pk)

    def test_habit_create(self):
        url = reverse("habits:habit-list")
        data = {
            "user": self.user.pk,
            "place": "дома",
            "time_action": "2026-06-10T09:30",
            "action": "повисеть на турнике",
            "award": "выпить сок",
            "periodicity": 2,
        }
        response = self.client.post(url, data)
        resp = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Habit.objects.all().count(), 2)

        self.assertEqual(resp.get("time_action"), "2026-06-10T09:30:00")

    def test_habit_update(self):
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        data = {"is_public": True}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("is_public"), True)

    def test_habit_delete(self):
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_habit_list(self):
        url = reverse("habits:habit-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "place": self.habit.place,
                    "time_action": self.habit.time_action,
                    "action": self.habit.action,
                    "is_pleasant": self.habit.is_pleasant,
                    "periodicity": self.habit.periodicity,
                    "award": self.habit.award,
                    "durations": self.habit.durations,
                    "is_public": self.habit.is_public,
                    "user": self.user.pk,
                    "habit_pleasant": self.habit.habit_pleasant,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data, result)
