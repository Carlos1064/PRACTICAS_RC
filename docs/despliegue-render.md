# Despliegue en Render

## Base PostgreSQL

1. En Render crea una base PostgreSQL con el plan Free y la misma región del servicio web.
2. En la base, copia la **Internal Database URL**. No la publiques ni la guardes en GitHub.
3. Abre el servicio web → **Environment** y agrega `DATABASE_URL` con esa URL.
4. Mantén `DEBUG=False` y configura `SECRET_KEY` con un valor aleatorio generado por Render. `RENDER_EXTERNAL_HOSTNAME` se añade automáticamente a los hosts y orígenes CSRF por la configuración de Django.

El plan Free de Render vence a los 30 días. Exporta la información que quieras conservar antes de esa fecha o cambia la base a un plan persistente. El sistema no guardará cambios de producción en SQLite si falta `DATABASE_URL`: Django detendrá el arranque para evitar perder datos silenciosamente.

## Comandos del servicio

En **Settings → Build & Deploy** configura:

- **Build Command:** `bash build.sh`
- **Start Command:** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

El build instala dependencias, recopila CSS/JavaScript con `collectstatic` y aplica las migraciones a la base configurada. No ejecutes `seed_demo` en el servicio público: crea cuentas con una contraseña de demostración conocida.

## Cuenta y primeros datos

Después del primer despliegue, abre **Shell** en el servicio y ejecuta:

```bash
python manage.py createsuperuser
```

Usa el correo y contraseña del administrador real del proyecto. Entra al panel para crear categorías y luego registra empresas y estudiantes desde la aplicación. La cuenta de superusuario recibe el rol de administrador de la plataforma.

## Verificación funcional

1. Abre el inicio; revisa que carguen CSS y JavaScript.
2. Crea una categoría desde el panel y confirma que aparece en el listado.
3. Registra una empresa y apruébala; crea y aprueba una oferta.
4. Registra un estudiante, postúlate y cambia el estado desde la cuenta de la empresa.
5. Abre el reporte y descarga el CSV.
6. Reinicia el servicio y confirma que los registros siguen disponibles. Si se creó la base Free, recuerda que se elimina al vencer el periodo gratuito.
