# Wireframes iniciales

Bocetos de baja fidelidad para definir jerarquía y comportamiento antes del CSS. En móvil, los filtros se muestran en un panel plegable y las tarjetas se apilan en una columna. Los textos y opciones que dependan del sistema se renderizan desde la base de datos.

## Inicio y listado de ofertas (público/estudiante)

```text
┌──────────────────────────────────────────────────────────┐
│ Marca       Ofertas   Ingresar   Crear cuenta             │
├──────────────────────────────────────────────────────────┤
│ Encuentra tu próxima oportunidad                          │
│ [ Buscar por cargo, empresa o palabra clave... ] [Buscar] │
│ [Tipo v] [Categoría v] [Modalidad v] [Ciudad v]           │
├─────────────────────────────┬────────────────────────────┤
│ Ofertas (N resultados)      │                            │
│ ┌─────────────────────────┐ │ Ordenar: [Más recientes v]│
│ │ Título             Nueva│ │                            │
│ │ Empresa · Ciudad        │ │                            │
│ │ Modalidad · Tipo        │ │                            │
│ │ Fecha límite   [Ver]    │ │                            │
│ └─────────────────────────┘ │                            │
│ ...                         │                            │
│ [Anterior] 1 2 3 [Siguiente]│                            │
└─────────────────────────────┴────────────────────────────┘
```

La columna lateral se convierte en filtros plegables en pantallas estrechas. Al cambiar filtros, `fetch` reemplaza resultados y paginación conservando el estado visual.

## Detalle de oferta y postulación

```text
┌──────────────────────────────────────────────────────────┐
│ Marca       Ofertas   Mis postulaciones   Mi perfil      │
├───────────────────────────────────┬──────────────────────┤
│ [Práctica] [Híbrida]              │ Resumen              │
│ Título de la oportunidad          │ Empresa              │
│ Empresa · Ciudad                  │ Ciudad               │
│ Descripción                       │ Modalidad             │
│ Requisitos                        │ Vacantes              │
│ Categoría                         │ Fecha límite          │
│                                   │ [Postularme]          │
└───────────────────────────────────┴──────────────────────┘
```

El botón muestra el estado correspondiente si la oferta venció, está cerrada o el usuario ya se postuló. Para visitante, dirige al ingreso o registro.

## Formularios de ingreso y registro

```text
┌──────────────────────────────────────────────┐
│ Marca                                        │
│ Crear cuenta                                │
│ [Estudiante/Egresado] [Empresa]              │
│ Nombre completo *                            │
│ Correo electrónico *                         │
│ Contraseña *                                 │
│ Confirmar contraseña *                       │
│ [Crear cuenta]                               │
│ ¿Ya tienes cuenta? Ingresar                  │
└──────────────────────────────────────────────┘
```

El registro empresarial añade razón social, NIT, sector, ciudad y descripción. El formulario de estudiante añade programa, semestre y ciudad. Los errores aparecen junto a los campos y mediante un mensaje visual global.

## Área del estudiante

```text
┌──────────────────────────────────────────────────────────┐
│ Marca       Ofertas   Mis postulaciones   Mi perfil       │
├──────────────────────────────────────────────────────────┤
│ Hola, [nombre]                                            │
│ [Completar/editar perfil]                                 │
│ Mis postulaciones                                         │
│ Oferta              Empresa        Estado       Fecha     │
│ Analista junior     Empresa A      En revisión  12/05     │
│ ...                                                       │
│ [Anterior] 1 [Siguiente]                                  │
└──────────────────────────────────────────────────────────┘
```

## Área de empresa

```text
┌──────────────────────────────────────────────────────────┐
│ Marca       Panel   Mis ofertas   Perfil                 │
├──────────────────────────────────────────────────────────┤
│ Estado de empresa: [Pendiente / Aprobada]                 │
│ [Nueva oferta] (solo habilitada al aprobarse)             │
│ Mis ofertas                                               │
│ Título             Estado       Fecha límite  Acciones    │
│ Diseñador UX       Pendiente    20/06         Editar      │
│ ...                                           Postulantes │
└──────────────────────────────────────────────────────────┘
```

La tabla cambia a tarjetas en móvil. Las acciones solo se ofrecen para recursos propios.

## Panel administrativo

```text
┌──────────────────────────────────────────────────────────┐
│ Marca       Resumen  Aprobaciones  Categorías  Usuarios   │
├──────────────────────────────────────────────────────────┤
│ [Empresas activas] [Ofertas publicadas] [Postulaciones]   │
│ Ofertas por categoría        Postulaciones por estado      │
│ [gráfico desde datos BD]     [gráfico desde datos BD]     │
│ Pendientes: empresas (n) · ofertas (n)                    │
│ [Revisar empresas] [Revisar ofertas]                      │
└──────────────────────────────────────────────────────────┘
```

Los gráficos y contadores se alimentan con consultas a la base de datos. La administración de categorías, usuarios y reportes comparte encabezado, navegación y componentes de tabla paginada.
