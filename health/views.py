from rest_framework.response import Response
from rest_framework.views import APIView

class HealthView(APIView):
    authentication_classes = []   # ← отключает JWT/Session/Basic
    permission_classes = []       # ← отключает проверки прав

    def get(self, request):
        return Response({"status": "ok", "service": "habit-traker"})
    