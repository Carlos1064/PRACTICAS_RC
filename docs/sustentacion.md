# Sustentación: presentación y demo de 10 minutos

La presentación ocupa **3:00 minutos** y la demostración en vivo **7:00 minutos**. Usa las diapositivas de `presentacion.pptx` y ensaya la demo con cronómetro. La cuenta y los datos deben estar preparados antes de iniciar.

## Parte 1 · Diapositivas (3:00)

### Diapositiva 1 — Problema y objetivos (0:00–1:00)

**Problema:** la búsqueda de prácticas y el seguimiento de candidaturas se fragmentan entre portales y comunicaciones independientes. Esto dificulta comparar oportunidades, mantener actualizado el perfil y conocer el estado de una postulación.

**Objetivo general:** desarrollar una plataforma web que centralice ofertas de prácticas y empleo y permita gestionar el proceso de postulación con control por roles.

**Objetivos específicos:**

1. Implementar perfiles para estudiantes y empresas.
2. Permitir publicar y buscar ofertas con filtros y paginación.
3. Gestionar postulaciones con estados y restricciones de acceso.
4. Proveer herramientas administrativas, indicadores y reportes.

### Diapositiva 2 — Arquitectura (1:00–2:15)

Explica el flujo de navegador a Django y base relacional. Señala que las vistas validan permisos y reglas, el ORM consulta SQLite, y las plantillas construyen la respuesta. `fetch` actualiza las ofertas y su paginación sin recargar la página.

### Diapositiva 3 — Valor y transición a demo (2:15–3:00)

Resume: moderación de empresas/ofertas, candidaturas sin duplicados, roles, indicadores y exportación CSV. “Ahora mostraré el flujo real con registros persistidos en la base de datos”.

## Parte 2 · Demostración en vivo (7:00)

| Tiempo | Acción | Qué decir o demostrar |
|---|---|---|
| 0:00–0:45 | Iniciar sesión como estudiante | Presentar el perfil y la navegación según rol. |
| 0:45–1:45 | Explorar ofertas | Escribir una búsqueda y combinar filtros; mostrar paginación y actualización parcial. |
| 1:45–2:40 | Postular y seguir | Abrir una oferta vigente, enviar mensaje opcional y mostrar el registro en Mis postulaciones. |
| 2:40–3:35 | Empresa | Cambiar a empresa aprobada, abrir Mis ofertas y mostrar los postulantes de su oferta; cambiar el estado. |
| 3:35–4:35 | Administración | Aprobar empresa y oferta pendientes (o explicar sus estados con registros preparados); abrir dashboard e indicar cifras. |
| 4:35–5:30 | Persistencia CRUD | Crear una categoría temporal para la demo, editar su nombre y eliminarla. Confirmar visualmente cada cambio. |
| 5:30–6:20 | Reporte | Filtrar postulaciones y descargar CSV. |
| 6:20–7:00 | Cierre técnico | Recordar validaciones por rol, duplicados bloqueados y mensajes visuales. Dejar abierta la página principal. |

### Datos y preparación

- Ejecuta `python manage.py migrate` y `python manage.py seed_demo` en la base preparada.
- Verifica inicio de sesión de `estudiante@demo.local`, `empresa1@demo.local` y `admin@demo.local`; la contraseña de desarrollo está en el README.
- Asegura que haya una empresa y una oferta pendientes para mostrar aprobación. Si la empresa pendiente no tiene oferta, explica el flujo de aprobación de oferta con una oferta pendiente de la empresa aprobada.
- Elige una categoría sin ofertas asociadas para el ejercicio de eliminar y anota su nombre temporal. No borres una categoría usada en ofertas.
- Arranca con `DEBUG=False`, una clave secreta real y `ALLOWED_HOSTS` configurado. Mantén la sesión del administrador lista para reducir cambios de cuenta.
- Ensaya el cambio entre roles o prepara perfiles de navegador separados. El reloj empieza con la primera diapositiva; al minuto 3 inicia la demo y al minuto 10 termina.
- Congela cambios de código el día anterior. Mantén un plan verbal de contingencia si el CDN de gráficos o el Wi-Fi no responde: el panel conserva sus indicadores en texto.

## Material pendiente de ejecución externa

El archivo de diapositivas y este guion están listos localmente. La publicación en GitHub/Padlet requiere un repositorio remoto o el enlace de entrega de la asignatura; el workspace no tiene remoto Git configurado ni acceso a la cuenta del curso. La grabación del video debe realizarse con el equipo de captura del presentador siguiendo `guion-video.md`.
