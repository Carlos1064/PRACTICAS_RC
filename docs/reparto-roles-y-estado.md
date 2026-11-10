# Reparto de roles y estado reconstruido

Este documento aplica ingeniería inversa al repositorio y convierte los roles del archivo **“Plan de entregables — Plataforma de Prácticas y Oportunidades Laborales”** en responsabilidades concretas sobre la implementación existente.

## Arquitectura que realmente se construyó

El plan inicial propone React/FastAPI y JWT como alternativas. El repositorio implementa una aplicación **Django MVT**: las vistas, permisos, formularios y ORM resuelven el backend; las plantillas Django, CSS y JavaScript componen el frontend; Django gestiona las sesiones. Por eso, el reparto se basa en los módulos reales y no presupone una API REST, JWT ni carpetas `frontend/` y `backend/`.

Flujo reconstruido: **navegador → URLs → vistas/permisos/formularios → ORM/modelos → SQLite o PostgreSQL → plantillas/HTML**. La búsqueda de ofertas actualiza resultados con `fetch`.

## Asignación por integrante

| Integrante y rol del plan | Responsabilidad en este proyecto | Archivos y entregables relacionados | Estado según el repositorio |
|---|---|---|---|
| **Carlos — Líder/Analista** | Mantener alcance e historias; coordinar integración y revisiones; definir criterios de aceptación; consolidar pruebas, documentación técnica y sustentación. | `docs/01-analisis.md`, `docs/02-diseño/`, `docs/pruebas/matriz-pruebas.md`, `docs/sustentacion.md`, `README.md`, `docs/decisiones-tecnicas.md` | **Documentado:** análisis, modelo, arquitectura, mapa de URLs, matriz, manual y guion están en el repo. La coordinación diaria, revisión de PR y presentación del equipo ocurren fuera del código y requieren confirmación del equipo. |
| **Santiago — UX/UI** | Mantener navegación comprensible por rol; revisar consistencia visual, estados vacíos/errores/éxito y adaptación móvil; aportar capturas y observaciones de usabilidad. | `docs/02-diseño/03-wireframes.md`, `docs/manual-usuario.md`, `docs/manual-usuario/imagenes/`, revisión de `templates/` y `static/css/app.css` | **Documentado:** hay wireframes y capturas del manual; la interfaz y los estados visuales existen. El archivo fuente de Figma, pruebas con usuarios y registro de comentarios no aparecen en este repositorio; confirmar si se entregaron externamente. |
| **Emily — Frontend** | Mantener plantillas, estilos, JavaScript e interacción; conectar pantallas con vistas Django; cuidar accesibilidad, mensajes y responsive; corregir la cuadrícula de ofertas y verificarla en escritorio/móvil. | `templates/`, `static/css/app.css`, `static/js/`, `docs/manual-usuario/imagenes/` | **Implementado:** pantallas para los tres roles, búsqueda con filtros/paginación dinámica, formularios, dashboard, reporte y exportación visual. **En seguimiento:** comprobar en el sitio desplegado la corrección visual de la cuadrícula de ofertas tras cada despliegue. |
| **Andrea — Backend** | Mantener modelos, reglas de negocio, validación del servidor, autenticación/permisos, persistencia, consultas, reportes y configuración de despliegue. | `cuentas/`, `ofertas/`, `postulaciones/`, `panel/`, `config/`, `build.sh`, `requirements.txt` | **Implementado:** cuentas y perfiles, empresas y aprobación, categorías, ofertas y aprobación, postulaciones con estados y restricciones, panel/reportes, SQLite local y PostgreSQL por configuración. |

## Reparto por módulo y puntos de integración

