from django.urls import path, include
from api.views import RegisterView, start_scan, get_scan_result

app_name = 'api'


urlpatterns = [
    #регистрация пользователя
    path('register/', RegisterView.as_view(), name='register'),
    #id начало сканирования 
    path('start-scan/', start_scan, name='start_scan'),
    #санирование по id задачи
    path('scan-result/<str:task_id>/', get_scan_result, name='get_scan_result') 
]