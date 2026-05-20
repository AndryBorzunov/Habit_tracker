from  rest_framework.routers import SimpleRouter
from rest_framework.urls import app_name

from habits.views import HabitViewSet
from habits.apps import HabitsConfig

app_name = HabitsConfig.name

router = SimpleRouter()
router.register("", HabitViewSet)

urlpatterns = []
urlpatterns += router.urls
