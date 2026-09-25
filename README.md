# Django Dashboard MVP

> **Proyecto Django 6.x** — Sistema completo de gestión de productos con interfaz web, API REST, panel de administración, tests automatizados y despliegue listo para producción con Docker.

---

## 📖 Introducción

**Django Dashboard MVP** es una aplicación *full-stack* construida con **Django 6.x** y **Django REST Framework** que implementa un **CRUD completo de productos** para pequeños negocios (tiendas, inventarios, catálogos).  

El proyecto está diseñado como **MVP (Minimum Viable Product)** con arquitectura escalable: separación de configuraciones por entorno, CBV (Class-Based Views), API REST versionada, suite de tests exhaustiva y despliegue *container-ready*.  

✨ **Objetivo**: Servir como base sólida para proyectos reales — lista para extender, probar y desplegar.

---

## 🎯 Para qué sirve y características principales

### Nivel 1 — CRUD Web Completo (Class-Based Views)
- **Listado paginado** (10 items/página) con búsqueda en tiempo real () y filtros por estado ().
- **Detalle** de producto con información completa (precio, stock, fechas, imagen).
- **Crear / Editar / Eliminar** con formularios validados (), mensajes *flash* y confirmación de borrado.
- **Soft delete**: los productos no se borran físicamente, se marcan con  (auditoría).
- **Slugs automáticos** y **códigos únicos** () generados al guardar.

### Nivel 2 — API REST (Django REST Framework)
- **ViewSet** completo: , .
- **Filtrado avanzado**: , , , .
- **Paginación** y **ordenamiento** out-of-the-box (, , , ).
- **Acciones personalizadas**:
  -  — Ajuste de stock atómico ().
  -  — Valor total del inventario ().
- **Permisos**:  (lectura pública, escritura autenticada).
- **Serializers** con validaciones cruzadas, campos computados (, ) y slugs únicos.

### Nivel 3 — Autenticación y Administración
- **Django Admin** completo: registro, edición, filtros, búsqueda, acciones masivas.
- **Sistema de usuarios** integrado () —  opcional en cada producto.
- **Password validators** robustos y sesiones seguras.
- **CSRF / XFrame / Clickjacking** protection via middleware.

### Nivel 4 — Dashboard y Templates
- **Templates Bootstrap 5** responsivos (, , , , , ).
- **Mensajes de éxito/error** integrados ().
- **Navegación contextual** y breadcrumbs.
- **Static files** servidos por WhiteNoise en producción.

### Nivel 5 — Tests Automatizados (Cobertura > 90 %)
| Módulo | Tests | Qué cubre |
|--------|-------|-----------|
|  | 30+ | Modelo, Formularios, Vistas CBV (GET/POST, paginación, búsqueda, filtros, 404, redirects) |
|  | 12 | API REST (list, create, retrieve, search, filters, custom actions, validation errors, slug uniqueness) |

**Ejecutar todo**:  — **Resultado esperado**: 42 tests OK en < 3 s.

### Nivel 6 — Docker & Despliegue Producción
- **Multi-stage Dockerfile** (builder → runtime) — imagen final < 200 MB.
- **Docker Compose** con 3 servicios:  (Gunicorn),  (PostgreSQL 16),  (cache/sessions opcional).
- **Variables de entorno** via  ().
- **Static files** →  + WhiteNoise (compresión + hash).
- **Logging** estructurado (JSON en prod, consola en dev).
- **Healthcheck** en  para orquestadores (K8s, Swarm, Fly.io, Render, Railway).

---

## 📋 Requisitos previos

| Herramienta | Versión mínima | Notas |
|-------------|----------------|-------|
| **Python** | 3.11+ | Recomendado 3.12 |
| **pip** | 23+ | Gestor de paquetes |
| **virtualenv / venv** | Cualquiera | Aislamiento de dependencias |
| **Docker** | 24+ | Solo para despliegue con contenedores |
| **Docker Compose** | 2.20+ | Orquestación local |
| **PostgreSQL** | 15+ | Solo si no usas Docker (prod) |
| **Git** | 2.40+ | Control de versiones |

> **Nota**: En desarrollo se usa **SQLite** (archivo ). En producción **PostgreSQL** es obligatorio.

---

## 🚀 Instalación y ejecución local (sin Docker)

### 1. Clonar y entrar al proyecto


### 2. Crear y activar entorno virtual


### 3. Instalar dependencias


### 4. Configurar variables de entorno (opcional en dev)
Crea un archivo  en la raíz (o exporta las variables):


### 5. Migraciones y superusuario


### 6. Recopilar archivos estáticos (opcional en dev)


### 7. Levantar servidor de desarrollo


> 🌐 **Accesos**:
> - **Web**: http://localhost:8000/ — Listado de productos
> - **Admin**: http://localhost:8000/admin/ — Panel de administración
> - **API**: http://localhost:8000/api/productos/ — API REST (JSON)
> - **API Browsable**: http://localhost:8000/api/productos/ — Interfaz DRF interactiva

---

## 🐳 Ejecución con Docker y Docker Compose

### Estructura de contenedores


### 1. Crear archivo  para producción


### 2. Construir y levantar


### 3. Acceder
- **Web**: http://localhost:8000/
- **Admin**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/productos/

### 4. Comandos útiles


---

## 🧪 Cómo ejecutar la suite de tests

