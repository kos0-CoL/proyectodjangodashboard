from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify


class ProductoManager(models.Manager):
    """Manager personalizado para filtrar solo productos activos."""
    def activos(self):
        return self.filter(activo=True, eliminado_en__isnull=True)
    
    def eliminados(self):
        return self.filter(eliminado_en__isnull=False)
    
    def por_defecto(self):
        return self.activos()


class Producto(models.Model):
    """
    Modelo simple para un sistema básico de productos.
    Representa un producto en un pequeño negocio (ej. tienda, inventario).
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del producto")
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name="Slug")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Precio",
        validators=[MinValueValidator(0.01, message="El precio debe ser mayor a cero.")]
    )
    stock = models.PositiveIntegerField(
        default=0, 
        verbose_name="Stock disponible",
        validators=[MinValueValidator(0, message="El stock no puede ser negativo.")]
    )
    activo = models.BooleanField(default=True, verbose_name="¿Activo?")
    eliminado_en = models.DateTimeField(null=True, blank=True, verbose_name="Eliminado el")
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    objects = ProductoManager()

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-creado_en']  # Más recientes primero

    def __str__(self):
        """Representación legible del objeto (usada en admin, shell, etc.)."""
        return f"{self.nombre} - ${self.precio}"

    @property
    def hay_stock(self):
        """Propiedad conveniente para saber si hay stock."""
        return self.stock > 0

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.nombre):
            self.slug = slugify(self.nombre)
            # Asegurar unicidad del slug
            original_slug = self.slug
            counter = 1
            while Producto.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def eliminar(self):
        """Eliminación suave: marca como eliminado en lugar de borrar."""
        from django.utils import timezone
        self.eliminado_en = timezone.now()
        self.save()

    def restaurar(self):
        """Restaura un producto eliminado."""
        self.eliminado_en = None
        self.save()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('core:detalle_producto_slug', kwargs={'slug': self.slug})