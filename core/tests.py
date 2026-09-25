"""
Tests unitarios para la app core.
Ejecuta con: python manage.py test core
"""
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Producto
from .forms import ProductoForm


class ProductoModelTests(TestCase):
    """Tests para el modelo Producto."""
    
    def setUp(self):
        """Datos de prueba reutilizables."""
        self.producto_data = {
            'nombre': 'Laptop HP 15"',
            'descripcion': 'Laptop para oficina',
            'precio': Decimal('899.99'),
            'stock': 10,
            'activo': True,
        }
    
    def test_crear_producto_valido(self):
        """Un producto con datos válidos se crea correctamente."""
        producto = Producto.objects.create(**self.producto_data)
        self.assertEqual(producto.nombre, 'Laptop HP 15"')
        self.assertEqual(producto.precio, Decimal('899.99'))
        self.assertEqual(producto.stock, 10)
        self.assertTrue(producto.activo)
        self.assertIsNotNone(producto.creado_en)
        self.assertIsNotNone(producto.actualizado_en)
    
    def test_str_representation(self):
        """__str__ devuelve formato correcto."""
        producto = Producto.objects.create(**self.producto_data)
        self.assertEqual(str(producto), 'Laptop HP 15" - $899.99')
    
    def test_hay_stock_property(self):
        """Property hay_stock funciona correctamente."""
        p_con_stock = Producto.objects.create(**self.producto_data)
        self.assertTrue(p_con_stock.hay_stock)
        
        p_sin_stock = Producto.objects.create(
            **{**self.producto_data, 'nombre': 'Mouse', 'stock': 0}
        )
        self.assertFalse(p_sin_stock.hay_stock)
    
    def test_nombre_unico(self):
        """No se pueden crear dos productos con el mismo nombre."""
        Producto.objects.create(**self.producto_data)
        with self.assertRaises(Exception):  # IntegrityError en BD
            Producto.objects.create(**self.producto_data)
    
    def test_precio_no_negativo_validator(self):
        """Validador MinValueValidator en precio."""
        producto = Producto(**{**self.producto_data, 'precio': Decimal('-10.00')})
        with self.assertRaises(ValidationError):
            producto.full_clean()
    
    def test_precio_cero_invalido(self):
        """Precio 0 es inválido (min 0.01)."""
        producto = Producto(**{**self.producto_data, 'precio': Decimal('0.00')})
        with self.assertRaises(ValidationError):
            producto.full_clean()
    
    def test_stock_no_negativo_validator(self):
        """Validador MinValueValidator en stock."""
        producto = Producto(**{**self.producto_data, 'stock': -5})
        with self.assertRaises(ValidationError):
            producto.full_clean()
    
    def test_ordering_por_fecha_creacion(self):
        """Meta.ordering = ['-creado_en'] funciona."""
        Producto.objects.create(**{**self.producto_data, 'nombre': 'Producto A'})
        Producto.objects.create(**{**self.producto_data, 'nombre': 'Producto B'})
        productos = list(Producto.objects.all())
        self.assertEqual(productos[0].nombre, 'Producto B')  # Más reciente primero


