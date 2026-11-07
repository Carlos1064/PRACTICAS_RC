# 01. Análisis del sistema

## 1. Nombre provisional

**Plataforma de Prácticas y Oportunidades Laborales**

El nombre es provisional y puede ajustarse cuando se defina la identidad visual del proyecto.

## 2. Problemática

La búsqueda y gestión de oportunidades de prácticas y empleo para estudiantes y egresados puede involucrar información distribuida entre distintos canales, como publicaciones institucionales, páginas de empresas y mensajes directos. Cuando las oportunidades y las postulaciones se administran por separado, resulta más difícil para los aspirantes encontrar vacantes pertinentes y consultar el avance de sus procesos; a las empresas les cuesta organizar las candidaturas recibidas; y a la institución le falta una vista centralizada para acompañar y revisar estas actividades.

Se propone construir una plataforma web que reúna en un solo lugar las ofertas de prácticas y empleo, los perfiles de estudiantes y egresados, y el seguimiento de las postulaciones. Las empresas podrán registrar sus datos y proponer ofertas, sujetas a aprobación administrativa. Los estudiantes y egresados podrán consultar oportunidades vigentes, filtrar resultados y postularse. La administración podrá revisar empresas y ofertas, gestionar categorías y supervisar la información del sistema.

La solución busca facilitar el acceso ordenado a las oportunidades y hacer trazable el proceso de postulación. El alcance de este análisis se basa en el plan del proyecto; no presupone estadísticas institucionales ni afirma que una institución específica tenga actualmente un problema medido. La necesidad concreta y cualquier dato local deberán validarse con la asignatura o con las personas usuarias antes de la sustentación.

## 3. Justificación

Una plataforma centralizada puede reducir la dispersión de la información, ofrecer criterios consistentes de búsqueda y permitir que cada aspirante consulte el estado de sus postulaciones. También puede ayudar a las empresas a revisar candidaturas desde un espacio organizado y dar al administrador herramientas para mantener la calidad de las publicaciones. El proyecto integra desarrollo web con Django, persistencia relacional, control de acceso por roles, validación de formularios y diseño adaptable, por lo que permite demostrar tanto la utilidad funcional como los conceptos técnicos del curso.

## 4. Actores y roles

| Actor | Descripción y responsabilidades |
|---|---|
| Estudiante/Egresado | Crea y actualiza su perfil, consulta ofertas publicadas y vigentes, se postula y revisa o retira sus postulaciones. |
| Empresa | Registra su organización, espera aprobación administrativa, administra su perfil y, una vez aprobada, crea y gestiona ofertas y revisa postulantes de sus propias ofertas. |
| Administrador | Gestiona usuarios y categorías, revisa y aprueba o rechaza empresas y ofertas, y consulta indicadores e informes del sistema. |
| Visitante | Consulta la página pública y las ofertas disponibles. Para postularse debe registrarse e iniciar sesión como estudiante/egresado. |

## 5. Objetivos

### Objetivo general

Desarrollar una plataforma web con Django que centralice la publicación y consulta de oportunidades de prácticas y empleo, así como la gestión y el seguimiento de postulaciones para estudiantes/egresados, empresas y administradores.

### Objetivos específicos

1. Diseñar e implementar una base de datos relacional que represente usuarios, perfiles, empresas, categorías, ofertas y postulaciones, aplicando relaciones y restricciones de integridad.
2. Implementar registro, autenticación y control de acceso según los roles de estudiante/egresado, empresa y administrador.
3. Permitir que las empresas aprobadas creen y administren ofertas, y que el administrador revise las solicitudes de empresas y ofertas antes de su publicación.
4. Facilitar la búsqueda de ofertas vigentes mediante texto y filtros, con resultados paginados y una interfaz adaptable a dispositivos móviles.
5. Gestionar el ciclo de las postulaciones, evitando duplicados y permitiendo que el estudiante consulte su estado y que la empresa responsable actualice el proceso.

## 6. Historias de usuario

Prioridades: **Alta** = necesaria para el flujo central; **Media** = aporta gestión y seguimiento; **Baja** = complemento útil que no bloquea el alcance mínimo.

