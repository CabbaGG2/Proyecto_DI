import os
import sys

# 1. Ruta al código
sys.path.insert(0, os.path.abspath('../../src'))

# 2. Configuración del proyecto
project = 'Gestión de Biblioteca'
copyright = '2026, CabbaGG'
author = 'CabbaGG'
release = '1.0'

# 3. Extensiones
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode'
]

# 4. Mocks nativos de Sphinx (esto es lo más estable)
autodoc_mock_imports = ["gi", "gi.repository"]

language = 'es'
html_theme = 'alabaster'