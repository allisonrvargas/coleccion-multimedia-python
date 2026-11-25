# 📚 Administrador de Colección de Libros, Películas y Música

[![CI](https://github.com/allisonrvargas/coleccion-multimedia-python/actions/workflows/ci.yml/badge.svg)](https://github.com/allisonrvargas/coleccion-multimedia-python/actions/workflows/ci.yml)
[![Licencia: MIT](https://img.shields.io/badge/licencia-MIT-green.svg)](LICENSE)

Aplicación de consola en **Python** para gestionar colecciones personales de libros, películas y música: organizar, buscar, editar y eliminar elementos, con los datos guardados en un archivo JSON.

## Características

- Añadir elementos (libro, película o música) con título, creador, género y valoración opcional de 0 a 10
- Listar la colección completa o filtrada por tipo y género
- Buscar por título, creador, género o ID
- Editar y eliminar elementos
- Ver estadísticas de la colección
- Persistencia en `collection.json` (con acentos y caracteres especiales)
- Tablas en consola con la librería `tabulate`

## Requisitos

- Python 3.9 o superior
- La librería `tabulate` (ver `requirements.txt`)

## Instalación y uso

```bash
git clone https://github.com/allisonrvargas/coleccion-multimedia-python.git
cd coleccion-multimedia-python
pip install -r requirements.txt
python main.py
```

## Pruebas

```bash
python -m unittest discover -s tests -t . -v
```

Las pruebas cubren la validación de valoraciones, guardar y cargar el JSON (incluido un archivo corrupto o inexistente), la generación de IDs, la búsqueda por ID o título y el formato de la tabla.

## Estructura

```text
main.py                 bucle principal y menú
menu.py                 textos de los menús
collection_manager.py   lógica de la colección (CRUD, búsqueda, estadísticas)
file_handler.py         lectura y escritura del JSON
utils.py                utilidades (limpiar pantalla, validar valoración)
collection.json         datos de ejemplo
tests/                  pruebas unitarias
```

## Autora

Allison Rocío Vargas Mejía ([@allisonrvargas](https://github.com/allisonrvargas)) · Campuslands

## Licencia

MIT