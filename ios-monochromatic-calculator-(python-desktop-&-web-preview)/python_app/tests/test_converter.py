"""Unit tests for UnitConverter model."""

import unittest
from python_app.models.exchange_service import ExchangeRateService
from python_app.models.unit_converter import UnitConversionError, UnitConverter


class TestUnitConverter(unittest.TestCase):
    """Test suite for unit conversion across all categories."""

    def setUp(self) -> None:
        self.service = ExchangeRateService(cache_file="data/test_exchange_cache.json")
        self.converter = UnitConverter(exchange_service=self.service)

    def test_length_conversion(self) -> None:
        # 1 km = 1000 m
        res = self.converter.convert("Comprimento", 1.0, "Quilômetros (km)", "Metros (m)")
        self.assertAlmostEqual(res, 1000.0, places=4)

        # 1 m to cm
        res2 = self.converter.convert("Comprimento", 2.5, "Metros (m)", "Centímetros (cm)")
        self.assertAlmostEqual(res2, 250.0, places=4)

    def test_weight_conversion(self) -> None:
        # 1 kg = 1000 g
        res = self.converter.convert("Peso", 1.0, "Quilogramas (kg)", "Gramas (g)")
        self.assertAlmostEqual(res, 1000.0, places=4)

    def test_negative_weight_rejected(self) -> None:
        with self.assertRaises(UnitConversionError):
            self.converter.convert("Peso", -5.0, "Quilogramas (kg)", "Gramas (g)")

    def test_temperature_conversion(self) -> None:
        # 0 °C = 32 °F
        res_f = self.converter.convert("Temperatura", 0.0, "Graus Celsius (°C)", "Graus Fahrenheit (°F)")
        self.assertAlmostEqual(res_f, 32.0, places=3)

        # 100 °C = 373.15 K
        res_k = self.converter.convert("Temperatura", 100.0, "Graus Celsius (°C)", "Kelvin (K)")
        self.assertAlmostEqual(res_k, 373.15, places=3)

        # Below absolute zero must raise error
        with self.assertRaises(UnitConversionError):
            self.converter.convert("Temperatura", -300.0, "Graus Celsius (°C)", "Kelvin (K)")

    def test_currency_conversion(self) -> None:
        # Using base offline rates: USD to BRL
        res = self.converter.convert(
            "Moeda", 100.0, "Dólar Americano (USD)", "Real Brasileiro (BRL)"
        )
        self.assertGreater(res, 0.0)


if __name__ == "__main__":
    unittest.main()
