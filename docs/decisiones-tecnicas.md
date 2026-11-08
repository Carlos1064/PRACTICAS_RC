# Decisiones técnicas

## Aplicación

Se usa Django en arquitectura MVT: las URL resuelven vistas, las vistas aplican permisos y reglas del negocio, el ORM consulta los modelos y las plantillas renderizan la respuesta. Las cuatro aplicaciones separan cuentas, ofertas, postulaciones y panel administrativo.

## Cuenta de usuario

`Usuario` deriva de las clases de autenticación de Django y usa el correo como identificador de acceso. La contraseña se guarda con el hash de Django. `rol` determina los permisos funcionales; `is_staff` conserva su función específica para el Django Admin. El usuario personalizado se definió antes de las primeras migraciones.

Los perfiles académicos y empresariales se modelan como relaciones uno a uno. Una empresa corresponde a una cuenta de rol empresa y debe ser aprobada para crear ofertas.

## Estados y aprobaciones

- El registro de empresa comienza en pendiente.
- Las ofertas nuevas y editadas comienzan en pendiente.
- La oferta tiene los estados pendiente, publicada, rechazada y cerrada. Se añadió `rechazada` para distinguir la decisión administrativa del cierre operativo.
- Las postulaciones se restringen por una tabla de transiciones en el modelo y la vista valida nuevamente la transición.
- La restricción única en base de datos evita dos postulaciones del mismo estudiante a la misma oferta.

## Integridad y propiedad

- Correo, NIT, categoría y pareja oferta/estudiante tienen unicidad donde corresponde.
- Vacantes debe ser mayor que cero mediante una restricción de base de datos y validación del formulario.
- Ofertas protegen empresa y categoría frente al borrado; las postulaciones conservan su relación con oferta y estudiante.
- Las vistas empresariales limitan los querysets al propietario y responden 403 si otra empresa intenta consultar, editar o cambiar datos ajenos.

## Interfaz y filtros

Las plantillas comparten un layout, mensajes y componentes para campos, paginación, tarjetas y estados. Las opciones de categoría, ciudad y los registros visibles se entregan desde las vistas. La búsqueda de ofertas devuelve HTML parcial con `fetch`, conservando la URL y permitiendo volver con el historial del navegador.

El JavaScript valida primero para dar respuesta rápida; los formularios Django repiten las validaciones en servidor. Los mensajes se presentan en la interfaz. Todas las operaciones que cambian datos son POST con CSRF.

## Base de datos y configuración

SQLite se usa para el desarrollo local. La configuración carga variables desde `.env`; `.env` no se versiona. La llave de ejemplo es un marcador y Django detiene el arranque con `DEBUG=False` si no se configura una llave real. Para sustentar, se debe desactivar debug y definir `ALLOWED_HOSTS`.

Los datos semilla son sintéticos. Las credenciales incluidas sirven únicamente para una base local.

## Reportes

Los indicadores se calculan desde consultas a la base. El CSV usa UTF-8 con BOM y separador punto y coma para facilitar su apertura en Excel configurado en español. Chart.js se carga por CDN y el dashboard conserva un resumen accesible en texto como alternativa.
