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
```bash
# Todos los tests (core + core.tests_api)
python manage.py test --verbosity=2

# Solo tests de modelos/forms/vistas
python manage.py test core.tests --verbosity=2

# Solo tests de API REST
python manage.py test core.tests_api --verbosity=2

# Con cobertura (requiere: pip install coverage)
coverage run --source='.' manage.py test
coverage report -m          # Resumen en terminal
coverage html               # Reporte HTML en htmlcov/index.html

### En Docker
docker compose exec web python manage.py test --verbosity=2
docker compose exec web coverage run --source='.' manage.py test
docker compose exec web coverage report -m

### Qué validan los tests (resumen)
| Categoría | Tests | Casos clave |
|-----------|-------|-------------|
| **Modelo** | 13 | Creación, , , , unicidad nombre, validadores precio/stock, ordering, soft delete |
| **Formularios** | 7 | Validación campos, precio/stock negativos, validación cruzada precio-stock,  |
| **Vistas CBV** | 16 | GET/POST lista (paginación, búsqueda, filtros), detalle (404), crear/editar/eliminar (redirects, mensajes) |
| **API REST** | 12 | List/create/retrieve, search, filtros /, acciones /, validaciones, slug único |

> **Total: ~48 tests** — Ejecutan en < 3 segundos. Objetivo: **cobertura > 80%** en código de negocio (, , , ).

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
- **Email**: gonzaleznazareno@abc.gob.ar

---

> **¿Te fue útil?** ⭐ Dale una estrella al repo y compártelo.  
> **¿Encontraste un bug?** Abre un *issue* con pasos para reproducir.  
> **¿Quieres contribuir?** Los PRs son bienvenidos — revisa la guía de contribución.

---

**Desarrollado con ❤️ usando Django 6 + DRF + Docker**  
*Última actualización: 2026*
