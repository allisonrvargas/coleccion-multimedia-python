"""
Módulo de menús
Contiene el diseño visual de los menús de la aplicación
"""


class Menu:
    """Clase para mostrar menús de la aplicación"""
    
    @staticmethod
    def show_main_menu():
        """Muestra el menú principal"""
        print("╔" + "═" * 58 + "╗")
        print("║" + " " * 58 + "║")
        print("║" + "   ADMINISTRADOR DE COLECCIÓN  ".center(58) + "║")
        print("║" + "  (Libros • Películas • Música)  ".center(58) + "║")
        print("║" + " " * 58 + "║")
        print("╠" + "═" * 58 + "╣")
        print("║" + " " * 58 + "║")
        print("║  1.  Añadir elemento a la colección" + " " * 17 + "║")
        print("║  2.  Listar elementos de la colección" + " " * 15 + "║")
        print("║  3.  Buscar elemento" + " " * 32 + "║")
        print("║  4.  Editar elemento" + " " * 32 + "║")
        print("║  5.  Eliminar elemento" + " " * 30 + "║")
        print("║  6.  Ver estadísticas" + " " * 30 + "║")
        print("║  7.  Guardar y salir" + " " * 32 + "║")
        print("║" + " " * 58 + "║")
        print("╚" + "═" * 58 + "╝")