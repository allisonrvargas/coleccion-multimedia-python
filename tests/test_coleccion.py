import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

from collection_manager import CollectionManager
from file_handler import FileHandler
from utils import validate_rating


def silencio():
    return redirect_stdout(StringIO())


class PruebasValoracion(unittest.TestCase):
    def test_acepta_valores_entre_0_y_10(self):
        self.assertEqual(validate_rating("0"), 0.0)
        self.assertEqual(validate_rating("7.5"), 7.5)
        self.assertEqual(validate_rating("10"), 10.0)

    def test_rechaza_fuera_de_rango_o_texto(self):
        for valor in ("-1", "10.1", "abc", ""):
            self.assertIsNone(validate_rating(valor))


class PruebasArchivo(unittest.TestCase):
    def setUp(self):
        self.carpeta = tempfile.TemporaryDirectory()
        self.ruta = os.path.join(self.carpeta.name, "coleccion.json")

    def tearDown(self):
        self.carpeta.cleanup()

    def test_archivo_inexistente_devuelve_lista_vacia(self):
        with silencio():
            self.assertEqual(FileHandler(self.ruta).load_collection(), [])

    def test_guardar_y_cargar_conserva_los_datos_con_acentos(self):
        datos = [{"id": 1, "tipo": "Película", "titulo": "Amélie", "creador": "Jeunet", "genero": "Comedia", "valoracion": 9.0}]
        manejador = FileHandler(self.ruta)
        with silencio():
            manejador.save_collection(datos)
            self.assertEqual(manejador.load_collection(), datos)

    def test_json_corrupto_no_rompe_el_programa(self):
        with open(self.ruta, "w", encoding="utf-8") as f:
            f.write("{esto no es json")
        with silencio():
            self.assertEqual(FileHandler(self.ruta).load_collection(), [])


class PruebasColeccion(unittest.TestCase):
    def setUp(self):
        self.carpeta = tempfile.TemporaryDirectory()
        ruta = os.path.join(self.carpeta.name, "coleccion.json")
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump([
                {"id": 1, "tipo": "Libro", "titulo": "Dune", "creador": "Herbert", "genero": "Ciencia ficción", "valoracion": 9.5},
                {"id": 5, "tipo": "Música", "titulo": "Abbey Road", "creador": "The Beatles", "genero": "Rock", "valoracion": None},
            ], f)
        with silencio():
            self.gestor = CollectionManager(ruta)

    def tearDown(self):
        self.carpeta.cleanup()

    def test_carga_los_elementos_existentes(self):
        self.assertEqual(len(self.gestor.collection), 2)

    def test_el_nuevo_id_sigue_al_mayor(self):
        self.assertEqual(self.gestor._generate_id(), 6)

    def test_el_primer_id_de_una_coleccion_vacia_es_1(self):
        self.gestor.collection = []
        self.assertEqual(self.gestor._generate_id(), 1)

    def test_busca_por_id_o_por_titulo_sin_distinguir_mayusculas(self):
        self.assertEqual(self.gestor._find_item_by_id_or_title("5")["titulo"], "Abbey Road")
        self.assertEqual(self.gestor._find_item_by_id_or_title("dune")["id"], 1)
        self.assertIsNone(self.gestor._find_item_by_id_or_title("no existe"))

    def test_la_tabla_muestra_na_cuando_no_hay_valoracion(self):
        salida = StringIO()
        with redirect_stdout(salida):
            self.gestor._display_items(self.gestor.collection)
        self.assertIn("9.5/10", salida.getvalue())
        self.assertIn("N/A", salida.getvalue())


if __name__ == "__main__":
    unittest.main()