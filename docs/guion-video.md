# Guion del video del proyecto (máximo 10 minutos)

Duración objetivo: **9 minutos y 30 segundos**. Graba la pantalla a 1080p, activa el cursor visible y deja los datos demo preparados. No muestres la contraseña en pantalla; inicia las sesiones antes de grabar o escríbela fuera de la captura.

## 0:00–1:00 · Problema y propósito

**En pantalla:** portada de la aplicación y luego la búsqueda pública.

**Narración:** “Encontrar una práctica y hacer seguimiento a una candidatura suele implicar consultar varios canales y comunicarse por separado con cada empresa. Esta plataforma concentra ofertas, perfiles y postulaciones en un solo lugar. Las empresas registran oportunidades, el equipo administrador revisa empresas y ofertas, y los estudiantes buscan y siguen sus candidaturas. El objetivo es hacer ese proceso más claro y verificable.”

## 1:00–6:00 · Recorrido funcional por rol

### Estudiante · 1:00–2:40

**En pantalla:** búsqueda de ofertas, filtros, detalle, postulación y “Mis postulaciones”.

**Narración:** “Como estudiante puedo filtrar por texto, tipo, categoría, modalidad y ciudad. Los resultados y la paginación se actualizan sin recargar la página. Abro una oferta para revisar requisitos y fecha límite, envío una postulación y consulto su estado en Mis postulaciones. El sistema impide duplicar la candidatura y bloquea ofertas cerradas o vencidas.”

### Empresa · 2:40–4:10

**En pantalla:** perfil empresarial, Mis ofertas, postulantes y perfil del candidato.

**Narración:** “La cuenta empresarial queda pendiente hasta la aprobación administrativa. Después puede crear ofertas; cada oferta requiere aprobación antes de aparecer al público. En una oferta propia reviso candidatos, consulto su perfil y mensaje, y cambio el estado de la postulación. Los permisos limitan esta vista a la empresa propietaria.”

### Administrador · 4:10–6:00

**En pantalla:** dashboard, aprobación de empresa y oferta, categorías, usuarios y reporte.

**Narración:** “El administrador revisa solicitudes de empresas y ofertas, gestiona categorías y usuarios, y consulta indicadores que se calculan desde la base de datos. El reporte puede filtrarse y descargarse como CSV. Los mensajes de éxito y error se muestran dentro de la interfaz.”

## 6:00–9:00 · Explicación general del código

**En pantalla:** editor con árbol de carpetas, modelos, vista de búsqueda, plantilla y JavaScript de filtros.

**Narración:** “El proyecto usa Django con arquitectura MVT. `cuentas` contiene el usuario personalizado y sus perfiles; `ofertas` implementa categorías, publicación y búsqueda; `postulaciones` controla candidaturas y transiciones; `panel` reúne indicadores y reportes. Las rutas dirigen a vistas que aplican permisos y consultan modelos mediante el ORM. Las plantillas renderizan la interfaz y componentes compartidos. En la búsqueda, JavaScript envía los filtros con `fetch` y reemplaza el fragmento de resultados; el servidor valida los parámetros y devuelve HTML. Las reglas también se validan en servidor, y la base de datos impone unicidad para evitar candidaturas duplicadas.”

## 9:00–9:30 · Cierre

**En pantalla:** vuelve a la página principal y muestra el repositorio local/documentación.

**Narración:** “La plataforma integra publicación moderada, búsqueda dinámica y seguimiento de postulaciones, con permisos por rol y datos persistentes. El README y el manual explican cómo instalarla y utilizarla. Gracias.”

## Lista de control antes de grabar

- Carga `seed_demo` y comprueba que existan las tres cuentas de rol y las ofertas de demostración.
- Ejecuta `python manage.py check` y las pruebas automatizadas.
- Usa `DEBUG=False` con una clave secreta real y `ALLOWED_HOSTS` configurado para la grabación.
- Cierra ventanas y notificaciones ajenas al proyecto; oculta datos personales y la contraseña demo.
- Ensaya el recorrido con cronómetro una vez; mantén el video por debajo de 10 minutos.
- Graba una prueba breve de audio y verifica que el texto y cursor se lean antes de hacer la toma final.
