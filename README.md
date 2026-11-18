# BookLoria

Aplicación web hecha con **Python y Django** para explorar la colección de la Biblioteca Pública de Montenegro (Quindío) por categoría de lectura, con datos abiertos reales.

> Proyecto del hackathon *Innovación con Datos Abiertos de Colombia* — "Construye, aprende e innova".
> Ejercicio de desarrollo ágil **inspirado en Scrum**, en un solo sprint comprimido. No es una aplicación completa del marco.

**Estado:** sprint terminado. La Definición de Terminado se verificó (secciones 6 y 7).

---

## 1. Descubrimiento

| Elemento | Detalle |
|---|---|
| **Problema (hipótesis de necesidad)** | Familias, docentes y mediadores de lectura podrían tener dificultad para saber qué lecturas hay en la biblioteca según el tipo de público y el género. **No está contrastado con usuarios reales**; los datos solo prueban que existen registros. |
| **Usuario o beneficiario** | Madres, padres, docentes y mediadores de lectura de Montenegro. Interesada secundaria: la persona bibliotecaria. |
| **Funcionalidad principal** | Elegir una categoría de lectura y ver los libros con título, autor y ejemplares. |
| **Valor esperado** | Encontrar ideas de lectura sin revisar más de 4.000 filas desordenadas. |

### Fuente de los datos

| Campo | Detalle |
|---|---|
| Conjunto de datos | Activos de Información Biblioteca Pública Montenegro Quindío 2022 |
| ID en datos.gov.co | `hecw-3dai` |
| URL | https://www.datos.gov.co/Cultura/Activos-de-Informaci-n-Biblioteca-P-blica-Monteneg/hecw-3dai/about_data |
| Entidad publicadora | Alcaldía de Montenegro, Quindío (orden territorial, DIVIPOLA 63470) |
| Archivo usado | `data/biblioteca_montenegro.csv` (4.162 registros, descargado el 13-11-2026) |
| Modalidad de acceso | Archivo descargado (CSV). No se usó una muestra |

Campos usados: `NOMBRE DEL LIBRO`, `AUTOR`, `GENERO`, `NUMERO` (ejemplares).

### Limitaciones de los datos

- Es un inventario único del **20 de noviembre de 2022**. No indica si un libro está disponible hoy.
- `GENERO` tiene 68 valores con errores y variantes (por ejemplo `CUENTO` y `CUENTOS`). El equipo los normaliza y los agrupa. **Las categorías son una decisión del equipo, no un dato oficial.**
- No hay edad recomendada. "Infantil" se toma solo de los registros cuyo género lo dice explícitamente (271).
- Los registros `ALBUM` (502) no indican si son infantiles, por lo que **no se clasifican como infantiles**.
- Hay registros sin autor o sin género (`-`) y títulos repetidos, que pueden ser otras copias o ediciones.
- Algunos valores de `GENERO` no son géneros sino nombres de editoriales o personas (por ejemplo `MERCK SHARP`). Quedan en "Sin clasificar".
- La vista de inicio descarta registros sin título. En el inventario actual no hay ninguno, así que los totales no cambian.

### Datos responsables
El conjunto describe el inventario de libros y **no contiene datos personales**. Se conserva la atribución a la fuente.

---

## 2. La aplicación

### Funcionalidad

