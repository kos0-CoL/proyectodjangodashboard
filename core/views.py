from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Producto
from .forms import ProductoForm


class ProductoListView(ListView):
    """
    CBV para listar productos con paginación, búsqueda y ordenamiento.
    
    Ventajas sobre FBV:
    - paginate_by automático
    - get_queryset() personalizable
    - get_context_data() para datos extra
    - context_object_name = 'productos' (igual que antes en template)
    """
    model = Producto
    template_name = 'core/lista.html'
    context_object_name = 'productos'
    paginate_by = 10  # Paginación automática: 10 por página
    ordering = ['-creado_en']  # Orden por defecto
    
    def get_queryset(self):
        """Filtrar por búsqueda (q) y estado (activo)."""
        queryset = super().get_queryset()
        
        # Búsqueda por nombre o descripción
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q) | Q(descripcion__icontains=q)
            )
        
        # Filtro por estado activo/inactivo
        estado = self.request.GET.get('estado')
        if estado == 'activos':
            queryset = queryset.filter(activo=True)
        elif estado == 'inactivos':
            queryset = queryset.filter(activo=False)
        
        # Ordenamiento por URL (?orden=nombre, ?orden=-precio, etc.)
        orden = self.request.GET.get('orden')
        if orden in ['nombre', '-nombre', 'precio', '-precio', 'stock', '-stock', 'creado_en', '-creado_en']:
            queryset = queryset.order_by(orden)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Añadir datos extra al contexto para el template."""
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['estado_actual'] = self.request.GET.get('estado', 'todos')
        context['orden_actual'] = self.request.GET.get('orden', '-creado_en')
        return context


class ProductoDetailView(DetailView):
    """
    CBV para ver detalle de un producto (READ del CRUD).
    Nueva funcionalidad que no teníamos en FBV.
    """
    model = Producto
    template_name = 'core/detalle.html'
    context_object_name = 'producto'
    pk_url_kwarg = 'pk'  # Por defecto ya es 'pk'


class ProductoCreateView(CreateView):
    """
    CBV para crear producto.
    Maneja GET/POST automáticamente, form_valid, form_invalid, success_url.
    """
    model = Producto
    form_class = ProductoForm
    template_name = 'core/crear.html'
    success_url = reverse_lazy('core:lista_productos')
    
    def form_valid(self, form):
        """Ejecutado cuando el formulario es válido."""
        messages.success(self.request, f'¡Producto "{form.instance.nombre}" creado correctamente!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Ejecutado cuando el formulario tiene errores."""
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        return super().form_invalid(form)


class ProductoUpdateView(UpdateView):
    """
    CBV para editar producto.
    Maneja instance automáticamente via pk_url_kwarg.
    """
    model = Producto
    form_class = ProductoForm
    template_name = 'core/editar.html'
    success_url = reverse_lazy('core:lista_productos')
    pk_url_kwarg = 'pk'
    
    def form_valid(self, form):
        messages.success(self.request, f'¡Producto "{form.instance.nombre}" actualizado!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Corrige los errores antes de guardar.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        """Pasar 'producto' al template (igual que FBV para compatibilidad)."""
        context = super().get_context_data(**kwargs)
        context['producto'] = self.object
        return context


class ProductoDeleteView(DeleteView):
    """
    CBV para eliminar producto con confirmación.
    GET muestra confirmación, POST elimina.
    """
    model = Producto
    template_name = 'core/eliminar.html'
    success_url = reverse_lazy('core:lista_productos')
    pk_url_kwarg = 'pk'
    context_object_name = 'producto'  # Para que template use {{ producto }}
    
    def form_valid(self, form):
        """DELETE usa form_valid (no hay formulario real, solo confirmación POST)."""
        messages.success(self.request, f'Producto "{self.object.nombre}" eliminado.')
        return super().form_valid(form)