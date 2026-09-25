"""
URL configuration for myproject project.

La lista `urlpatterns` enruta URLs a vistas. Para más información:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include  # include permite incluir URLs de otras apps

urlpatterns = [
    path('admin/', admin.site.urls),                       # Panel de administración de Django
    path('', include('core.urls')),                        # URLs del sitio web principal
    path('api/', include('core.api_urls')),                # 🚀 API REST - Endpoint /api/productos/
]