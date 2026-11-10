# Mapa de URLs y vistas

Las rutas usan nombres Django estables y nombres de espacio por aplicación. Toda operación que modifica datos usa POST con CSRF. Las rutas de administración de la plataforma comprueban autenticación y rol; las vistas de empresa filtran por la empresa asociada al usuario actual.

| Método | URL | Nombre | Vista / responsabilidad | Acceso | Plantilla o respuesta |
|---|---|---|---|---|---|
| GET | `/` | `inicio` | Inicio y resumen de ofertas destacadas | Público | `inicio.html` |
| GET | `/cuentas/registro/` | `cuentas:registro` | Selección de tipo de cuenta | Público | `cuentas/registro.html` |
| GET, POST | `/cuentas/registro/estudiante/` | `cuentas:registro_estudiante` | Crear usuario y perfil de estudiante | Público | `cuentas/registro_estudiante.html` |
| GET, POST | `/cuentas/registro/empresa/` | `cuentas:registro_empresa` | Crear usuario y empresa pendiente | Público | `cuentas/registro_empresa.html` |
| GET, POST | `/cuentas/ingresar/` | `cuentas:login` | Autenticar y redirigir según rol | Público | `cuentas/login.html` |
| POST | `/cuentas/salir/` | `cuentas:logout` | Cerrar sesión | Usuario autenticado | Redirección a inicio |
| GET | `/cuentas/perfil/` | `cuentas:perfil` | Ver perfil propio según rol | Autenticado | Plantilla según rol |
| GET, POST | `/cuentas/perfil/editar/` | `cuentas:perfil_editar` | Editar perfil propio | Estudiante o empresa | Formulario correspondiente |
| GET | `/ofertas/` | `ofertas:lista` | Buscar, filtrar y paginar ofertas vigentes; admite respuesta parcial para `fetch` | Público | `ofertas/lista.html` o parcial de resultados |
| GET | `/ofertas/<id>/` | `ofertas:detalle` | Detalle de una oferta publicada | Público | `ofertas/detalle.html` |
| GET | `/empresa/ofertas/` | `ofertas:mis_ofertas` | Listar ofertas de la empresa actual | Empresa | `ofertas/empresa/lista.html` |
| GET, POST | `/empresa/ofertas/nueva/` | `ofertas:crear` | Crear oferta pendiente | Empresa aprobada | `ofertas/empresa/formulario.html` |
| GET, POST | `/empresa/ofertas/<id>/editar/` | `ofertas:editar` | Editar oferta propia según estado | Dueña de oferta | Formulario |
| POST | `/empresa/ofertas/<id>/cerrar/` | `ofertas:cerrar` | Cerrar oferta propia | Dueña de oferta | Redirección con mensaje |
| GET | `/empresa/ofertas/<id>/postulantes/` | `postulaciones:postulantes` | Lista paginada y filtrable de candidaturas | Dueña de oferta | `postulaciones/empresa/lista.html` |
| GET, POST | `/empresa/postulaciones/<id>/estado/` | `postulaciones:cambiar_estado` | Cambiar estado de candidatura | Empresa dueña | Redirección con mensaje |
| GET, POST | `/ofertas/<id>/postular/` | `postulaciones:crear` | Crear postulación, comprobar duplicado/fecha/estado | Estudiante autenticado | Procesa y redirige al detalle |
| GET | `/cuentas/postulaciones/` | `postulaciones:mis_postulaciones` | Lista paginada de postulaciones propias | Estudiante autenticado | `postulaciones/mis_lista.html` |
| POST | `/cuentas/postulaciones/<id>/retirar/` | `postulaciones:retirar` | Retirar postulación propia si es válido | Estudiante propietario | Redirección con mensaje |
| GET | `/admin-plataforma/` | `panel:dashboard` | Indicadores calculados desde la BD | Administrador | `panel/dashboard.html` |
| GET | `/admin-plataforma/empresas/pendientes/` | `cuentas:empresas_pendientes` | Listar y paginar empresas pendientes | Administrador | `cuentas/admin/empresas.html` |
| POST | `/admin-plataforma/empresas/<id>/decision/` | `cuentas:decision_empresa` | Aprobar o rechazar empresa | Administrador | Redirección con mensaje |
| GET | `/admin-plataforma/ofertas/pendientes/` | `ofertas:pendientes` | Listar y paginar ofertas pendientes | Administrador | `ofertas/admin/pendientes.html` |
| POST | `/admin-plataforma/ofertas/<id>/decision/` | `ofertas:decision` | Aprobar o rechazar oferta | Administrador | Redirección con mensaje |
| GET | `/admin-plataforma/categorias/` | `ofertas:categorias` | Buscar y paginar categorías | Administrador | `ofertas/admin/categorias_lista.html` |
| GET, POST | `/admin-plataforma/categorias/nueva/` | `ofertas:categoria_crear` | Crear categoría | Administrador | Formulario |
| GET, POST | `/admin-plataforma/categorias/<id>/editar/` | `ofertas:categoria_editar` | Editar categoría | Administrador | Formulario |
| POST | `/admin-plataforma/categorias/<id>/eliminar/` | `ofertas:categoria_eliminar` | Eliminar categoría con confirmación y control de referencias | Administrador | Redirección con mensaje |
| GET | `/admin-plataforma/usuarios/` | `cuentas:usuarios` | Buscar y paginar usuarios | Administrador | `cuentas/admin/usuarios.html` |
| POST | `/admin-plataforma/usuarios/<id>/estado/` | `cuentas:usuario_estado` | Activar o desactivar cuenta | Administrador | Redirección con mensaje |
| GET | `/admin-plataforma/reportes/postulaciones/` | `panel:reporte` | Reporte filtrable y paginado | Administrador | `panel/reporte.html` |
| GET | `/admin-plataforma/reportes/postulaciones.csv` | `panel:reporte_csv` | Exportar resultados filtrados | Administrador | CSV |
| GET | `/403/` | `error_403` | Acceso denegado | Público | `403.html` |
| GET | Ruta inexistente | `handler404` | Recurso no encontrado | Público | `404.html` |
| Error interno | — | `handler500` | Error inesperado | Público | `500.html` |

## Notas de implementación

- El parámetro `page` conserva los filtros al navegar la paginación. Para la búsqueda dinámica, la vista de listado renderiza el mismo parcial cuando la petición pide resultados para `fetch`.
- El cierre de sesión, la retirada, las decisiones administrativas y las acciones de estado son POST para evitar cambios por enlaces GET.
- Los identificadores se consultan dentro de un queryset limitado por el propietario. Si un usuario de empresa intenta acceder a un recurso ajeno, se responde con 403.
- El administrador del sitio puede usar el admin de Django durante desarrollo; las funciones presentadas al usuario se implementan en las vistas del panel y aplican las reglas del proyecto.