| ID | Prioridad | Historia de usuario | Criterio de aceptación resumido |
|---|---|---|---|
| HU-01 | Alta | Como estudiante o egresado, quiero crear una cuenta y completar mi perfil para presentar mi formación a las empresas. | El sistema valida los campos requeridos y el correo único; el perfil queda asociado a la cuenta. |
| HU-02 | Alta | Como representante de una empresa, quiero registrar mi cuenta y los datos de mi organización para solicitar acceso a la plataforma. | La empresa se crea en estado pendiente y no puede publicar ofertas antes de su aprobación. |
| HU-03 | Alta | Como usuario registrado, quiero iniciar y cerrar sesión para acceder de forma segura a las funciones de mi rol. | La autenticación funciona y las vistas restringidas comprueban el rol correspondiente. |
| HU-04 | Alta | Como administrador, quiero revisar y aprobar o rechazar empresas para controlar quién publica oportunidades. | Puedo consultar empresas pendientes y registrar una decisión. |
| HU-05 | Alta | Como empresa aprobada, quiero crear una oferta para presentar una oportunidad a estudiantes y egresados. | La oferta valida sus datos y queda pendiente de aprobación administrativa. |
| HU-06 | Alta | Como administrador, quiero aprobar o rechazar ofertas para asegurar que solo las autorizadas aparezcan como publicadas. | Las ofertas pendientes pueden revisarse y su estado se actualiza según la decisión. |
| HU-07 | Alta | Como estudiante o egresado, quiero buscar y filtrar ofertas vigentes para encontrar oportunidades acordes con mis intereses. | Puedo buscar por texto y filtrar por tipo, categoría, modalidad o ciudad; los resultados se paginan. |
| HU-08 | Alta | Como estudiante o egresado, quiero postularme a una oferta vigente para expresar mi interés en ella. | Se registra una sola postulación por estudiante y oferta; no se acepta una oferta cerrada o vencida. |
| HU-09 | Media | Como estudiante o egresado, quiero consultar y retirar mis postulaciones para hacer seguimiento a mis procesos. | Veo el estado de cada postulación y puedo retirar una que todavía corresponda según las reglas del sistema. |
| HU-10 | Alta | Como empresa, quiero revisar las postulaciones recibidas para gestionar el proceso de selección de mis ofertas. | Solo puedo ver candidatos de ofertas que pertenecen a mi empresa y actualizar estados permitidos. |
| HU-11 | Media | Como administrador, quiero gestionar categorías y cuentas de usuario para mantener organizada y moderada la plataforma. | Puedo buscar, paginar y ejecutar las acciones autorizadas sobre categorías y usuarios. |
| HU-12 | Baja | Como administrador, quiero consultar indicadores y exportar un reporte de postulaciones para revisar la actividad de la plataforma. | Los indicadores se calculan con datos almacenados y el reporte puede descargarse en CSV con filtros disponibles. |

## 7. Reglas de negocio

1. Cada correo de usuario debe ser único.
2. Una empresa recién registrada queda en estado **pendiente** hasta que el administrador la apruebe o rechace.
3. Solo una empresa aprobada puede crear ofertas.
4. Toda oferta nueva queda en estado **pendiente** y solo se muestra como publicada tras la aprobación administrativa.
5. Una empresa solo puede consultar y editar sus propios datos, ofertas y postulaciones asociadas a sus ofertas.
6. Un estudiante/egresado no puede postularse más de una vez a la misma oferta.
7. Solo se aceptan postulaciones a ofertas publicadas, abiertas y cuya fecha límite no haya vencido.
8. Una oferta cerrada o vencida no admite nuevas postulaciones.
9. Solo la empresa propietaria de una oferta puede revisar y cambiar el estado de las postulaciones asociadas, respetando las transiciones permitidas.
10. Un usuario solo puede ejecutar las acciones habilitadas para su rol; el administrador cuenta con las funciones de gestión asignadas.
11. Los campos marcados como obligatorios deben validarse tanto en el navegador como en el servidor.
12. Las acciones importantes informan su resultado mediante mensajes visuales dentro de la interfaz.

## 8. Alcance

### Incluido en el alcance mínimo

- Registro, inicio y cierre de sesión para estudiantes/egresados y empresas.
- Perfiles de estudiante/egresado y empresa.
- Aprobación administrativa de empresas y ofertas.
- CRUD de categorías para administración.
- CRUD básico de ofertas para empresas aprobadas, con cierre de ofertas.
- Consulta de ofertas publicadas y vigentes con búsqueda, filtros y paginación.
- Postulación, prevención de duplicados y consulta/gestión de estados.
- Control de acceso por rol, validaciones de formularios y mensajes de resultado.
- Panel administrativo con indicadores y reporte CSV, sujeto al tiempo disponible del plan.
- Interfaz adaptable, páginas de error propias y documentación del proyecto.

### Fuera del alcance mínimo; posibles extras

- Notificaciones por correo electrónico.
- Favoritos o alertas personalizadas de nuevas ofertas.
- Carga y almacenamiento de archivos PDF para hojas de vida.
- Integraciones con bolsas de empleo externas, redes profesionales o sistemas institucionales.
- Aplicación móvil nativa.

## 9. Supuestos y aspectos por validar

- El proyecto se desarrolla como ejercicio académico y se dirige a estudiantes/egresados y empresas interesadas en oportunidades de prácticas o empleo.
- El plan no especifica una institución, programa académico, cifras de usuarios ni canales actuales; por ello, la problemática se formula de manera general y no incluye datos cuantitativos inventados.
- Los estados de postulación y sus transiciones concretas se definirán durante el diseño, respetando los estados enumerados en el plan general.
- La publicación del entregable en el Padlet requiere conocer el espacio o enlace de la asignatura y disponer del acceso correspondiente.

## 10. Estado del entregable

Este documento completa el análisis base de la Fase 1. Antes de usarlo como descripción institucional definitiva, conviene reemplazar o complementar la problemática general con el contexto real de la asignatura y validar los supuestos indicados.
