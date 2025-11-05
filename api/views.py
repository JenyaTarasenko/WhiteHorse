from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from .models import ScanTask
from .tasks import scan_website

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            
            "message": "✅ Вы успешно зарегистрировались!",
            "user": serializer.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


def start_scan(request):
    url = request.GET.get('url')
    user = request.user
    if not url:
        return JsonResponse({'error': 'URL обязателен'}, status=400)

    task = ScanTask.objects.create(user=user, url=url)
    scan_website.delay(str(task.id))  # асинхронный запуск через Celery

    return JsonResponse({'message': 'Сканирование запущено', 'task_id': task.id})