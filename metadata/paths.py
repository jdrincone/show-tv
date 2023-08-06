import os


class Paths:
    path_file = os.path.dirname(os.path.abspath(__file__))
    json = os.path.join(path_file, "..", "json")
    data = os.path.join(path_file, "..", "data")
    profiling = os.path.join(path_file, "..", "profiling")
    path_input = os.path.join(path_file, "..", "input")
    cred = os.path.join(path_input, "cred.yaml")
    db_lulobank = os.path.join(path_file, "..", "db", "lulobank.bd")

    def root_json(self, name_file):
        """Genera las rutas donde se almacena los testigos para cada reporte.

        Args:
            name_file: reporte de dataclean.
        """
        return os.path.join(Paths.json, f'shows_{name_file}.json')

    def root_parquet(self, name_file):
        """Genera las rutas donde se almacena los testigos para cada reporte.

        Args:
            name_file: reporte de dataclean.
        """
        return os.path.join(Paths.data, f'{name_file}.parquet')

    def root_profiling(self, name_file):
        """Genera las rutas donde se almacena los testigos para cada reporte.

        Args:
            name_file: reporte de dataclean.
        """
        return os.path.join(Paths.profiling, f'{name_file}.html')
