"""
Serializadores DRF para el modelo Producto.
"""
from rest_framework import serializers
from .models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializer para la API REST de productos.
    Incluye métodos de creación/actualización personalizados y validations.
    """
    hay_stock = serializers.SerializerMethodField()
    creado_en = serializers.DateTimeField(read_only=True)
    actualizado_en = serializers.DateTimeField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='core:detalle_producto_slug')

    class Meta:
        model = Producto
        fields = [
            'url',
            'id',
            'nombre',
            'slug',
            'descripcion',
            'precio',
            'stock',
            'activo',
            'eliminado_en',
            'creado_en',
            'actualizado_en',
            'hay_stock',
        ]
        read_only_fields = ['slug', 'eliminado_en', 'creado_en', 'actualizado_en', 'hay_stock']

    def validate_nombre(self, value):
        """Validación personalizada del nombre: prohibir espacios al inicio o final."""
        if value.strip() != value:
            raise serializers.ValidationError("El nombre no puede tener espacios al inicio o al final.")
        return value.strip()

    def validate_precio(self, value):
        """Validación personalizada del precio: mínimo 0.01."""
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a cero.")
        return value

    def validate_stock(self, value):
        """Validación personalizada del stock: no negativo."""
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value

    def create(self, validated_data):
        """Sobrescribir create para setear slug automáticamente."""
        from django.utils.text import slugify
        nombre = validated_data['nombre']
        slug = slugify(nombre)
        # Asegurar unicidad del slug
        original_slug = slug
        counter = 1
        while Producto.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
        validated_data['slug'] = slug
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Sobrescribir update para preservar slug si no cambia nombre."""
        if 'nombre' in validated_data and validated_data['nombre'] != instance.nombre:
            from django.utils.text import slugify
            nombre = validated_data['nombre']
            slug = slugify(nombre)
            original_slug = slug
            counter = 1
            while Producto.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            validated_data['slug'] = slug
        return super().update(instance, validated_data)

    @staticmethod
    def get_hay_stock(obj):
        """Método para el campo hay_stock."""
        return obj.stock > 0