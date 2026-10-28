"""Unit tests for CalculatorEngine model."""

import unittest
from python_app.models.calculator_engine import CalculatorEngine


class TestCalculatorEngine(unittest.TestCase):
    """Test suite for mathematical arithmetic and scientific engine."""

    def setUp(self) -> None:
        self.engine = CalculatorEngine()

    def test_basic_addition(self) -> None:
        self.engine.input_digit("5")
        self.engine.set_operator("+")
        self.engine.input_digit("7")
        expr, res = self.engine.calculate_result()
        self.assertEqual(res, "12")
        self.assertEqual(self.engine.current_value, "12")

    def test_floating_precision_addition(self) -> None:
        # 0.1 + 0.2 must equal 0.3 without 0.30000000000000004 artifact
        self.engine.input_digit("0")
        self.engine.input_decimal_separator()
        self.engine.input_digit("1")
        self.engine.set_operator("+")
        self.engine.input_digit("0")
        self.engine.input_decimal_separator()
        self.engine.input_digit("2")
        _, res = self.engine.calculate_result()
        self.assertEqual(res, "0.3")

    def test_division_by_zero(self) -> None:
        self.engine.input_digit("9")
        self.engine.set_operator("/")
        self.engine.input_digit("0")
        _, res = self.engine.calculate_result()
        self.assertEqual(res, "Indefinido")
        self.assertEqual(self.engine.current_value, "Indefinido")

    def test_multiplication_and_subtraction(self) -> None:
        self.engine.input_digit("8")
        self.engine.set_operator("*")
        self.engine.input_digit("6")
        _, res = self.engine.calculate_result()
        self.assertEqual(res, "48")

        self.engine.set_operator("-")
        self.engine.input_digit("1")
        self.engine.input_digit("3")
        _, res = self.engine.calculate_result()
        self.assertEqual(res, "35")

    def test_toggle_sign(self) -> None:
        self.engine.input_digit("4")
        self.engine.input_digit("2")
        self.engine.toggle_sign()
        self.assertEqual(self.engine.current_value, "-42")
        self.engine.toggle_sign()
        self.assertEqual(self.engine.current_value, "42")

    def test_percentage(self) -> None:
        self.engine.input_digit("5")
        self.engine.input_digit("0")
        self.engine.percentage()
        self.assertEqual(self.engine.current_value, "0.5")

    def test_backspace(self) -> None:
        self.engine.input_digit("1")
        self.engine.input_digit("2")
        self.engine.input_digit("3")
        self.assertEqual(self.engine.current_value, "123")
        self.engine.backspace()
        self.assertEqual(self.engine.current_value, "12")
        self.engine.backspace()
        self.assertEqual(self.engine.current_value, "1")
        self.engine.backspace()
        self.assertEqual(self.engine.current_value, "0")

    def test_scientific_square_root(self) -> None:
        self.engine.set_value("144")
        _, res = self.engine.apply_scientific_function("sqrt")
        self.assertEqual(res, "12")

    def test_scientific_negative_sqrt(self) -> None:
        self.engine.set_value("-9")
        _, res = self.engine.apply_scientific_function("sqrt")
        self.assertEqual(res, "Entrada Inválida")

    def test_scientific_factorial(self) -> None:
        self.engine.set_value("5")
        _, res = self.engine.apply_scientific_function("factorial")
        self.assertEqual(res, "120")

    def test_scientific_logarithms(self) -> None:
        self.engine.set_value("100")
        _, res = self.engine.apply_scientific_function("log10")
        self.assertEqual(res, "2")

    def test_trigonometry_radians_and_degrees(self) -> None:
        # Radians: sin(0) = 0
        self.engine.is_degree_mode = False
        self.engine.set_value("0")
        _, res = self.engine.apply_scientific_function("sin")
        self.assertEqual(res, "0")

        # Degrees: sin(90) = 1
        self.engine.is_degree_mode = True
        self.engine.set_value("90")
        _, res = self.engine.apply_scientific_function("sin")
        self.assertEqual(res, "1")


if __name__ == "__main__":
    unittest.main()
