from django.urls import path
from . import views

# app_name permite usar nombres con namespace: 'core:lista_productos'
app_name = 'core'

urlpatterns = [
    # Lista de productos (página principal) - CBV con paginación/búsqueda
    path('', views.ProductoListView.as_view(), name='lista_productos'),
    
    # Detalle de producto (NUEVO - READ en CRUD)
    path('<int:pk>/', views.ProductoDetailView.as_view(), name='detalle_producto'),
    
    # Crear nuevo producto - CBV
    path('crear/', views.ProductoCreateView.as_view(), name='crear_producto'),
    
    # Editar producto existente - CBV
    path('editar/<int:pk>/', views.ProductoUpdateView.as_view(), name='editar_producto'),
    
    # Eliminar producto (con confirmación) - CBV
    path('eliminar/<int:pk>/', views.ProductoDeleteView.as_view(), name='eliminar_producto'),
]

"""
NOTAS IMPORTANTES SOBRE URLs CON CBV:

1. Las CBV usan .as_view() para convertirse en callables compatibles con URLconf.

2. pk_url_kwarg='pk' en las vistas coincide con <int:pk> en las URLs.

3. success_url = reverse_lazy('core:lista_productos') usa reverse_lazy
   (necesario en atributos de clase, se resuelve al primer request).

4. NUEVA RUTA: /<int:pk>/ → ProductoDetailView (detalle de producto)

5. Los nombres (name='...') NO cambian: compatibilidad total con templates
   y redirects existentes.
"""