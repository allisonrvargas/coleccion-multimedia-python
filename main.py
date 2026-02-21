"""Administrador de Colección de Libros/Películas/Música"""

from menu import Menu
from collection_manager import CollectionManager
from utils import clear_screen, pause


def main():
    """Función principal que ejecuta la aplicación"""
    manager = CollectionManager()
    menu = Menu()
    
    while True:
        clear_screen()
        menu.show_main_menu()
        
        option = input("\n Seleccione una opción: ").strip()
        
        if option == "1":
            manager.add_item()
        elif option == "2":
            manager.list_items()
        elif option == "3":
            manager.search_item()
        elif option == "4":
            manager.edit_item()
        elif option == "5":
            manager.delete_item()
        elif option == "6":
            manager.show_statistics()
        elif option == "7":
            print("\nGuardando cambios...")
            manager.save_collection()
            print(" ¡Gracias por usar el Administrador de Colección!")
            break
        else:
            print("\n Opción no válida. Intente nuevamente.")
        
        pause()


if __name__ == "__main__":
    main()