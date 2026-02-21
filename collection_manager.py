"""
Módulo de gestión de colección
Contiene la lógica principal para administrar elementos
"""

from file_handler import FileHandler
from utils import clear_screen, pause, validate_rating
from tabulate import tabulate


class CollectionManager:
    """Clase para gestionar la colección de elementos"""
    
    def __init__(self, filename="collection.json"):
        self.filename = filename
        self.file_handler = FileHandler(filename)
        self.collection = self.file_handler.load_collection()
    
    def add_item(self):
        """Añade un nuevo elemento a la colección"""
        clear_screen()
        print("=" * 60)
        print(" AÑADIR NUEVO ELEMENTO A LA COLECCIÓN")
        print("=" * 60)
        
        print("\n¿Qué tipo de elemento desea añadir?")
        print("1. Libro")
        print("2. Película")
        print("3. Música")
        
        type_option = input("\n Seleccione el tipo (1-3): ").strip()
        
        types = {"1": "Libro", "2": "Película", "3": "Música"}
        
        if type_option not in types:
            print("\n Tipo no válido.")
            return
        
        item_type = types[type_option]
        
        print(f"\n--- Datos del {item_type} ---")
        titulo = input("Título: ").strip()
        
        if not titulo:
            print("\n El título no puede estar vacío.")
            return
        
        if item_type == "Libro":
            creator_label = "Autor"
        elif item_type == "Película":
            creator_label = "Director"
        else:
            creator_label = "Artista"
        
        creador = input(f"{creator_label}: ").strip()
        genero = input("Género: ").strip()
        
        while True:
            valoracion_str = input("Valoración (0-10, opcional - Enter para omitir): ").strip()
            if valoracion_str == "":
                valoracion = None
                break
            
            valoracion = validate_rating(valoracion_str)
            if valoracion is not None:
                break
            print(" Valoración inválida. Debe ser un número entre 0 y 10.")
        
        item_id = self._generate_id()
        
        item = {
            "id": item_id,
            "tipo": item_type,
            "titulo": titulo,
            "creador": creador,
            "genero": genero,
            "valoracion": valoracion
        }
        
        self.collection.append(item)
        self.save_collection()
        print(f"\n {item_type} '{titulo}' añadido con ID: {item_id}")

    def list_items(self):
        """Lista todos los elementos de la colección"""
        clear_screen()
        print("=" * 60)
        print(" LISTADO DE ELEMENTOS")
        print("=" * 60)
        
        if not self.collection:
            print("\n  La colección está vacía.")
            return
        
        print("\n¿Cómo desea ver la colección?")
        print("1. Todos los elementos\n2. Solo Libros\n3. Solo Películas\n4. Solo Música\n5. Por género")
        
        filter_option = input("\n Seleccione una opción (1-5): ").strip()
        filtered_items = self.collection.copy()
        
        if filter_option == "2":
            filtered_items = [item for item in self.collection if item["tipo"] == "Libro"]
        elif filter_option == "3":
            filtered_items = [item for item in self.collection if item["tipo"] == "Película"]
        elif filter_option == "4":
            filtered_items = [item for item in self.collection if item["tipo"] == "Música"]
        elif filter_option == "5":
            genero = input("\n Ingrese el género a buscar: ").strip().lower()
            filtered_items = [item for item in self.collection if genero in item["genero"].lower()]
        
        if not filtered_items:
            print("\n  No se encontraron elementos.")
            return
        
        self._display_items(filtered_items)

    def search_item(self):
        """Busca elementos en la colección por diversos criterios"""
        clear_screen()
        print("=" * 60)
        print(" BUSCAR ELEMENTO")
        print("=" * 60)
        
        if not self.collection:
            print("\n  La colección está vacía.")
            return
        
        print("\n1. Por título\n2. Por autor/director/artista\n3. Por género\n4. Por ID")
        search_option = input("\n Seleccione opción (1-4): ").strip()
        search_term = input("\n Ingrese término de búsqueda: ").strip().lower()
        
        results = []
        if search_option == "1":
            results = [i for i in self.collection if search_term in i["titulo"].lower()]
        elif search_option == "2":
            results = [i for i in self.collection if search_term in i["creador"].lower()]
        elif search_option == "3":
            results = [i for i in self.collection if search_term in i["genero"].lower()]
        elif search_option == "4":
            results = [i for i in self.collection if search_term == str(i["id"])]
        
        if not results:
            print(f"\n  No se encontró nada con '{search_term}'.")
        else:
            self._display_items(results)

    def edit_item(self):
        """Edita un elemento buscando por ID o Título"""
        clear_screen()
        print("=" * 60)
        print("EDITAR ELEMENTO")
        print("=" * 60)
        
        if not self.collection:
            print("\n  La colección está vacía.")
            return
        
        search_val = input("\n Ingrese el ID o Título del elemento a editar: ").strip()
        # USAMOS EL NUEVO MÉTODO AQUÍ
        item = self._find_item_by_id_or_title(search_val)
        
        if not item:
            print(f"\n No se encontró: {search_val}")
            return
        
        self._display_items([item])
        print("\n--- Nuevos datos (Enter para mantener actual) ---")
        
        new_titulo = input(f"Título [{item['titulo']}]: ").strip()
        new_creador = input(f"Creador [{item['creador']}]: ").strip()
        new_genero = input(f"Género [{item['genero']}]: ").strip()
        
        while True:
            curr = item['valoracion'] if item['valoracion'] is not None else "N/A"
            val_str = input(f"Valoración (0-10) [{curr}]: ").strip()
            if val_str == "":
                new_val = item['valoracion']
                break
            new_val = validate_rating(val_str)
            if new_val is not None: break
            print(" Error, número entre 0 y 10.")
        
        if new_titulo: item['titulo'] = new_titulo
        if new_creador: item['creador'] = new_creador
        if new_genero: item['genero'] = new_genero
        if val_str: item['valoracion'] = new_val
        
        self.save_collection()
        print("\n  Elemento actualizado.")

    def delete_item(self):
        """Elimina un elemento buscando por ID o Título"""
        clear_screen()
        print("=" * 60)
        print("ELIMINAR ELEMENTO")
        print("=" * 60)
        
        if not self.collection:
            print("\n  La colección está vacía.")
            return
        
        search_val = input("\n Ingrese el ID o Título a eliminar: ").strip()
        # USAMOS EL NUEVO MÉTODO AQUÍ TAMBIÉN
        item = self._find_item_by_id_or_title(search_val)
        
        if not item:
            print(f"\n No se encontró: {search_val}")
            return
        
        self._display_items([item])
        confirm = input("\n  ¿Eliminar permanentemente? (s/n): ").strip().lower()
        
        if confirm == 's':
            self.collection.remove(item)
            self.save_collection()
            print("\n  Elemento eliminado.")
        else:
            print("\n Operación cancelada.")

    def show_statistics(self):
        """Muestra estadísticas básicas"""
        clear_screen()
        if not self.collection: return
        total = len(self.collection)
        print(f"\n Total de elementos: {total}")
        # (Aquí puedes mantener tu lógica de estadísticas actual)

    def save_collection(self):
        self.file_handler.save_collection(self.collection)

    def _generate_id(self):
        if not self.collection: return 1
        return max(item["id"] for item in self.collection) + 1

    # NUEVO MÉTODO INCORPORADO
    def _find_item_by_id_or_title(self, search_value):
        """Busca un elemento por su ID o por su Título exacto"""
        for item in self.collection:
            if str(item["id"]) == str(search_value) or item["titulo"].lower() == search_value.lower():
                return item
        return None

    def _display_items(self, items):
        table_data = []
        for item in items:
            val = f"{item['valoracion']}/10" if item['valoracion'] is not None else "N/A"
            table_data.append([item['id'], item['tipo'], item['titulo'], item['creador'], item['genero'], val])
        
        headers = ["ID", "Tipo", "Título", "Creador", "Género", "Valoración"]
        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))