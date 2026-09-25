from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Producto.
    Personaliza qué se ve, cómo se filtra y cómo se busca.
    """
    # Campos que se muestran en la lista principal
    list_display = ['nombre', 'precio', 'stock', 'activo', 'creado_en']
    
    # Filtros laterales (barra derecha)
    list_filter = ['activo', 'creado_en']
    
    # Búsqueda por campos
    search_fields = ['nombre', 'descripcion']
    
    # Campos editables directamente desde la lista (sin entrar a editar)
    list_editable = ['precio', 'stock', 'activo']
    
    # Campos de solo lectura (no editables)
    readonly_fields = ['creado_en', 'actualizado_en']
    
    # Organización del formulario de edición en secciones
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'descripcion', 'precio')
        }),
        ('Inventario', {
            'fields': ('stock', 'activo')
        }),
        ('Fechas (automáticas)', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)  # Sección colapsable
        }),
    )
    
    # Número de items por página
    list_per_page = 10


# IMPORTANTE: El decorador @admin.register(Producto) hace lo mismo que:
# admin.site.register(Producto, ProductoAdmin)
# Pero es más limpio y "pythonico".