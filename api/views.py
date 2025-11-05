from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from .models import ScanTask
from .tasks import scan_website
from .url_scanner import quick_scan
from rest_framework.decorators import api_view
from urllib.parse import urlparse

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



@api_view(['POST'])
def test_scan(request):
    print("Получен URL:", request.POST)
    """
    GET /api/test-scan/?url=https://example.com
    Синхронный вызов quick_scan — удобно для быстрого теста компонента.
    """
    url = request.POST.get('url')
    if not url:
        return JsonResponse({'error': 'URL не указан. Пример: /api/test-scan/?url=https://example.com'}, status=400)

    # Простая валидация URL
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return JsonResponse({'error': 'Некорректный URL'}, status=400)

    try:
        result = quick_scan(url)   # Вызов твоей функции
        return JsonResponse(result, status=200, safe=False)
    except Exception as e:
        # Возвращаем ошибку (в проде можно логировать и возвращать более общий текст)
        return JsonResponse({'error': 'scan_failed', 'detail': str(e)}, status=500)