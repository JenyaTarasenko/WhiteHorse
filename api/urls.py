from django.urls import path, include
from api.views import RegisterView, test_scan

app_name = 'api'


urlpatterns = [
    
    path('register/', RegisterView.as_view(), name='register'),
    path('test-scan/', test_scan, name='test_scan'),
]