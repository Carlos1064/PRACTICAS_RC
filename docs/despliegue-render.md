# Despliegue en Render

## Base PostgreSQL

1. En Render crea una base PostgreSQL con el plan Free y la misma región del servicio web.
2. En la base, copia la **Internal Database URL**. No la publiques ni la guardes en GitHub.
3. Abre el servicio web → **Environment** y agrega `DATABASE_URL` con esa URL.
4. Mantén `DEBUG=False` y configura `SECRET_KEY` con un valor aleatorio generado por Render. `RENDER_EXTERNAL_HOSTNAME` se añade automáticamente a los hosts y orígenes CSRF por la configuración de Django.
5. Para crear el administrador sin usar Render Shell, agrega temporalmente estas variables secretas al servicio web:

   - `BOOTSTRAP_ADMIN_EMAIL`: correo que usarás para administrar la plataforma.
   - `BOOTSTRAP_ADMIN_NAME`: nombre del administrador.
   - `BOOTSTRAP_ADMIN_PASSWORD`: una contraseña larga, única y distinta de las cuentas demo.

   Guarda las variables seleccionando **Save, rebuild, and deploy**. El build ejecuta migraciones y crea la cuenta si todavía no existe. El comando no cambia la contraseña en despliegues posteriores. Después del despliegue, elimina `BOOTSTRAP_ADMIN_PASSWORD` (y las otras dos variables si quieres) del servicio; la cuenta creada permanece en PostgreSQL.

El plan Free de Render vence a los 30 días. Exporta la información que quieras conservar antes de esa fecha o cambia la base a un plan persistente. El sistema no guardará cambios de producción en SQLite si falta `DATABASE_URL`: Django detendrá el arranque para evitar perder datos silenciosamente.

## Comandos del servicio

En **Settings → Build & Deploy** configura:

- **Build Command:** `bash build.sh`
- **Start Command:** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

El build instala dependencias, recopila CSS/JavaScript con `collectstatic`, aplica las migraciones y crea el administrador inicial.

## Cargar datos sintéticos para una demostración

La base local de este proyecto contiene datos sintéticos: cinco cuentas, tres empresas, cinco categorías, treinta ofertas publicadas, una pendiente y dos postulaciones. Para generarlos en PostgreSQL sin usar Shell, agrega temporalmente al Environment del servicio:

- `LOAD_DEMO_DATA` = `true`
- `DEMO_PASSWORD` = una contraseña demo fuerte y privada

Selecciona **Save, rebuild, and deploy**. Después de que el build termine correctamente, elimina ambas variables y vuelve a desplegar. Las cuentas estudiante y empresa usarán la contraseña definida en `DEMO_PASSWORD`; el comando conserva la contraseña del administrador creado anteriormente. No muestra la contraseña en los logs.

La carga recrea los registros definidos por `seed_demo`; no copia cambios manuales que pudieras haber hecho en filas de la base SQLite local. No subas `db.sqlite3` ni archivos de exportación con datos reales al repositorio público.

## Cuenta y primeros datos

Entra con el correo y la contraseña configurados arriba. La cuenta recibe el rol administrador de la plataforma. Desde el panel crea categorías y luego registra empresas y estudiantes desde la aplicación.

## Verificación funcional

1. Abre el inicio; revisa que carguen CSS y JavaScript.
2. Crea una categoría desde el panel y confirma que aparece en el listado.
3. Registra una empresa y apruébala; crea y aprueba una oferta.
4. Registra un estudiante, postúlate y cambia el estado desde la cuenta de la empresa.
5. Abre el reporte y descarga el CSV.
6. Reinicia el servicio y confirma que los registros siguen disponibles. Si se creó la base Free, recuerda que se elimina al vencer el periodo gratuito.
