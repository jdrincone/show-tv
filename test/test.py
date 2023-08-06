import unittest
import datetime
from unittest.mock import patch

from src.core import list_dates, json_api


class TestListDates(unittest.TestCase):
    def test_list_dates_single_day(self):
        """ Verifica si la función funciona correctamente cuando el rango es de un solo día."""
        start_date = datetime.date(2022, 12, 1)
        end_date = datetime.date(2022, 12, 1)
        expected_dates = ['2022-12-01']
        self.assertEqual(list_dates(start_date, end_date), expected_dates)

    def test_list_dates_multiple_days(self):
        """Verifica si la función maneja correctamente un rango de múltiples días."""
        start_date = datetime.date(2022, 12, 1)
        end_date = datetime.date(2022, 12, 3)
        expected_dates = ['2022-12-01', '2022-12-02', '2022-12-03']
        self.assertEqual(list_dates(start_date, end_date), expected_dates)

    def test_list_dates_same_date(self):
        """Asegura que la función genere correctamente la lista de fechas cuando
         la fecha inicial y final son iguales."""
        start_date = datetime.date(2023, 1, 1)
        end_date = datetime.date(2023, 1, 1)
        expected_dates = ['2023-01-01']
        self.assertEqual(list_dates(start_date, end_date), expected_dates)

    def test_list_dates_invalid_range(self):
        """ Comprueba que la función devuelva una lista vacía cuando el rango es
        inválido (end_date anterior a start_date)"""
        start_date = datetime.date(2023, 2, 1)
        end_date = datetime.date(2023, 1, 1)
        expected_dates = []
        self.assertEqual(list_dates(start_date, end_date), expected_dates)


class TestJsonApi(unittest.TestCase):
    @patch('requests.get')
    def test_json_api_success(self, mock_get):
        """Verifica si la función json_api devuelve el JSON simulado cuando
        la respuesta de requests.get es exitosa (estado HTTP 200)."""

        # Configuramos el objeto mock para que devuelva una respuesta exitosa simulada
        json_response = {"key": "value"}
        mock_get.return_value.json.return_value = json_response

        # Realizamos la llamada a la función json_api con una URL simulada
        url = "http://example.com"
        result = json_api(url)

        # Verificamos que la función devuelva el JSON simulado
        self.assertEqual(result, json_response)

        # Verificamos que requests.get fue llamado con la URL correcta
        mock_get.assert_called_once_with(url, headers={"accept": "application/json"})


if __name__ == '__main__':
    unittest.main()
