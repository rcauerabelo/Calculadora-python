"""Calculator Engine Model.

Responsible for mathematical state management, token parsing, scientific
evaluations, precision formatting, and defensive error handling.
Does not depend on any UI framework.
"""

from decimal import Decimal, InvalidOperation, getcontext
import math
import re
from typing import Optional, Tuple

# Set high decimal precision for standard arithmetic operations
getcontext().prec = 28


class CalculatorError(Exception):
    """Base domain exception for calculator operations."""


class SyntaxExpressionError(CalculatorError):
    """Raised when an expression has mismatched parentheses or invalid syntax."""


class MathDomainError(CalculatorError):
    """Raised when an operation is outside mathematical domain (e.g. sqrt(-1), log(0))."""


class CalculatorEngine:
    """Core mathematical engine for arithmetic and scientific calculations."""

    def __init__(self) -> None:
        self.current_value: str = "0"
        self.expression_preview: str = ""
        self.last_operator: Optional[str] = None
        self.pending_operand: Optional[Decimal] = None
        self.is_new_entry: bool = True
        self.is_degree_mode: bool = False
        self.last_result: Optional[str] = None

    def reset(self) -> None:
        """Reset the calculator state to zero (AC - All Clear)."""
        self.current_value = "0"
        self.expression_preview = ""
        self.last_operator = None
        self.pending_operand = None
        self.is_new_entry = True

    def clear_entry(self) -> None:
        """Clear current entry (C) while preserving pending expression."""
        self.current_value = "0"
        self.is_new_entry = True

    def toggle_sign(self) -> None:
        """Invert the sign of the current value (+/-)."""
        if self.current_value in ("0", "Indefinido", "Erro de Sintaxe", "Entrada Inválida"):
            return
        if self.current_value.startswith("-"):
            self.current_value = self.current_value[1:]
        else:
            self.current_value = "-" + self.current_value

    def percentage(self) -> None:
        """Convert the current value to a percentage (divide by 100)."""
        try:
            val = Decimal(self.current_value)
            val = val / Decimal("100")
            self.current_value = self._format_decimal(val)
            self.is_new_entry = True
        except (InvalidOperation, OverflowError):
            self.current_value = "Entrada Inválida"

    def backspace(self) -> None:
        """Remove the last typed digit from current value."""
        if self.is_new_entry or self.current_value in ("0", "Indefinido", "Erro de Sintaxe", "Entrada Inválida"):
            self.current_value = "0"
            self.is_new_entry = True
            return

        if len(self.current_value) > 1:
            self.current_value = self.current_value[:-1]
            if self.current_value == "-":
                self.current_value = "0"
                self.is_new_entry = True
        else:
            self.current_value = "0"
            self.is_new_entry = True

    def input_digit(self, digit: str) -> None:
        """Append a numeric digit (0-9) to current value."""
        if not digit.isdigit():
            raise ValueError(f"Invalid digit: {digit}")

        if self.is_new_entry or self.current_value in ("0", "Indefinido", "Erro de Sintaxe", "Entrada Inválida"):
            self.current_value = digit
            self.is_new_entry = False
        else:
            # Prevent excessive visual overflow (max 18 digits)
            clean_len = len(self.current_value.replace(".", "").replace("-", ""))
            if clean_len < 18:
                self.current_value += digit

    def input_decimal_separator(self) -> None:
        """Append a decimal separator (.) to current value."""
        if self.is_new_entry or self.current_value in ("Indefinido", "Erro de Sintaxe", "Entrada Inválida"):
            self.current_value = "0."
            self.is_new_entry = False
        elif "." not in self.current_value:
            self.current_value += "."
            self.is_new_entry = False

    def set_operator(self, operator: str) -> None:
        """Queue a binary operator (+, -, *, /) and compute pending operations."""
        if operator not in ("+", "-", "*", "/", "×", "÷", "^"):
            raise ValueError(f"Unsupported operator: {operator}")

        norm_op = "*" if operator in ("*", "×") else ("/" if operator in ("/", "÷") else operator)

        if self.pending_operand is not None and not self.is_new_entry:
            self.calculate_result()

        try:
            self.pending_operand = Decimal(self.current_value)
            self.last_operator = norm_op
            symbol = "×" if norm_op == "*" else ("÷" if norm_op == "/" else norm_op)
            self.expression_preview = f"{self._format_for_display(self.current_value)} {symbol}"
            self.is_new_entry = True
        except (InvalidOperation, OverflowError):
            self.current_value = "Entrada Inválida"
            self.is_new_entry = True

    def calculate_result(self) -> Tuple[Optional[str], str]:
        """Compute the pending calculation and return (expression, result).

        Returns:
            Tuple[Optional[str], str]: The evaluated expression string and the formatted result.
        """
        if self.pending_operand is None or self.last_operator is None:
            return None, self.current_value

        try:
            current = Decimal(self.current_value)
            prev = self.pending_operand
            op = self.last_operator

            symbol = "×" if op == "*" else ("÷" if op == "/" else op)
            expr_str = f"{self._format_for_display(str(prev))} {symbol} {self._format_for_display(str(current))}"

            if op == "+":
                res = prev + current
            elif op == "-":
                res = prev - current
            elif op == "*":
                res = prev * current
            elif op == "/":
                if current == Decimal("0"):
                    self.current_value = "Indefinido"
                    self.pending_operand = None
                    self.last_operator = None
                    self.is_new_entry = True
                    return expr_str, "Indefinido"
                res = prev / current
            elif op == "^":
                res = Decimal(str(math.pow(float(prev), float(current))))
            else:
                raise ValueError(f"Unknown operator {op}")

            result_str = self._format_decimal(res)
            self.current_value = result_str
            self.expression_preview = f"{expr_str} ="
            self.pending_operand = None
            self.last_operator = None
            self.is_new_entry = True
            self.last_result = result_str
            return expr_str, result_str

        except ZeroDivisionError:
            self.current_value = "Indefinido"
            self._reset_transient()
            return None, "Indefinido"
        except (OverflowError, math.erange if hasattr(math, 'erange') else OverflowError):
            self.current_value = "Estouro de Memória"
            self._reset_transient()
            return None, "Estouro de Memória"
        except (InvalidOperation, ValueError):
            self.current_value = "Entrada Inválida"
            self._reset_transient()
            return None, "Entrada Inválida"

    def apply_scientific_function(self, func_name: str) -> Tuple[str, str]:
        """Execute a unary scientific function (sin, cos, sqrt, log, etc.)."""
        try:
            val = float(self.current_value)
            angle_val = math.radians(val) if self.is_degree_mode else val
            expr_desc = f"{func_name}({self.current_value})"

            if func_name == "sin":
                res = math.sin(angle_val)
            elif func_name == "cos":
                res = math.cos(angle_val)
            elif func_name == "tan":
                if math.isclose(math.cos(angle_val), 0.0, abs_tol=1e-12):
                    self.current_value = "Indefinido"
                    self.is_new_entry = True
                    return expr_desc, "Indefinido"
                res = math.tan(angle_val)
            elif func_name == "sqrt":
                if val < 0:
                    self.current_value = "Entrada Inválida"
                    self.is_new_entry = True
                    return expr_desc, "Entrada Inválida"
                res = math.sqrt(val)
            elif func_name == "cbrt":
                res = math.cbrt(val) if hasattr(math, "cbrt") else (val ** (1 / 3))
            elif func_name == "sqr":
                res = val ** 2
                expr_desc = f"({self.current_value})²"
            elif func_name == "cube":
                res = val ** 3
                expr_desc = f"({self.current_value})³"
            elif func_name == "inverse":
                if val == 0:
                    self.current_value = "Indefinido"
                    self.is_new_entry = True
                    return f"1/({self.current_value})", "Indefinido"
                res = 1 / val
                expr_desc = f"1/({self.current_value})"
            elif func_name == "log10":
                if val <= 0:
                    self.current_value = "Entrada Inválida"
                    self.is_new_entry = True
                    return expr_desc, "Entrada Inválida"
                res = math.log10(val)
            elif func_name == "ln":
                if val <= 0:
                    self.current_value = "Entrada Inválida"
                    self.is_new_entry = True
                    return expr_desc, "Entrada Inválida"
                res = math.log(val)
            elif func_name == "exp":
                res = math.exp(val)
            elif func_name == "factorial":
                if val < 0 or not val.is_integer() or val > 170:
                    self.current_value = "Entrada Inválida" if val < 0 or not val.is_integer() else "Estouro de Memória"
                    self.is_new_entry = True
                    return f"{self.current_value}!", self.current_value
                res = float(math.factorial(int(val)))
                expr_desc = f"{int(val)}!"
            elif func_name == "pi":
                res = math.pi
                expr_desc = "π"
            elif func_name == "e":
                res = math.e
                expr_desc = "e"
            else:
                raise ValueError(f"Unknown scientific function: {func_name}")

            # Round near-zero floating artifacts (e.g. sin(pi) -> 0)
            if abs(res) < 1e-15:
                res = 0.0

            result_str = self._format_float(res)
            self.current_value = result_str
            self.expression_preview = f"{expr_desc} ="
            self.is_new_entry = True
            self.last_result = result_str
            return expr_desc, result_str

        except (ValueError, MathDomainError):
            self.current_value = "Entrada Inválida"
            self.is_new_entry = True
            return f"{func_name}()", "Entrada Inválida"
        except OverflowError:
            self.current_value = "Estouro de Memória"
            self.is_new_entry = True
            return f"{func_name}()", "Estouro de Memória"

    def toggle_angle_mode(self) -> str:
        """Switch between Radian (Rad) and Degree (Deg) modes."""
        self.is_degree_mode = not self.is_degree_mode
        return "Deg" if self.is_degree_mode else "Rad"

    def set_value(self, value: str) -> None:
        """Load an explicit value (e.g. from history entry)."""
        self.current_value = value
        self.is_new_entry = True

    def _reset_transient(self) -> None:
        self.pending_operand = None
        self.last_operator = None
        self.is_new_entry = True

    def _format_decimal(self, d: Decimal) -> str:
        """Format a Decimal number cleanly, eliminating trailing zeros."""
        if d.is_nan():
            return "Indefinido"
        if d.is_infinite():
            return "Estouro de Memória"
        normalized = d.normalize()
        # Prevent scientific notation for reasonable numbers
        sign, digits, exponent = normalized.as_tuple()
        if exponent > -10 and exponent < 12:
            s = f"{normalized:f}"
        else:
            s = f"{normalized:e}"
        return s

    def _format_float(self, f: float) -> str:
        """Format a float cleanly with integer checks and rounding."""
        if math.isnan(f):
            return "Indefinido"
        if math.isinf(f):
            return "Estouro de Memória"
        if f.is_integer() and abs(f) < 1e14:
            return str(int(f))
        # Use precision-trimmed string
        formatted = f"{f:.10g}"
        return formatted

    def _format_for_display(self, num_str: str) -> str:
        """Format number string for clear readability in expressions."""
        if not num_str:
            return "0"
        return num_str