- [x] Ver una lista de libros reales del inventario (issue #3)
- [x] Explorar libros por categoría de lectura (issue #6)
- [x] Filtrar solo libros marcados como infantiles (issue #7)

> Las casillas se marcan solo cuando el criterio se comprobó, no cuando el código existe.

### Recorrido principal
1. Abrir la página de inicio (`/`) y pulsar "Explorar por categoría de lectura".
2. Elegir una categoría en `/libros/`.
3. Opcionalmente, activar la casilla "Solo infantiles" para ver solo los registros cuyo género dice "infantil". Se puede combinar con una categoría.
4. Ver los libros con título, autor, categoría y ejemplares.

### Casos controlados
- **Categoría sin resultados:** mensaje claro.
- **"Solo infantiles" sin resultados** (por ejemplo, combinado con "Literatura"): mensaje que indica la categoría y sugiere desactivar el filtro.
- **Libro sin autor:** se muestra "Autor no registrado".
- **Archivo de datos ausente:** mensaje de error comprensible, sin pantalla rota.
- **"Sin clasificar":** no aparece por defecto; la página lo avisa y permite verlo.
- **Edad recomendada:** la página aclara que el inventario no la incluye.

### Categorías de lectura

La clasificación usa una tabla de correspondencia (`GENRE_CATEGORIES` en `library/services.py`) que asigna **una única categoría** a cada género normalizado.

| Categoría | Libros | Criterio de agrupación |
|---|---|---|
| Literatura | 1.835 | Novelas, cuentos, poesía, antologías, ensayos, mitos y leyendas para adultos, tradición oral, literatura universal y escritores montenegrinos. |
| Ciencias sociales e historia | 612 | Geografía, historia y ciencias sociales (incluye variantes mal escritas). |
| Ciencias y tecnología | 508 | Tecnología, ciencias aplicadas, ciencias naturales y matemáticas. |
| Álbumes | 502 | Género `ALBUM`. Aparte porque el dato no indica si es infantil. |
| Infantil | 271 | Géneros que dicen explícitamente "infantil". |
| Arte y cultura | 246 | Teatro, dramaturgia, arte, recreación, deporte y manualidades. |
| Braille | 40 | Colección en Braille. |
| Educación y consulta | 11 | Cartillas, magisterio, valores y material didáctico. |
| Idiomas | 1 | Material de aprendizaje de idiomas (inglés). |
| Sin clasificar | 136 | Género vacío (`-`, 129) o valores que no son géneros. |

Criterios: cada libro recibe exactamente una categoría; se usa el género ya normalizado (mayúsculas, tildes, espacios y errores de escritura); lo que no está en la tabla va a "Sin clasificar"; el campo `genre` se conserva junto a `category`.

---

## 3. Planificación (Scrum)

### Objetivo del Producto (Product Goal)
Ayudar a las familias, docentes y mediadores de lectura de Montenegro a explorar la colección de la Biblioteca Pública por tipo de lectura.

### Objetivo del Sprint (Sprint Goal)
Que una persona pueda elegir una categoría de lectura y, opcionalmente, "solo infantiles", y vea los libros de la Biblioteca de Montenegro con autor y ejemplares, con mensajes claros cuando no haya resultados o falten datos.

### Lista de Producto (Product Backlog)

| Issue | Tipo | Elemento | Prioridad | ¿Entró al sprint? |
|---|---|---|---|---|
| #3 | Historia de usuario | Ver una lista de libros reales en la página de inicio | High | Sí |
| #6 | Historia de usuario | Explorar libros por categoría de lectura | High | Sí |
| #7 | Historia de usuario | Filtrar solo libros marcados como infantiles | High | Sí |

### Lista del Sprint (Sprint Backlog)
**Objetivo:** el del apartado anterior.
**Elementos elegidos:** #3, #6 y #7.
**Plan:** las tareas técnicas que los hacen posibles.

| Issue | Tipo | Trabajo | Priority | Story Points | Responsable |
|---|---|---|---|---|---|
| #1 | Técnica | Preparar repositorio, proyecto base y tablero | High | 2 | Angie Espinosa |
| #2 | Técnica | Cargar el CSV y leerlo desde `services.py` | High | 3 | Angie Espinosa |
| #3 | Historia | Ver lista de libros reales en la página de inicio | High | 2 | Camilo Zarate |
| #4 | Técnica | Normalizar los géneros del inventario | High | 3 | Paola Acosta |
| #5 | Técnica | Agrupar los géneros en categorías de lectura | High | 3 | Paola Acosta |
| #6 | Historia | Explorar libros por categoría de lectura | High | 5 | Angie Espinosa |
| #7 | Historia | Filtrar solo libros marcados como infantiles | High | 3 | Paola Acosta |
| #8 | Técnica | Escribir pruebas automáticas y verificar el recorrido | Medium | 3 | Camilo Zarate |
| #9 | Técnica | Completar README y verificar la DoD | Medium | 2 | Camilo Zarate |

Los puntos de historia son una estimación relativa y opcional. El estado real de cada issue está en el tablero.

### Seguimiento
- **GitHub Project:** https://github.com/users/julara209/projects/5
- **Issues:** https://github.com/julara209/BookLoria/issues
- Los issues se etiquetan `user-story` o `technical`, y sus títulos empiezan con `[HU]` o `[T]`.

### Sobre Scrum en este ejercicio
Se aplicaron el Objetivo del Producto, la Lista de Producto, el Objetivo del Sprint, la Lista del Sprint, la Definición de Terminado, la Revisión y la Retrospectiva en **un solo sprint** comprimido. El Daily Scrum no se representó artificialmente: los bloqueos se comunicaron cuando aparecieron.

---

## 4. Instalación y ejecución

**Requisitos:** Python 3.15 y Django 6.1.3 (ver `requirements.txt`), y Git.

```bash
git clone https://github.com/julara209/BookLoria.git
cd BookLoria
python -m venv .venv
```

Activar el entorno virtual:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

Instalar y ejecutar:

```bash
pip install -r requirements.txt
python manage.py runserver
```

Abrir http://127.0.0.1:8000/

> Si PowerShell bloquea la activación, ejecutar antes `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.

### Pruebas

```bash
python manage.py test
```

**Último resultado registrado:** Ran 36 tests in 0.866s    OK

### Estructura del proyecto

```
BookLoria/
├── data/
│   └── biblioteca_montenegro.csv
├── library/
│   ├── services.py          # leer, normalizar, agrupar y filtrar los datos
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   ├── static/library/styles.css
│   └── templates/library/
│       ├── base.html
│       ├── index.html
│       ├── books.html
│       ├── _source.html
│       └── _books_table.html
├── manage.py
├── requirements.txt
└── README.md
```

---

## 5. Colaboración con Git y GitHub

Flujo seguido en cada funcionalidad:

**Issue → Rama → Commit → Pull Request → Revisión → Comprobación → Integración → Verificación de la DoD → Done**

- Ramas y commits en inglés (por ejemplo `feature/browse-by-category`).
- Cada Pull Request menciona su issue con `Refs #N`, sin cierre automático.
- Cada cambio lo revisa una persona distinta de quien lo escribió.

**Pull Requests revisados e integrados** (8 en total, 0 abiertos al cierre del sprint):

| PR | Título | Autoría | Estado |
|---|---|---|---|
| [#10](https://github.com/julara209/BookLoria/pull/10) | Add Django project structure and placeholder home page | @julara209 | Integrado |
| [#11](https://github.com/julara209/BookLoria/pull/11) | Add library CSV and loader function in services.py | @julara209 | Integrado |
| [#12](https://github.com/julara209/BookLoria/pull/12) | feat: normalize book genres | @ypaoolp | Integrado |
| [#14](https://github.com/julara209/BookLoria/pull/14) | Group normalized genres into reading categories | @ypaoolp | Integrado |
| [#15](https://github.com/julara209/BookLoria/pull/15) | Add home page listing real books from the inventory | @1028865362 | Integrado |
| [#16](https://github.com/julara209/BookLoria/pull/16) | Add category selector and filtered book list | @julara209 | Integrado |
| [#17](https://github.com/julara209/BookLoria/pull/17) | Fix inventory integration and book listing | @ypaoolp | Integrado |
| [#13](https://github.com/julara209/BookLoria/pull/13) | Añadimos la HU-001 (elegir categoría) | @1028865362 | Cerrado sin integrar |

---

## 6. Definición de Terminado (DoD)

- [x] Django inicia sin errores bloqueantes.
- [x] Desde el navegador se puede elegir una categoría y ver resultados.
- [x] La aplicación atiende el problema elegido de forma demostrable.
- [x] Se usan datos reales cuya fuente está identificada.
- [x] Se cumplen los criterios de aceptación de cada issue completado.
- [x] Categoría sin resultados y libro sin autor no provocan fallos bloqueantes.
- [x] Se ejecutó y registró una comprobación funcional real.
- [x] Los cambios están revisados e integrados en la rama principal.
- [x] El README contiene los pasos para instalar y ejecutar la aplicación.
- [x] GitHub Issues y Projects reflejan el estado verdadero del trabajo.

> Un merge o una columna *Done* no equivalen por sí solos a "Terminado". Las casillas se marcan solo cuando se comprobaron.

---

## 7. Verificación

| Comprobación | Quién | Fecha | Resultado |
|---|---|---|---|
| Prueba manual del recorrido principal (`/` → `/libros/` → elegir categoría) | Camilo Zarate | 17-11-2026 | Correcto: se ven título, autor, categoría y ejemplares |
| Prueba manual: categoría sin resultados | Camilo Zarate | 17-11-2026 | Correcto: mensaje claro, sin errores |
| Prueba manual: libro sin autor | Camilo Zarate | 17-11-2026 | Correcto: se muestra "Autor no registrado" |
| Prueba manual: «Solo infantiles», solo y combinado con una categoría | Camilo Zarate| 17-11-2026 | Correcto: aplica ambas condiciones y muestra mensaje si no hay resultados |
| Ejecución por otra persona desde cero, siguiendo este README | Camilo Zarate | 17-11-2026 | Correcto |

**Resultado real de `python manage.py test`:**
```
Ran 36 tests in 0.866s
OK
```

**Pendiente o bloqueado:**
- Sin pendientes que impidan cumplir la Definición de Terminado.

---

## 8. Revisión y retrospectiva

### Sprint Review
- **Recorrido realmente disponible:** inicio con los primeros 50 libros del inventario; página `/libros/` con selector de categoría y casilla «Solo infantiles», combinable con la categoría; mensajes claros cuando no hay resultados o falta el autor.
- **Qué cumplió la DoD y qué quedó pendiente:** se cumplieron todos los puntos de la sección 6. No quedaron pendientes.
- **Comentarios recibidos:** ninguno registrado al cierre de este README.

### Retrospectiva
- **Qué funcionó bien:** separar la lógica en `services.py` permitió probar la lectura, normalización y agrupación de datos sin depender de la interfaz. Las pruebas automáticas detectaron desajustes entre las categorías y los conteos esperados.
- **Qué obstáculo afectó más:** dos ramas modificaron los mismos archivos (`services.py` y `books.html`) y generaron conflictos al integrarlas. Además, un bloque duplicado en la tabla `GENRE_CATEGORIES` sobrescribía una categoría sin avisar.
- **Acción concreta de mejora para el próximo ciclo:** traer `main` a la rama (`git fetch` y `git merge origin/main`) antes de empezar a trabajar, y ejecutar `python manage.py test` antes de cada push.

---

## 9. Equipo

| Nombre | Rol / aportes |
|---|---|
| Angie Espinosa | Preparó el repositorio, el proyecto base y el tablero (#1). Cargó el CSV y lo leyó desde `services.py` (#2). Desarrolló la exploración por categoría (#6). |
| Camilo Zarate | Lista de libros en la página de inicio (#3). Pruebas automáticas y verificación del recorrido (#8). README y verificación de la DoD (#9). |
| Paola Acosta | Normalización de géneros (#4), agrupación en categorías (#5) y filtro «Solo infantiles» (#7). |

## 10. Atribución

Datos: *Activos de Información Biblioteca Pública Montenegro Quindío 2022*, Alcaldía de Montenegro, Quindío, publicados en el [Portal de Datos Abiertos de Colombia](https://www.datos.gov.co/).