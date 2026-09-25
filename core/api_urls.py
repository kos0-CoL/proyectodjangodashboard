"""
URLs API REST para productos.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api_views import ProductoViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]