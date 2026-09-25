from django.contrib import admin
from .models import Producto
import os

# Configuración de Cloudinary (si se usa)
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME', 'demo')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY', '666399167468226')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET', 'z65ejY6o5a3d6Q4f')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Producto.
    Incluye imágenes, gestión de códigos, soft delete y acciones.
    """
    # Campos que se muestran en la lista principal
    list_display = ['nombre', 'codigo', 'precio', 'stock', 'activo', 'destacado', 'creado_en']
    
    # Filtros laterales (barra derecha)
    list_filter = ['activo', 'destacado', 'creado_en', 'eliminado_en']
    
    # Búsqueda por campos
    search_fields = ['nombre', 'descripcion', 'codigo']
    
    # Campos editables directamente desde la lista (sin entrar a editar)
    list_editable = ['precio', 'stock', 'activo', 'destacado']
    
    # Campos de solo lectura (no editables)
    readonly_fields = ['creado_en', 'actualizado_en', 'codigo', 'vista_imagen']
    
    # Organización del formulario de edición en secciones
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'slug', 'codigo', 'descripcion', 'precio')
        }),
        ('Inventario y estado', {
            'fields': ('stock', 'activo', 'destacado')
        }),
        ('Imagen', {
            'fields': ('imagen', 'vista_imagen')
        }),
        ('Fechas (automáticas)', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)  # Sección colapsable
        }),
        ('Eliminado suave', {
            'fields': ('eliminado_en',),
            'classes': ('collapse',),
            'description': 'Productos marcados como eliminados (soft delete).'
        }),
        ('Usuario creador', {
            'fields': ('usuario_creador',),
            'classes': ('collapse',),
            'description': 'Quién creó este producto.'
        }),
    )
    
    # Número de items por página
    list_per_page = 10
    
    # Acciones personalizadas en la lista
    actions = ['marcar_como_activos', 'marcar_como_destacados', 'exportar_como_csv']
    
    def vista_imagen(self, obj):
        """Mostrar una vista previa de la imagen en el formulario de admin."""
        if obj.imagen:
            return f'<img src="{obj.imagen.url}" style="max-height: 100px; max-width: 100px;" />'
        return 'No hay imagen'
    vista_imagen.allow_tags = True
    vista_imagen.short_description = 'Vista previa'
    
    def marcar_como_activos(self, request, queryset):
        """Action: marcar seleccionados como activos."""
        queryset.update(activo=True)
    marcar_como_activos.short_description = 'Marcar seleccionados como activos'
    
    def marcar_como_destacados(self, request, queryset):
        """Action: marcar seleccionados como destacados."""
        queryset.update(destacado=True)
    marcar_como_destacados.short_description = 'Marcar seleccionados como destacados'
    
    def exportar_como_csv(self, request, queryset):
        """Action: exportar CSV de productos seleccionados."""
        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="productos.csv"'
        writer = csv.writer(response)
        writer.writerow(['Nombre', 'Código', 'Precio', 'Stock', 'Activo', 'Destacado', 'Creado en'])
        for producto in queryset:
            writer.writerow([
                producto.nombre,
                producto.codigo,
                str(producto.precio),
                producto.stock,
                producto.activo,
                producto.destacado,
                producto.creado_en,
            ])
        return response
    exportar_como_csv.short_description = 'Exportar seleccionados como CSV'
    
    def get_queryset(self, request):
        """Mostrar todos los productos, incluidos los eliminados (para acciones admin)."""
        return Producto.objects.all()
    
    def delete_model(self, request, obj):
        """Sobrescribir delete para soft delete (si está habilitado)."""
        # Opcional: si quieres soft delete en admin, podrías marcar eliminado_en
        # pero mantendremos el delete real para simplicidad en este ejemplo.
        super().delete_model(request, obj)


# IMPORTANTE: El decorador @admin.register(Producto) hace lo mismo que:
# admin.site.register(Producto, ProductoAdmin)
# Pero es más limpio y "pythonico".