class ProductoFormTests(TestCase):
    """Tests para el formulario ProductoForm."""
    
    def test_form_valido_con_datos_correctos(self):
        """Formulario válido con todos los campos requeridos."""
        form = ProductoForm(data={
            'nombre': 'Teclado Mecánico',
            'descripcion': 'Switches azules',
            'precio': '129.99',
            'stock': 5,
            'activo': True,
        })
        self.assertTrue(form.is_valid())
    
    def test_form_invalido_sin_nombre(self):
        """Nombre es obligatorio."""
        form = ProductoForm(data={
            'nombre': '',
            'precio': '100.00',
            'stock': 1,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
    
    def test_form_invalido_precio_negativo(self):
        """Precio negativo falla validación."""
        form = ProductoForm(data={
            'nombre': 'Test',
            'precio': '-50.00',
            'stock': 1,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('precio', form.errors)
    
    def test_form_invalido_stock_negativo(self):
        """Stock negativo falla validación."""
        form = ProductoForm(data={
            'nombre': 'Test',
            'precio': '100.00',
            'stock': '-1',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('stock', form.errors)
    
    def test_clean_validacion_cruzada_precio_stock(self):
        """Validación cruzada: stock > 0 requiere precio > 0."""
        form = ProductoForm(data={
            'nombre': 'Test Cruzado',
            'precio': '0.00',  # Precio inválido
            'stock': 10,       # Pero hay stock
        })
        self.assertFalse(form.is_valid())
        self.assertIn('precio', form.errors)
        self.assertTrue(
            any('stock' in str(e).lower() or 'precio' in str(e).lower() 
                for e in form.errors['precio'])
        )
    
    def test_form_save_crea_producto(self):
        """form.save() crea instancia en BD."""
        form = ProductoForm(data={
            'nombre': 'Producto Test Save',
            'precio': '99.99',
            'stock': 3,
        })
        self.assertTrue(form.is_valid())
        producto = form.save()
        self.assertEqual(producto.nombre, 'Producto Test Save')
        self.assertEqual(Producto.objects.count(), 1)


class ProductoViewTests(TestCase):
    """Tests para las vistas (CBV)."""
    
    def setUp(self):
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            descripcion='Descripción test',
            precio=Decimal('150.00'),
            stock=5,
            activo=True,
        )
        self.lista_url = reverse('core:lista_productos')
        self.crear_url = reverse('core:crear_producto')
        self.detalle_url = reverse('core:detalle_producto', kwargs={'pk': self.producto.pk})
        self.editar_url = reverse('core:editar_producto', kwargs={'pk': self.producto.pk})
        self.eliminar_url = reverse('core:eliminar_producto', kwargs={'pk': self.producto.pk})
    
    def test_lista_productos_get(self):
        """GET lista productos retorna 200 y usa template correcto."""
        response = self.client.get(self.lista_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/lista.html')
        self.assertContains(response, 'Producto Test')
    
    def test_lista_productos_paginacion(self):
        """Paginación funciona (crear 15 productos, paginate_by=10)."""
        for i in range(15):
            Producto.objects.create(
                nombre=f'Producto {i}',
                precio=Decimal('10.00'),
                stock=1,
            )
        response = self.client.get(self.lista_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['productos']), 10)
    
    def test_lista_productos_busqueda(self):
        """Búsqueda ?q= funciona."""
        Producto.objects.create(nombre='Laptop Gaming', precio=Decimal('1000'), stock=1)
        response = self.client.get(self.lista_url, {'q': 'Gaming'})
        self.assertContains(response, 'Laptop Gaming')
        self.assertNotContains(response, 'Producto Test')
    
    def test_lista_productos_filtro_estado(self):
        """Filtro ?estado=activos/inactivos funciona."""
        Producto.objects.create(nombre='Inactivo', precio=Decimal('10'), stock=1, activo=False)
        response = self.client.get(self.lista_url, {'estado': 'activos'})
        self.assertContains(response, 'Producto Test')
        self.assertNotContains(response, 'Inactivo')
        
        response = self.client.get(self.lista_url, {'estado': 'inactivos'})
        self.assertContains(response, 'Inactivo')
        self.assertNotContains(response, 'Producto Test')
    
    def test_detalle_producto_get(self):
        """GET detalle producto retorna 200."""
        response = self.client.get(self.detalle_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/detalle.html')
        self.assertContains(response, 'Producto Test')
    
    def test_detalle_producto_404(self):
        """Detalle de PK inexistente retorna 404."""
        url = reverse('core:detalle_producto', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_crear_producto_get(self):
        """GET crear muestra formulario."""
        response = self.client.get(self.crear_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/crear.html')
        self.assertIsInstance(response.context['form'], ProductoForm)
    
    def test_crear_producto_post_valido(self):
        """POST crear válido redirige y crea producto."""
        data = {
            'nombre': 'Nuevo Producto POST',
            'descripcion': 'Creado via test',
            'precio': '299.99',
            'stock': 7,
            'activo': True,
        }
        response = self.client.post(self.crear_url, data)
        self.assertRedirects(response, self.lista_url)
        self.assertTrue(Producto.objects.filter(nombre='Nuevo Producto POST').exists())
        self.assertEqual(Producto.objects.count(), 2)
    
    def test_crear_producto_post_invalido(self):
        """POST crear inválido no redirige y muestra errores."""
        data = {'nombre': '', 'precio': '100', 'stock': 1}  # nombre vacío
        response = self.client.post(self.crear_url, data)
        self.assertEqual(response.status_code, 200)
        # Verificar error en contexto del formulario (TemplateResponse)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('nombre', form.errors)
        self.assertEqual(Producto.objects.count(), 1)
    
    def test_editar_producto_get(self):
        """GET editar muestra formulario precargado."""
        response = self.client.get(self.editar_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/editar.html')
        self.assertEqual(response.context['form'].instance, self.producto)
    
    def test_editar_producto_post_valido(self):
        """POST editar válido actualiza y redirige."""
        data = {
            'nombre': 'Producto Actualizado',
            'descripcion': 'Nueva desc',
            'precio': '199.99',
            'stock': 3,
            'activo': False,
        }
        response = self.client.post(self.editar_url, data)
        self.assertRedirects(response, self.lista_url)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Producto Actualizado')
        self.assertEqual(self.producto.precio, Decimal('199.99'))
        self.assertFalse(self.producto.activo)
    
    def test_eliminar_producto_get(self):
        """GET eliminar muestra confirmación."""
        response = self.client.get(self.eliminar_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/eliminar.html')
        self.assertEqual(response.context['producto'], self.producto)
    
    def test_eliminar_producto_post(self):
        """POST eliminar borra y redirige."""
        response = self.client.post(self.eliminar_url)
        self.assertRedirects(response, self.lista_url)
        self.assertFalse(Producto.objects.filter(pk=self.producto.pk).exists())
        self.assertEqual(Producto.objects.count(), 0)