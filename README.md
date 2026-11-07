# Plataforma de Prácticas y Oportunidades Laborales

Proyecto académico en Django. El análisis y el diseño están en `docs/`.

## Requisitos

- Python 3.12 o superior compatible con Django 5.2.
- Git.

## Preparación local (Windows PowerShell)

1. Crear un entorno virtual. Si Django ya está instalado en el Python del equipo y no hay acceso a internet, se puede exponer esa instalación con:

   ```powershell
   python -m venv --system-site-packages .venv
   ```

2. Activar el entorno:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Si hay acceso a paquetes, instalar dependencias con `python -m pip install -r requirements.txt`.
4. Copiar `.env.example` como `.env` y establecer una clave secreta local.
5. Definir `AUTH_USER_MODEL = 'cuentas.Usuario'` antes de crear/aplicar migraciones. Ya está configurado en `config/settings.py`.
6. Crear migraciones y aplicar la base de datos:

   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

7. Iniciar el servidor:

   ```powershell
   python manage.py runserver
   ```

El proyecto todavía no tiene datos semilla ni cuentas de prueba; se crearán en la fase de modelos.
