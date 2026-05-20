from django.test import TestCase
from rest_framework.exceptions import ValidationError

from habits.models import Habit


class HabitModelTestCase(TestCase):
    def test_cannot_set_both_fields(self):
        habit = Habit(award="Подарок", habit_pleasant=None)
        with self.assertRaises(ValidationError):
            habit.full_clean()
