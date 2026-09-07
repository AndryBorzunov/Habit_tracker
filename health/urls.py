from django.urls import path

from health.apps import HealthConfig
from health.views import HealthView

app_name = HealthConfig.name

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
]
