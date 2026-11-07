# Matriz de pruebas

Proyecto: Plataforma de Prácticas y Oportunidades Laborales. La ejecución se realizó con la base temporal del framework de pruebas de Django; la base local de demostración no se modifica.

| ID | Módulo | Caso y pasos | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|---|
| TC-01 | Cuentas | Enviar correo y contraseña incorrectos al ingreso. | Mantener al usuario anónimo y mostrar un error comprensible. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-02 | Cuentas | Registrar estudiante con datos válidos. | Crear usuario con contraseña cifrada y perfil asociado. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-03 | Cuentas | Registrar empresa con datos válidos. | Crear cuenta y empresa en estado pendiente. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-04 | Permisos | Abrir gestión de categorías como estudiante. | Responder 403 con página propia. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-05 | Aprobaciones | Aprobar una empresa pendiente como administrador. | Cambiar el estado a aprobada. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-06 | Ofertas | Crear oferta con empresa aprobada. | Guardar oferta en estado pendiente. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-07 | Validación | Enviar una fecha límite pasada al formulario de oferta. | Rechazar el formulario y mostrar error de fecha. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-08 | Búsqueda | Buscar una oferta con petición AJAX. | Filtrar resultados y devolver solo el parcial. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-09 | Paginación | Consultar 11 ofertas con tamaño de página 9. | Mostrar nueve registros en la primera página y dos en la segunda. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-10 | Ofertas | Intentar crear oferta con empresa pendiente. | No crearla y avisar que falta aprobación. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-11 | Propiedad | Intentar editar y cerrar oferta de otra empresa. | Rechazar ambas acciones con 403. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-12 | Postulaciones | Enviar dos veces postulación a la misma oferta. | Conservar una sola postulación y avisar del duplicado. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-13 | Postulaciones | Postularse a oferta cerrada o vencida. | No crear postulaciones y mostrar el bloqueo. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-14 | Postulaciones | Retirar postulación propia activa. | Cambiar estado a retirada. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-15 | Privacidad | Empresa ajena solicita lista o perfil de postulante. | Responder 403 sin entregar datos. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-16 | Postulaciones | Empresa dueña cambia enviada a en revisión. | Aplicar la transición válida. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-17 | Postulaciones | Empresa dueña intenta cambiar enviada a contratada. | Rechazar la transición y conservar el estado. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-18 | Errores | Abrir 403, 404 y provocar 500 con `DEBUG=False`. | Mostrar páginas propias sin traceback ni detalle interno. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-19 | Reportes | Exportar postulaciones a CSV. | Entregar CSV UTF-8 con BOM y datos de la base. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |
| TC-20 | Reportes | Filtrar reporte por categoría y periodo. | Devolver solo los registros coincidentes, paginados. | Cumplió el resultado esperado en la prueba automatizada. | Aprobado |

| TC-21 | Formularios | Enviar vacíos ingreso, registros, perfiles, categoría, oferta y cambio de estado. | Mostrar errores junto a los campos requeridos y no guardar datos incompletos. | Verificado en las pruebas automatizadas de cada formulario. | Aprobado |