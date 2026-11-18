# BookLoria

Aplicación web hecha con **Python y Django** para explorar la colección de la Biblioteca Pública de Montenegro (Quindío) por categoría de lectura.

> **Estado:** en desarrollo. Este README se actualiza a medida que se completan los issues.

## Problema e hipótesis

Familias, docentes y mediadores de lectura podrían tener dificultad para saber qué lecturas hay en la biblioteca según el tipo de público y el género.

> Esto es una **hipótesis de necesidad**: no fue contrastada con usuarios reales. Los datos solo prueban que existen registros.

**Usuarios:** madres, padres, docentes y mediadores de lectura de Montenegro.

## Funcionalidad

- [x] Ver una lista de libros reales del inventario (página de inicio, primeros 50)
- [x] Explorar libros por categoría de lectura (`/libros/`)
- [x] Filtrar solo libros marcados como infantiles (casilla «Solo infantiles»)

## Fuente de los datos

| Campo | Detalle |
|---|---|
| Conjunto de datos | Activos de Información Biblioteca Pública Montenegro Quindío 2022 |
| ID en datos.gov.co | `hecw-3dai` |
| URL | https://www.datos.gov.co/Cultura/Activos-de-Informaci-n-Biblioteca-P-blica-Monteneg/hecw-3dai/about_data |
| Entidad publicadora | Alcaldía de Montenegro, Quindío |
| Archivo usado | `data/Biblioteca_Montenegro.csv` (4.162 registros, descargado el 13-11-2026) |
| Modalidad de acceso | Archivo descargado (CSV) |

Campos usados: `NOMBRE DEL LIBRO`, `AUTOR`, `GENERO`, `NUMERO` (ejemplares).

## Limitaciones de los datos

- Es un inventario del **20 de noviembre de 2022**. No indica si un libro está disponible hoy.
- El campo `GENERO` tiene 68 valores con errores y variantes; el equipo los normaliza y los agrupa en categorías. **Las categorías son una decisión del equipo, no un dato oficial.**
- No hay edad recomendada. "Infantil" se toma solo de los registros cuyo género lo dice explícitamente (271 registros).
- Los registros `ALBUM` (502) no indican si son infantiles, por lo que **no se clasifican como infantiles**.
- Hay registros sin autor o sin género (`-`) y títulos repetidos, que pueden ser otras copias o ediciones.
- Algunos valores de `GENERO` no son géneros sino nombres de editoriales, instituciones o personas (por ejemplo, `MERCK SHARP` o `RUFFUS`). Se dejan en "Sin clasificar".

## Categorías de lectura

BookLoria agrupa los géneros normalizados del inventario en categorías de lectura para facilitar la exploración.

La clasificación se hace con una tabla de correspondencia definida en `library/services.py` (`GENRE_CATEGORIES`), que relaciona cada género con **una única categoría**.

| Categoría | Libros | Criterio de agrupación |
|---|---|---|
| Literatura | 1.835 | Novelas, cuentos, poesía, antologías, ensayos, mitos y leyendas para adultos, tradición oral, literatura universal y escritores montenegrinos. |
| Ciencias sociales e historia | 612 | Geografía, historia y ciencias sociales (incluye variantes mal escritas del mismo género). |
| Ciencias y tecnología | 508 | Tecnología, ciencias aplicadas, ciencias naturales y matemáticas. |
| Álbumes | 502 | Género `ALBUM`. Se mantiene aparte porque el dato no indica si es infantil. |
| Infantil | 271 | Registros cuyo género dice explícitamente "infantil": novela, poesía, teatro, mitos y leyendas infantiles y enciclopedia infantil. |
| Arte y cultura | 246 | Teatro, dramaturgia, arte, recreación, deporte y manualidades. |
| Braille | 40 | Colección en Braille (género `BRAILLE`). |
| Educación y consulta | 11 | Cartillas, magisterio, valores y material didáctico. |
| Idiomas | 1 | Material de aprendizaje de idiomas (inglés). |
| Sin clasificar | 136 | Género vacío (`-`, 129 registros) o valores que no son géneros ni tienen una correspondencia definida. |

> Los conteos corresponden al inventario de 2022 y deben coincidir con los resultados de `python manage.py test`.

### Criterios de clasificación

- Cada libro recibe exactamente una categoría.
- Se usa el género previamente normalizado (mayúsculas, tildes, espacios y errores de escritura).
- Los géneros que no están en la tabla se asignan a "Sin clasificar".
- La categoría **Infantil** coincide con el filtro "solo infantiles": ambas contienen los mismos 271 registros. La poesía infantil, por ejemplo, aparece en Infantil y no en Literatura.
- El campo `genre` original (normalizado) se conserva junto a `category`.
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

**Último resultado registrado** (`python manage.py test`, 16-11-2026):

```
Found 29 test(s).
Ran 29 tests in 0.670s
OK
```

**Prueba manual en el navegador:** _pendiente — la persona que revise debe abrir `/`, elegir una categoría en `/libros/`, activar «Solo infantiles» y registrar aquí lo que vio._

## Estructura del proyecto

> Ajustar a la estructura real del proyecto base.

```
BookLoria/
├── data/
│   └── biblioteca_montenegro.csv
├── library/
│   ├── services.py      # leer, normalizar y agrupar los datos
│   ├── views.py         # inicio y listado por categoría
│   ├── urls.py
│   ├── tests.py
│   └── templates/library/   # index, books y parciales
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