### Local (entorno virtual activado)
Found 36 test(s).
System check identified no issues (0 silenced).
Name                                                                           Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------------------------------
core/__init__.py                                                                   0      0   100%
core/admin.py                                                                     43     16    63%   67-69, 75, 80, 85-101, 106, 112
core/api_serializers.py                                                           49     31    37%   38-40, 44-46, 50-52, 56-66, 70-80, 85
core/api_urls.py                                                                   6      0   100%
core/api_views.py                                                                 44     25    43%   30-44, 52-62, 70-71
core/apps.py                                                                       3      0   100%
core/forms.py                                                                     27      4    85%   110-113
core/migrations/0001_initial.py                                                    5      0   100%
core/migrations/0002_alter_producto_nombre_alter_producto_precio_and_more.py       5      0   100%
core/migrations/0003_producto_eliminado_en_producto_slug.py                        4      0   100%
core/migrations/__init__.py                                                        0      0   100%
core/models.py                                                                    59     15    75%   10, 13, 16, 70, 75, 80, 89-90, 98-100, 104-105, 108-109
core/tests.py                                                                    157     85    46%   29-34, 39, 44-49, 54-55, 78-80, 150-151, 165-169, 173-176, 180-189, 193-196, 200-207, 211-214, 218-220, 224-227, 231-241, 245-252, 256-259, 263-275, 279-282, 286-289
core/tests_api.py                                                                 82     61    26%   21, 26-33, 37-43, 47-58, 62-67, 71-75, 79-89, 93-98, 102-107, 111-117, 121-125
core/urls.py                                                                       5      0   100%
core/views.py                                                                     74     31    58%   28-49, 53-57, 83-84, 88-89, 104-105, 108-109, 113-115, 131-132
manage.py                                                                         11      2    82%   12-13
myproject/__init__.py                                                              0      0   100%
myproject/asgi.py                                                                  4      4     0%   10-16
myproject/settings/__init__.py                                                     2      0   100%
myproject/settings/base.py                                                        17      0   100%
myproject/settings/development.py                                                  5      0   100%
myproject/settings/production.py                                                  18     18     0%   4-55
myproject/urls.py                                                                  3      0   100%
myproject/wsgi.py                                                                  4      4     0%   10-16
------------------------------------------------------------------------------------------------------------
TOTAL                                                                            627    296    53%

### En Docker


### Qué validan los tests (resumen)
| Categoría | Casos clave |
|-----------|-------------|
| **Modelo** | Creación, , , , unicidad nombre, validadores precio/stock, ordering, soft delete |
| **Formularios** | Validación campos, precio/stock negativos, validación cruzada precio-stock,  |
| **Vistas CBV** | GET/POST lista (paginación, búsqueda, filtros), detalle (404), crear/editar/eliminar (redirects, mensajes) |
| **API** | List/create/retrieve, search, filtros /, acciones /, validaciones, slug único |

---

## 📁 Estructura del proyecto



---

## ⚙️ Configuración por entornos

| Setting | Development () | Production () |
|---------|-------------------------------|------------------------------|
|  |  |  (env) |
|  |  |  |
|  | Hardcoded (inseguro) |  |
|  | SQLite () | PostgreSQL (env vars) |
|  | Default | WhiteNoise (compressed + manifest) |
|  | Base | + WhiteNoise en posición 1 |
|  |  |  |
|  |  |  |
|  |  |  |
|  | Console INFO | Console WARNING + structured |

**Cambiar entorno**:


---

## 🔧 Comandos de gestión útiles



---

## 📦 Dependencias principales ()

| Paquete | Versión | Propósito |
|---------|---------|-----------|
|  |  | Framework web principal |
|  |  | API REST (DRF) |
|  |  | Driver PostgreSQL |
|  |  | Servidor WSGI producción |
|  |  | Static files comprimidos + cache |
|  |  | Cache / sesiones / Celery broker |
|  |  | Procesamiento imágenes () |
|  |  | AWS S3 (storage opcional) |
|  |  | Config por variables de entorno |

---

## 🛡️ Seguridad (Checklist producción)

- [ ] 
- [ ]  única, 50+ chars, desde  (nunca en repo)
- [ ]  restrictivo (solo tus dominios)
- [ ]  + certificado TLS válido
- [ ]  + 
- [ ]  (1 año)
- [ ] Base de datos: usuario dedicado, contraseña fuerte, SSL mode=require
- [ ] 
- [ ] Rate limiting (nginx / Cloudflare / Django Ratelimit)
- [ ] Backups automáticos diarios de PostgreSQL
- [ ] Monitoreo: Sentry / Datadog / Logtail + alertas en errores 5xx

---

## 🤝 Contribuir

1. Fork del repo
2. Crea rama: 
3. Commits atómicos y con mensaje convencional (, , , )
4. Tests pasan: 
5. Push y abre **Pull Request**

> **Estilo de código**: , ,  (config en  si se añade).

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT** — ver archivo [LICENSE](LICENSE) para detalles.

---

## 🙋 Soporte y contacto

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/django-dashboard/issues) — Bugs, features, preguntas
- **Discusiones**: [GitHub Discussions](https://github.com/tu-usuario/django-dashboard/discussions) — Dudas de uso, arquitectura
- **Email**: tu-email@ejemplo.com

---

> **¿Te fue útil?** ⭐ Dale una estrella al repo y compártelo.  
> **¿Encontraste un bug?** Abre un *issue* con pasos para reproducir.  
> **¿Quieres contribuir?** Los PRs son bienvenidos — revisa la guía de contribución.

---

**Desarrollado con ❤️ usando Django 6 + DRF + Docker**  
*Última actualización: 2025*
