# Sistema de Gestión de Biblioteca Municipal

Este proyecto consiste en una aplicación de escritorio diseñada para la administración de inventarios de libros, desarrollada como parte del módulo de Diseño de Interfaces (DI). La aplicación permite realizar operaciones de lectura, escritura, actualización y borrado de datos sobre una base de datos local.

## Características Principales

* **Interfaz Gráfica de Usuario (GUI):** Implementada con el toolkit GTK 3 para ofrecer una experiencia de usuario nativa.
* **Gestión de Datos (CRUD):** Funcionalidad completa para añadir, visualizar, editar y eliminar registros de libros.
* **Persistencia de Datos:** Uso de SQLite para el almacenamiento de la información en un archivo local.
* **Documentación Técnica:** Generación de documentación automatizada mediante Sphinx, integrando los comentarios del código fuente (Docstrings).

## Tecnologías Utilizadas

* **Lenguaje:** Python 3.12
* **Interfaz Gráfica:** PyGObject (GTK 3)
* **Base de Datos:** SQLite 3
* **Documentación:** Sphinx (Extensiones: autodoc, napoleon, viewcode)
* **Entorno de Desarrollo:** MSYS2 / MinGW64

## Estructura del Directorio

* `src/`: Carpeta que contiene el código fuente del programa.
    * `main.py`: Punto de entrada de la aplicación y gestión de la interfaz.
    * `conexionBD.py`: Clase de abstracción para la base de datos.
* `docs/`: Carpeta de configuración y salida de la documentación.
    * `source/`: Archivos de configuración y archivos .rst de Sphinx.
    * `build/`: Resultado de la compilación de la documentación en formato HTML.

## Requisitos e Instalación

Para ejecutar el proyecto en un entorno Windows bajo MinGW64, es necesario instalar las siguientes dependencias:

1. Instalación de librerías de Python y GTK:
   `pacman -S mingw-w64-x86_64-python-gobject mingw-w64-x86_64-gtk3`

2. Ejecución de la aplicación:
   `python src/main.py`

## Generación de Documentación

El proyecto utiliza Sphinx para generar documentación técnica a partir del código. Se han implementado técnicas de "mocking" para permitir la compilación en entornos donde las librerías gráficas no están presentes durante el proceso de build.

Para compilar la documentación:
1. Navegar al directorio `docs/`.
2. Ejecutar el comando: `make html`
3. Consultar el archivo resultante en: `docs/build/html/index.html`

## Autor
* **Greg (CabbaGG)**
* Estudiante de 2º de Desarrollo de Aplicaciones Multiplataforma (DAM).