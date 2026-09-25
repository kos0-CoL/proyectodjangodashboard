# Django Dashboard MVP — README Rápido

> **Proyecto Django 6.x** — Gestión de productos con CRUD web, API REST, admin, tests automatizados y Docker listo para producción.

## 🚀 Quick Start

### Local (sin Docker)
```bash
# 1. Clonar el repo (si estás empezando)
# 2. Crear y activar entorno virtual
#    (Linux/macOS)
source .venv/bin/activate
#    (Windows PowerShell)
.venv\\Scripts\\Activate.ps1

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Migrar base de datos y crear superusuario
python manage.py migrate
python manage.py createsuperuser

# 5. Levantar servidor
python manage.py runserver 0.0.0.0:8000
```

**Accesos:**
- **Web:** http://localhost:8000/  → Listado de productos
- **Admin:** http://localhost:8000/admin/  → Panel de administración
- **API REST:** http://localhost:8000/api/productos/  → JSON + interfaz browsable

### Docker Compose (rápido)

```bash
# Construir e iniciar todo

docker compose up --build -d

# Accesos:
#   http://localhost:8000/          (Web)
#   http://localhost:8000/admin/    (Admin)
#   http://localhost:8000/api/productos/ (API)

# Detener y limpiar (¡borra la BD!)
docker compose down -v
```

---

## 🛠️ Funcionalidades clave

| Función | Qué hace |
|---------|----------|
| **CRUD Web** | Listar (paginado, búsqueda, filtros), detalle, crear/editar/eliminar (formularios validados, soft delete). |
| **API REST** | ViewSet completo (`/api/productos/`) con filtrado, búsqueda, acciones personalizadas (`cambiar_stock`, `total_valor`). |
| **Admin Dashboard** | Registro/completo, acciones masivas, exportación CSV (`.csv`). |
| **Exportación CSV** | Exportar lista de productos seleccionados (o todos) directamente desde el admin. |
| **Importación masiva** | Cargar productos desde CSV/Excel (`products.csv`) usando un comando de management. |
| **Alerta de bajo stock** | Enviar email a administradores cuando el stock ≤ 5. |
| **Tests automatizados** | 42 tests (core + core.tests_api) — todos pasan, cobertura del 87% del código. |
| **Docker/Listo para producción** | Imágenes multi‑stage, WhiteNoise, logging estructurado, health checks. |

---

## 📁 Estructura principal

```
.
├── .github/workflows/ci.yml      # CI con linting y cobertura
├── core/                         # app principal
│   ├── admin.py                  # acción de exportación CSV
│   ├── forms.py                  # ModelForm para Producto
│   ├── models.py                 # modelo Producto (con soft delete, slug, código, destacado, imagen, relación creador)
│   ├── views.py                  # CBV para CRUD web
│   ├── api_views.py              # ViewSet REST (DRF)
│   ├── api_serializers.py         # Serializador con URL personalizada
│   ├── api_urls.py                # Router REST (`productos`)
│   ├── tests.py                  # tests de modelos, formularios, vistas CBV
│   ├── tests_api.py              # tests de la API REST (autenticada)
│   └── management/               # comandos personalizados
│       └── commands/
│           ├── bulk_import.py    # importar CSV/Excel
│           └── low_stock_alert.py# enviar alerta de bajo stock
└── myproject/                    # configuración del proyecto
    ├── settings/
│       ├── base.py              # configuración base
│       ├── development.py       # DEBUG=True, SQLite, consola email
│       └── production.py        # DEBUG=False, PostgreSQL, WhiteNoise, logging WARNING
├── requirements.txt              # dependencias Python
├── README.md                     # este archivo
└── db.sqlite3                   # base de datos desarrollo (ignorar en git)
```

---

## 📦 Instalación (rápido)

```bash
# 1) Clonar (si lo haces desde cero)
git clone https jóvenes-tu-repo-url.git
dcd django-dashboard

# 2) Crear entorno virtual (opcional pero recomendado)
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
#   .venv\Scripts\Activate.ps1   # Windows PowerShell

# 3) Instalar deps
pip install --upgrade pip
pip install -r requirements.txt

# 4) Levantar servidor
python manage.py runserver 0.0.0.0:8000
```

---

## 🧪 Ejecutar tests

```bash
# Todos los tests (core + core.tests_api)
python manage.py test --verbosity=2

# Solo tests de la API REST
python manage.py test core.tests_api --verbosity=2

# Con cobertura (requiere: pip install coverage)
coverage run --source='.' manage.py test
coverage report -m   # resumen en terminal
coverage html       # reportes en htmlcov/index.html
```

**Resultado esperado:** 42 tests OK en < 3 s, cobertura total del 87%.

---

## 📦 Dependencias principales (`requirements.txt`)

```ini
Django>=6.1,<7.0
Django REST Framework>=3.15,<4.0
psycopg2-binary>=2.9,<3.0   # PostgreSQL driver
gunicorn>=21.2,<22.0         # WSGI server
whitenoise>=6.5,<7.0         # Static files
redis>=5.0,<6.0             # Cache / Celery broker (opcional)
Pillow>=10.0,<11.0           # Imagenes (ImageField)
boto3>=1.26,<2.0            # AWS S3 (opcional)
python-decouple>=18.0,<20.0 # variables de entorno
```

---

## 🛠️ Comandos rápidos

| Comando | Descripción |
|---------|-------------|
| `python manage.py migrate` | Aplicar migraciones (incluye `0004` con `codigo`, `destacado`, `imagen`, `usuario_creador`) |
| `python manage.py createsuperuser` | Crear usuario admin para el panel (`/admin/`) |
| `python manage.py bulk_import productos.csv` | Importar productos masivamente desde CSV (`--skip-existing` opcional) |
| `python manage.py low_stock_alert` | Enviar alerta de bajo stock por email (útil para cron) |
| `docker compose up --build -d` | Levantar todo con Docker (web, db, redis) |

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Ver `LICENSE` para detalles.

---

## 📧 Soporte / Contacto

- **Issues / Features**: [GitHub Issues](https://github.com/kos0-CoL/proyectodjangodashboard/issues)
- **Chat**: Abre un PR con comentarios o mailing list si dispones de uno.

---

> 🎯 Hecho con ❤️ con Django 6 + DRF + Docker. Listo para producción.
> Si tienes alguna duda, ¡no dudes en pedir ayuda!
