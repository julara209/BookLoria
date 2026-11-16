# BookLoria

Aplicación web hecha con **Python y Django** para explorar la colección de la Biblioteca Pública de Montenegro (Quindío) por categoría de lectura.

> **Estado:** en desarrollo. Este README se actualiza a medida que se completan los issues.

## Problema y hospotesis

Familias, docentes y mediadores de lectura podrían tener dificultad para saber qué lecturas hay en la biblioteca según el tipo de público y el género.

> Esto es una **hipótesis de necesidad**: no fue contrastada con usuarios reales. Los datos solo prueban que existen registros.

**Usuarios:** madres, padres, docentes y mediadores de lectura de Montenegro.

## Funcionalidad

- [ ] Ver una lista de libros reales del inventario
- [ ] Explorar libros por categoría de lectura
- [ ] Filtrar solo libros marcados como infantiles

## Fuente de los datos

| Campo | Detalle |
|---|---|
| Conjunto de datos | Activos de Información Biblioteca Pública Montenegro Quindío 2022 |
| ID en datos.gov.co | `hecw-3dai` |
| URL | https://www.datos.gov.co/Cultura/Activos-de-Informaci-n-Biblioteca-P-blica-Monteneg/hecw-3dai/about_data |
| Entidad publicadora | Alcaldía de Montenegro, Quindío |
| Archivo usado | `data/biblioteca_montenegro.csv` (4.162 registros, descargado el 13-11-2026) |
| Modalidad de acceso | Archivo descargado (CSV) |

Campos usados: `NOMBRE DEL LIBRO`, `AUTOR`, `GENERO`, `NUMERO` (ejemplares).

## Limitaciones de los datos

- Es un inventario del **20 de noviembre de 2022**. No indica si un libro está disponible hoy.
- El campo `GENERO` tiene 68 valores con errores y variantes; el equipo los normaliza y los agrupa en categorías. **Las categorías son una decisión del equipo, no un dato oficial.**
- No hay edad recomendada. "Infantil" se toma solo de los registros cuyo género lo dice explícitamente.
- Hay registros sin autor o sin género (`-`) y títulos repetidos, que pueden ser otras copias o ediciones.

## Categorías de lectura

BookLoria agrupa los géneros normalizados del inventario en categorías de lectura para facilitar la búsqueda y exploración de los libros.

La clasificación se realiza mediante una tabla de correspondencia definida en `library/services.py`, que relaciona cada género con una única categoría.

| Categoría | Criterio de agrupación |
|---|---|
| Literatura | Novelas, cuentos, poesía, antologías, ensayos, mitos y leyendas para adultos y literatura universal. |
| Infantil y juvenil | Libros y materiales identificados explícitamente como infantiles o juveniles. |
| Arte y cultura | Teatro, dramaturgia, arte, recreación, deporte y manualidades. |
| Ciencias y tecnología | Tecnología, informática, ciencias naturales, matemáticas y medicina. |
| Ciencias sociales e historia | Geografía, historia y ciencias sociales. |
| Educación y consulta | Cartillas, magisterio y materiales educativos o de consulta. |
| Idiomas | Materiales relacionados con el aprendizaje de idiomas, como inglés. |
| Sin clasificar | Géneros vacíos, desconocidos o que no tienen una correspondencia definida. |

### Criterios de clasificación

- Cada libro recibe exactamente una categoría.
- Se utiliza el género previamente normalizado para realizar la clasificación.
- Los géneros que no aparecen en la tabla de correspondencias se asignan a "Sin clasificar".
- Las categorías son una agrupación definida por el equipo y no una clasificación oficial de la biblioteca.

## Requisitos

- Python 3.x (usar la versión indicada en `requirements.txt` o por el instructor)
- Git

## Instalación

```bash
git clone https://github.com/julara209/BookLoria.git
cd BookLoria
python -m venv .venv
```

Activar el entorno virtual:

```bash
# Windows (PowerShell)
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python manage.py runserver
```

Abrir en el navegador: http://127.0.0.1:8000/

## Pruebas

```bash
python manage.py test
```

**Último resultado registrado:** _pendiente — completar con el resultado real (issue #8)._

## Estructura del proyecto

> Ajustar a la estructura real del proyecto base.

```
BookLoria/
├── data/
│   └── biblioteca_montenegro.csv
├── library/
│   ├── services.py      # leer, normalizar y agrupar los datos
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── templates/library/index.html
├── manage.py
├── requirements.txt
└── README.md
```

## Organización del trabajo

- **Tablero (GitHub Project):** https://github.com/users/julara209/projects/5
- **Issues:** https://github.com/julara209/BookLoria/issues
- **Flujo:** Issue → Rama → Commit → Pull Request → Revisión → Integración → Verificación de DoD → Done
- Ramas y commits en inglés. Los Pull Requests usan `Refs #N`, no `Closes #N`.

## Definición de Terminado (DoD)

- [ ] Django inicia sin errores bloqueantes.
- [ ] Desde el navegador se puede elegir una categoría y ver resultados.
- [ ] Los datos vienen del CSV `hecw-3dai`, con la fuente citada en este README.
- [ ] Se cumplen los criterios de aceptación de cada issue.
- [ ] Una categoría sin resultados y un libro sin autor no rompen la página.
- [ ] Se ejecutó `python manage.py test` y se registró el resultado real.
- [ ] Los cambios fueron revisados por otra persona e integrados en `main`.
- [ ] El README explica instalación, ejecución y origen de los datos.
- [ ] Issues y Project reflejan el estado real.

## Equipo

| Nombre | Rol / aportes |
|---|---|
| Angie Espinosa | _completar_ |
| Camilo Zarate | _completar_ |
| Paola Acosta | _completar_ |

## Retrospectiva

_Completar al final: qué funcionó, qué obstáculo afectó más y una acción concreta de mejora._
