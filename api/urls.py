from django.urls import path, include
from api.views import RegisterView

app_name = 'api'


urlpatterns = [
    path('register', RegisterView.as_view(), name='register')
  
]