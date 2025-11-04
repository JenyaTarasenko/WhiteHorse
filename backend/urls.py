from django.conf.urls.static import static  # Добавь этот импорт
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),#app_name
    path("", TemplateView.as_view(template_name="base.html")),
    
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/auth/', include('djoser.urls.authtoken')),      # Получение токена (login/logout)
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)