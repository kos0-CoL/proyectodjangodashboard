"""
Vistas DRF para productos con filtrado, búsqueda y paginación.
"""
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Producto
from .api_serializers import ProductoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD completo + acciones personalizadas.
    Rutas: /api/productos/ (todas las acciones), /api/productos/{pk}/ (detalle)
    """
    queryset = Producto.objects.all().select_related()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'precio', 'stock', 'creado_en', 'actualizado_en']
    ordering = ['-creado_en']

    def get_queryset(self):
        """Aplicar filtros adicionales: activo, eliminado, etc."""
        qs = super().get_queryset()
        # ?activo=true/false
        activo = self.request.query_params.get('activo')
        if activo is not None:
            activo_bool = activo.lower() in ('true', '1', 'yes')
            qs = qs.filter(activo=activo_bool)
        # ?eliminado=true para mostrar solo eliminados (admin)
        eliminado = self.request.query_params.get('eliminado')
        if eliminado is not None:
            eliminado_bool = eliminado.lower() in ('true', '1', 'yes')
            if eliminado_bool:
                qs = Producto.objects.eliminados()
            else:
                qs = Producto.objects.activos()
        return qs

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cambiar_stock(self, request, pk=None):
        """
        Acción personalizada: ajustar stock con validación.
        POST /api/productos/{pk}/cambiar_stock/ con {'delta': +5 or -2}
        """
        producto = self.get_object()
        delta = request.data.get('delta', 0)
        if not isinstance(delta, (int, float)):
            return Response({'error': 'delta debe ser numérico'}, status=status.HTTP_400_BAD_REQUEST)
        nuevo_stock = producto.stock + delta
        if nuevo_stock < 0:
            return Response({'error': 'Stock no puede ser negativo'}, status=status.HTTP_400_BAD_REQUEST)
        producto.stock = nuevo_stock
        producto.save()
        serializer = self.get_serializer(producto)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def total_valor(self, request):
        """
        Acción personalizada: calcular valor total del inventario (precio * stock).
        GET /api/productos/total_valor/
        """
        total = sum(p.precio * p.stock for p in self.get_queryset())
        return Response({'total_valor': float(total)})