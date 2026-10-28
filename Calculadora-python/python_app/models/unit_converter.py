"""Unit Converter Model.

Supports Length, Weight, Temperature, and Currency conversions with high
precision, input validation, and bidirectional calculations.
"""

from decimal import Decimal, InvalidOperation
from typing import Dict, List, Optional
from python_app.models.exchange_service import ExchangeRateService


class UnitConversionError(Exception):
    """Exception raised for errors during unit conversions."""


class UnitConverter:
    """Core domain model for converting measurements across diverse categories."""

    # Length units mapped to base unit: Metros (m)
    LENGTH_UNITS: Dict[str, float] = {
        "Metros (m)": 1.0,
        "Quilômetros (km)": 1000.0,
        "Centímetros (cm)": 0.01,
        "Milímetros (mm)": 0.001,
        "Milhas (mi)": 1609.344,
        "Jardas (yd)": 0.9144,
        "Pés (ft)": 0.3048,
        "Polegadas (in)": 0.0254,
    }

    # Weight units mapped to base unit: Gramas (g)
    WEIGHT_UNITS: Dict[str, float] = {
        "Quilogramas (kg)": 1000.0,
        "Gramas (g)": 1.0,
        "Miligramas (mg)": 0.001,
        "Libras (lb)": 453.59237,
        "Onças (oz)": 28.349523,
        "Toneladas (t)": 1000000.0,
    }

    # Temperature unit labels
    TEMPERATURE_UNITS: List[str] = [
        "Graus Celsius (°C)",
        "Graus Fahrenheit (°F)",
        "Kelvin (K)",
    ]

    # Currency codes with user-friendly descriptions
    CURRENCY_UNITS: Dict[str, str] = {
        "USD": "Dólar Americano (USD)",
        "BRL": "Real Brasileiro (BRL)",
        "EUR": "Euro (EUR)",
        "GBP": "Libra Esterlina (GBP)",
        "JPY": "Iene Japonês (JPY)",
        "CAD": "Dólar Canadense (CAD)",
        "CHF": "Franco Suíço (CHF)",
        "AUD": "Dólar Australiano (AUD)",
        "BTC": "Bitcoin (BTC)",
    }

    CATEGORIES = ["Comprimento", "Peso", "Temperatura", "Moeda"]

    def __init__(self, exchange_service: Optional[ExchangeRateService] = None) -> None:
        self.exchange_service = exchange_service or ExchangeRateService()

    def get_units_for_category(self, category: str) -> List[str]:
        """Return the available units for a given category."""
        if category == "Comprimento":
            return list(self.LENGTH_UNITS.keys())
        if category == "Peso":
            return list(self.WEIGHT_UNITS.keys())
        if category == "Temperatura":
            return list(self.TEMPERATURE_UNITS)
        if category == "Moeda":
            return list(self.CURRENCY_UNITS.values())
        raise ValueError(f"Categoria desconhecida: {category}")

    def convert(self, category: str, value: float, from_unit: str, to_unit: str) -> float:
        """Perform conversion between units in a selected category.

        Raises:
            UnitConversionError: On invalid units or mathematically impossible values (e.g. Kelvin < 0).
        """
        if from_unit == to_unit:
            return value

        if category == "Comprimento":
            return self._convert_linear(value, from_unit, to_unit, self.LENGTH_UNITS)

        if category == "Peso":
            if value < 0:
                raise UnitConversionError("Massa não pode ser negativa.")
            return self._convert_linear(value, from_unit, to_unit, self.WEIGHT_UNITS)

        if category == "Temperatura":
            return self._convert_temperature(value, from_unit, to_unit)

        if category == "Moeda":
            return self._convert_currency(value, from_unit, to_unit)

        raise UnitConversionError(f"Categoria inválida: {category}")

    def _convert_linear(
        self, value: float, from_unit: str, to_unit: str, table: Dict[str, float]
    ) -> float:
        if from_unit not in table or to_unit not in table:
            raise UnitConversionError(f"Unidade inválida: {from_unit} ou {to_unit}")
        # Convert to base unit then to target unit
        base_val = value * table[from_unit]
        return base_val / table[to_unit]

    def _convert_temperature(self, value: float, from_unit: str, to_unit: str) -> float:
        # Convert to Celsius first
        if "Celsius" in from_unit:
            celsius = value
        elif "Fahrenheit" in from_unit:
            celsius = (value - 32.0) * (5.0 / 9.0)
        elif "Kelvin" in from_unit:
            if value < 0:
                raise UnitConversionError("Temperatura em Kelvin não pode ser menor que zero absoluto (0 K).")
            celsius = value - 273.15
        else:
            raise UnitConversionError(f"Unidade de temperatura desconhecida: {from_unit}")

        if celsius < -273.15:
            raise UnitConversionError("Temperatura abaixo do zero absoluto (-273,15 °C).")

        # Convert from Celsius to target
        if "Celsius" in to_unit:
            return celsius
        if "Fahrenheit" in to_unit:
            return (celsius * 9.0 / 5.0) + 32.0
        if "Kelvin" in to_unit:
            return celsius + 273.15

        raise UnitConversionError(f"Unidade de temperatura destino desconhecida: {to_unit}")

    def _convert_currency(self, value: float, from_label: str, to_label: str) -> float:
        # Extract currency codes
        inv_map = {v: k for k, v in self.CURRENCY_UNITS.items()}
        from_code = inv_map.get(from_label, from_label)
        to_code = inv_map.get(to_label, to_label)

        rate = self.exchange_service.get_rate(from_code, to_code)
        return value * rate
