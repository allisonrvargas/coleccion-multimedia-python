"""
Módulo de manejo de archivos
Gestiona la carga y guardado de datos en JSON
"""

import json
import os


class FileHandler:
    """Clase para manejar operaciones con archivos JSON"""
    
    def __init__(self, filename):
        self.filename = filename
    
    def load_collection(self):
        """Carga la colección desde el archivo JSON"""
        if not os.path.exists(self.filename):
            print(f"ℹ  Archivo '{self.filename}' no encontrado. Se creará uno nuevo.")
            return []
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                print(f" Colección cargada correctamente ({len(data)} elementos)")
                return data
        except json.JSONDecodeError:
            print(f"  Error al leer '{self.filename}'. Se iniciará con colección vacía.")
            return []
        except Exception as e:
            print(f" Error inesperado al cargar: {e}")
            return []
    
    def save_collection(self, collection):
        """Guarda la colección en el archivo JSON"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(collection, file, ensure_ascii=False, indent=4)
            print(f" Colección guardada correctamente en '{self.filename}'")
        except Exception as e:
            print(f" Error al guardar la colección: {e}")