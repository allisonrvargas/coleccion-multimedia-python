"""
Módulo de utilidades
Funciones auxiliares para la aplicación
"""

import os
import platform


def clear_screen():
    """Limpia la pantalla de la consola"""
    sistema = platform.system()
    if sistema == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def pause():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input("\n⏸  Presione Enter para continuar...")


def validate_rating(rating_str):
    """
    Valida que la valoración sea un número entre 0 y 10
    
    Args:
        rating_str: String con la valoración
        
    Returns:
        float o None si es inválida
    """
    try:
        rating = float(rating_str)
        if 0 <= rating <= 10:
            return rating
        return None
    except ValueError:
        return None