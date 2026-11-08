# Plataforma de Prácticas y Oportunidades Laborales

Aplicación académica para reunir ofertas de prácticas y empleo, perfiles de estudiantes y empresas, y seguimiento de postulaciones. El proyecto usa Django con arquitectura MVT y SQLite en desarrollo. El análisis, los diseños, la matriz de pruebas y el manual están en `docs/`.

## Funciones

- Registro e ingreso para estudiantes/egresados y empresas.
- Aprobación administrativa de empresas y ofertas antes de publicarlas.
- Gestión de perfiles, categorías y ofertas.
- Búsqueda de oportunidades con filtros, paginación y actualización parcial con `fetch`.
- Postulaciones únicas, retiro y seguimiento de estados.
- Panel con indicadores, gráficos y reporte filtrable con exportación CSV.
- Control de acceso por rol, validación de servidor y navegador, mensajes visuales y páginas propias 403, 404 y 500.

## Tecnologías

- Python 3.12 o superior compatible con Django 5.2.
- Django 5.2.18.
- SQLite para desarrollo.
- HTML5, CSS3 y JavaScript.
- Chart.js 4.4.8 desde CDN en el panel (el resumen en texto sigue disponible si no carga el CDN).

## Instalación local en Windows PowerShell

Desde la carpeta del proyecto:

1. Crear un entorno virtual:

   ```powershell
   python -m venv .venv
   ```

   Si el equipo ya tiene Django instalado y no puede descargar paquetes, usar `python -m venv --system-site-packages .venv`.

2. Activarlo:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Instalar dependencias:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Crear la configuración local:

   ```powershell
   Copy-Item .env.example .env
   ```

   Reemplaza `SECRET_KEY` por una cadena aleatoria larga. Para el desarrollo local deja `DEBUG=True` y `ALLOWED_HOSTS=localhost,127.0.0.1`. Antes de sustentar o desplegar usa `DEBUG=False` y configura los hosts correspondientes.

5. Crear las tablas y datos de demostración:

   ```powershell
   python manage.py migrate
   python manage.py seed_demo
   ```

6. Iniciar la aplicación:

   ```powershell
   python manage.py runserver
   ```

7. Abrir `http://127.0.0.1:8000/`.

El modelo de usuario personalizado (`cuentas.Usuario`) ya está enlazado como `AUTH_USER_MODEL`. Si se prepara otra base desde cero, no se debe cambiar ese ajuste después de generar las migraciones iniciales.

## Cuentas de demostración

El comando `seed_demo` crea cinco cuentas, dos empresas aprobadas y una pendiente, cinco categorías, treinta ofertas publicadas, una oferta pendiente y dos postulaciones de demostración. Las cuentas usan la contraseña local `PracticasDemo2026!`:

| Rol | Correo |
|---|---|
| Estudiante | `estudiante@demo.local` |
| Empresa | `empresa1@demo.local` |
| Empresa | empresa2@demo.local |
| Empresa pendiente | empresa3@demo.local |
| Administrador de plataforma | `admin@demo.local` |

Estas credenciales son solo para desarrollo. Cada vez que se ejecuta el seed, actualiza las contraseñas de demostración. Para usar el Django Admin se requiere una cuenta con `is_staff`; puedes crearla con `python manage.py createsuperuser`.

## Pruebas y verificaciones

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

La matriz ejecutada está en [`docs/pruebas/matriz-pruebas.md`](docs/pruebas/matriz-pruebas.md).

## Estructura

```text
config/          Configuración, rutas y páginas de error
cuentas/         Usuario, perfiles, autenticación y gestión de cuentas
ofertas/         Categorías, ofertas, búsqueda y aprobaciones
postulaciones/   Candidaturas y cambios de estado
panel/           Indicadores, reportes y exportación CSV
templates/       Plantillas compartidas y páginas por módulo
static/          CSS y JavaScript
docs/            Análisis, diseño, pruebas y manual
```

## Documentación

- [Análisis](docs/01-analisis.md)
- [Diseño y modelo E-R](docs/02-diseno/01-modelo-er.md)
- [Mapa de URLs y vistas](docs/02-diseno/02-mapa-urls.md)
- [Wireframes](docs/02-diseno/03-wireframes.md)
- [Arquitectura](docs/02-diseno/04-arquitectura.md)
- [Guion para el video](docs/guion-video.md)
- [Presentación de sustentación](docs/presentacion.pptx)
- [Guion y ruta de demo](docs/sustentacion.md)
- [Manual de usuario](docs/manual-usuario.md)
- [Decisiones técnicas](docs/decisiones-tecnicas.md)
- [Matriz de pruebas](docs/pruebas/matriz-pruebas.md)