| Módulo o flujo | Responsable principal | Apoyo / revisión | Evidencia implementada |
|---|---|---|---|
| Requisitos, historias, alcance y aceptación | Carlos | Todos aportan necesidades de su módulo | `docs/01-analisis.md`, README y documentación de diseño |
| Diseño, navegación, responsive y estados | Santiago | Emily implementa; Carlos valida contra requisitos | Wireframes, `templates/`, `static/css/app.css` |
| Registro, ingreso, perfiles y permisos | Andrea (lógica/datos) | Emily (pantallas); Santiago (revisión de interacción); Carlos (criterios) | `cuentas/`, `templates/cuentas/` |
| Explorar y ver ofertas | Andrea (consulta/filtros) | Emily (plantillas/JS/CSS); Santiago (diseño); Carlos (aceptación) | `ofertas/views.py`, `templates/ofertas/`, `static/js/ofertas.js` |
| Crear, editar, cerrar y aprobar ofertas | Andrea | Emily + Santiago; Carlos revisa flujo | `ofertas/`, `cuentas/admin_urls.py`, plantillas de ofertas y administración |
| Postulaciones y cambios de estado | Andrea | Emily para vistas; Santiago para claridad de estados; Carlos para casos de prueba | `postulaciones/`, `templates/postulaciones/` |
| Dashboard, filtros de reporte y CSV | Andrea (consultas/datos) | Emily (presentación); Santiago (legibilidad); Carlos (validación del entregable) | `panel/`, `templates/panel/`, `static/js/dashboard.js` |
| Pruebas funcionales y regresión | Carlos coordina | Cada responsable ejecuta casos de su módulo; revisión cruzada | `docs/pruebas/matriz-pruebas.md` y pruebas Django en cada app |
| Manual, evidencias y sustentación | Carlos consolida | Santiago capturas/diseño; Emily y Andrea explican sus módulos; todos ensayan un flujo por rol | `docs/manual-usuario.md`, `docs/sustentacion.md`, `docs/guion-video.md`, `docs/presentacion.pptx` |

## Estado reconstruido frente a los entregables del plan

### Hecho en el código o la documentación

- Tres roles: estudiante, empresa y administrador; navegación y permisos asociados.
- Registro, ingreso, perfil de estudiante y perfil de empresa.
- Empresas y ofertas con estados de aprobación; categorías administrables.
- Búsqueda con filtros, paginación de nueve resultados y actualización parcial.
- Postulación, prevención de duplicados, retiro y seguimiento de estados.
- Gestión empresarial de ofertas y postulantes, con límites de propiedad.
- Dashboard, filtros de reporte y descarga CSV.
- Validación del lado servidor y cliente, páginas 403/404/500, guía de instalación, documentación de arquitectura y pruebas.
- Configuración de despliegue con PostgreSQL y carga opcional de datos de demostración.

### Requiere confirmación fuera del repositorio

- Padlet, tablero de tareas, entrevistas de validación y registro de reuniones del plan.
- Prototipo Figma original y revisiones/comentarios de UI en Pull Requests.
- Evidencia de pruebas de usabilidad con participantes.
- Reparto de tiempos de exposición y ensayo real de cada integrante.
- Validación visual final de la cuadrícula de ofertas en el despliegue; el CSS local está fijado en `grid-template` de tres columnas para escritorio y una en móvil, pero el navegador del usuario debe mostrar la versión desplegada correspondiente.

Estas evidencias no se marcan como fallidas: no pueden inferirse solo leyendo el código.

## Orden de trabajo recomendado para cerrar la entrega

1. **Emily + Santiago:** comprobar la cuadrícula de ofertas en escritorio y móvil en la versión desplegada; registrar captura y ancho de pantalla. Emily corrige CSS/plantilla; Santiago verifica el diseño.
2. **Andrea:** revisar las reglas del flujo completo y la configuración de datos del entorno de demostración; dejar instrucciones reproducibles sin credenciales.
3. **Carlos:** recorrer la matriz de pruebas con el equipo, registrar resultados actuales y asignar cualquier incidencia a su responsable.
4. **Santiago + Carlos:** confirmar si Figma, Padlet, tablero y pruebas de usabilidad se entregaron por fuera; completar las evidencias faltantes si la asignatura las exige.
5. **Todos:** ensayar el flujo estudiante → empresa → administrador siguiendo `docs/sustentacion.md`; cada integrante explica su parte.

## Criterio de cierre

Una tarea se considera cerrada cuando su responsable la implementa o documenta, otra persona revisa el resultado, la prueba correspondiente queda registrada y el cambio integrado permite seguir el flujo por rol. Los cambios se asignan por módulo; la revisión cruzada evita que quien implementó sea la única persona que valide.
