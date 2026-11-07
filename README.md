# Plataforma de Prácticas y Oportunidades Laborales

Proyecto académico en Django. El análisis y el diseño están en `docs/`.

## Requisitos

- Python 3.12 o superior compatible con Django 5.2.
- Git.

## Preparación local (Windows PowerShell)

1. Crear y activar un entorno virtual:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   Si Django ya está instalado en el Python del equipo y no hay acceso a internet, agregar `--system-site-packages` al crear el entorno.

2. Instalar las dependencias: `python -m pip install -r requirements.txt`.
3. Copiar `.env.example` como `.env` y definir una clave secreta local.
4. El modelo personalizado `cuentas.Usuario` ya está configurado como `AUTH_USER_MODEL`; debe permanecer definido antes de aplicar migraciones.
5. Crear/aplicar migraciones (necesario al instalar en una base vacía):

   ```powershell
   python manage.py migrate
   ```

6. Cargar los datos de demostración:

   ```powershell
   python manage.py seed_demo
   ```

7. Iniciar el servidor:

   ```powershell
   python manage.py runserver
   ```

## Cuentas locales de demostración

El seed crea cuentas para estudiante, dos empresas y administrador. La contraseña compartida es `PracticasDemo2026!`.

- `estudiante@demo.local`
- `empresa1@demo.local`
- `empresa2@demo.local`
- `admin@demo.local`

Estas credenciales son únicamente para desarrollo local. El comando `seed_demo` se puede volver a ejecutar; actualiza sus registros de demostración y no duplica categorías ni ofertas.
