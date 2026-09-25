"""
Tests API REST para DRF.
Ejecuta con: python manage.py test core.tests_api
"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from decimal import Decimal
from django.contrib.auth.models import User
from .models import Producto


class ProductoAPITests(TestCase):
    """
    Tests para el API REST de productos.
    """
    def setUp(self):
        """Configurar cliente y datos."""
        self.client = APIClient()
        # Crear usuario y autenticar para poder hacer POST (IsAuthenticatedOrReadOnly)
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.crear_producto("Laptop HP", "Laptop de oficina", Decimal('899.99'), 10)
        self.crear_producto("Mouse Inalámbrico", "Mouse sin cables", Decimal('29.99'), 5)

    def crear_producto(self, nombre, descripcion, precio, stock):
        """Helper para crear producto via API."""
        url = reverse('producto-list')
        data = {
            'nombre': nombre,
            'descripcion': descripcion,
            'precio': str(precio),
            'stock': stock,
        }
        response = self.client.post(url, data, format='json')
        return response

    def test_listar_productos(self):
        """GET /api/productos/ debe retornar lista."""
        url = reverse('producto-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn('nombre', response.data[0])
        self.assertIn('slug', response.data[0])
        self.assertIn('url', response.data[0])

    def test_crear_producto_via_api(self):
        """POST /api/productos/ crea un producto."""
        url = reverse('producto-list')
        data = {
            'nombre': 'Tablet',
            'descripcion': 'Tablet 10" para lectura',
            'precio': '199.99',
            'stock': 7,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producto.objects.count(), 3)
        self.assertIn('slug', response.data)
        self.assertIn('url', response.data)

    def test_obtener_producto_detalle(self):
        """GET /api/productos/{id}/ devuelve un solo producto."""
        producto = Producto.objects.first()
        url = reverse('producto-detail', kwargs={'pk': producto.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], producto.nombre)
        self.assertEqual(response.data['slug'], producto.slug)

    def test_busqueda_api(self):
        """GET /api/productos/?search=laptop filtra correctamente."""
        url = reverse('producto-list')
        response = self.client.get(url, {'search': 'laptop'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre'], 'Laptop HP')

    def test_filtro_activo_api(self):
        """GET /api/productos/?activo=true filtra por estado."""
        url = reverse('producto-list')
        response = self.client.get(url, {'activo': 'true'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Los dos productos creados están activos (activo=True por defecto)
        self.assertEqual(len(response.data), 2)
        # Desactivar uno
        prod = Producto.objects.first()
        prod.activo = False
        prod.save()
        response = self.client.get(url, {'activo': 'true'}, format='json')
        self.assertEqual(len(response.data), 1)

    def test_accion_personalizada_cambiar_stock(self):
        """POST /api/productos/{pk}/cambiar_stock/ ajusta stock."""
        producto = Producto.objects.first()
        url = reverse('producto-cambiar-stock', kwargs={'pk': producto.pk})
        data = {'delta': -3}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stock'], producto.stock - 3)

    def test_accion_personalizada_total_valor(self):
        """GET /api/productos/total_valor/ retorna valor total."""
        url = reverse('producto-total-valor')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        total = response.data['total_valor']
        # (899.99 * 10) + (29.99 * 5) = 8999.9 + 149.95 = 9149.85
        self.assertAlmostEqual(total, 9149.85, places=2)

    def test_error_validacion_api(self):
        """POST /api/productos/ con datos inválidos retorna error."""
        url = reverse('producto-list')
        data = {'nombre': '', 'precio': '-10', 'stock': -5}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nombre', response.data)
        self.assertIn('precio', response.data)
        self.assertIn('stock', response.data)

    def test_slug_unico_en_api(self):
        """Crear productos con nombres que generan slug duplicado → slug único."""
        # Nombres distintos que generan el mismo slug base
        self.crear_producto('Producto Test', 'Descripción 1', Decimal('10'), 1)
        response2 = self.crear_producto('Producto Test!', 'Descripción 2', Decimal('20'), 2)  # slugify -> 'producto-test'
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response2.data['slug'], 'producto-test')
        self.assertTrue(response2.data['slug'].startswith('producto-test-'))