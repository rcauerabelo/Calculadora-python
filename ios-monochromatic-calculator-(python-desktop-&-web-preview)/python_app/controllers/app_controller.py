"""Application Controller (MVC).

Mediates interaction between UI views, mathematical engine, unit converter,
and history persistence. Handles keyboard event mapping and state synchronization.
"""

from typing import Optional
from python_app.models.calculator_engine import CalculatorEngine
from python_app.models.exchange_service import ExchangeRateService
from python_app.models.history_store import HistoryStore
from python_app.models.unit_converter import UnitConverter


class AppController:
    """Controller coordinating CalculatorEngine, UnitConverter, and HistoryStore."""

    def __init__(
        self,
        engine: Optional[CalculatorEngine] = None,
        history_store: Optional[HistoryStore] = None,
        exchange_service: Optional[ExchangeRateService] = None,
        unit_converter: Optional[UnitConverter] = None,
    ) -> None:
        self.engine = engine or CalculatorEngine()
        self.history_store = history_store or HistoryStore()
        self.exchange_service = exchange_service or ExchangeRateService()
        self.unit_converter = unit_converter or UnitConverter(self.exchange_service)

        self.window: Optional[any] = None
        self.active_mode: str = "Simples"

    def attach_window(self, window: any) -> None:
        """Attach the main UI window to this controller."""
        self.window = window
        self._update_display()

    # --- DIGIT & OPERATOR HANDLERS ---

    def handle_digit(self, digit: str) -> None:
        """Handle numeric input (0-9)."""
        self.engine.input_digit(digit)
        self._update_display()

    def handle_operator(self, operator: str) -> None:
        """Handle binary mathematical operators (+, -, *, /)."""
        self.engine.set_operator(operator)
        self._update_display()

    def handle_action(self, action: str) -> None:
        """Handle special actions like AC, +/-, %, =, decimal point, backspace."""
        if action == "AC":
            self.engine.reset()
        elif action == "+/-":
            self.engine.toggle_sign()
        elif action == "%":
            self.engine.percentage()
        elif action in (".", ","):
            self.engine.input_decimal_separator()
        elif action == "backspace":
            self.engine.backspace()
        elif action == "=":
            expr, res = self.engine.calculate_result()
            if expr and res not in ("Indefinido", "Erro de Sintaxe", "Entrada Inválida", "Estouro de Memória"):
                self.history_store.add(expr, res, mode=self.active_mode)
                if self.window and self.window.is_history_open:
                    self.window.history_drawer.refresh()
        elif action.startswith("ANGLE_"):
            mode = action.split("_")[1]
            self.engine.is_degree_mode = (mode == "Deg")
        elif action == "Ans":
            if self.engine.last_result:
                self.engine.set_value(self.engine.last_result)
        self._update_display()

    def handle_scientific(self, func_name: str) -> None:
        """Execute unary scientific math function (sin, cos, sqrt, log, etc.)."""
        expr, res = self.engine.apply_scientific_function(func_name)
        if expr and res not in ("Indefinido", "Erro de Sintaxe", "Entrada Inválida", "Estouro de Memória"):
            self.history_store.add(expr, res, mode="Científica")
            if self.window and self.window.is_history_open:
                self.window.history_drawer.refresh()
        self._update_display()

    # --- HISTORY REUSE (CRUD: USE) ---

    def handle_use_history(self, value: str) -> None:
        """Re-inject selected history result into active calculator."""
        clean_val = value.replace(" ", "").split("=")[-1]
        self.engine.set_value(clean_val)
        self._update_display()

    def record_conversion_history(self, expr: str, res: str, mode: str) -> None:
        """Record conversion events into history store."""
        self.history_store.add(expr, res, mode=mode)
        if self.window and self.window.is_history_open:
            self.window.history_drawer.refresh()

    # --- MODE SWITCHING ---

    def switch_mode(self, mode: str) -> None:
        """Switch active operational mode."""
        self.active_mode = mode
        if self.window:
            self.window.set_mode(mode)

    # --- KEYBOARD SHORTCUTS MAPPING ---

    def handle_key_event(self, event) -> None:
        """Map raw keyboard keys to corresponding calculator actions."""
        char = event.char
        keysym = event.keysym

        if char.isdigit():
            self.handle_digit(char)
        elif char in ("+", "-"):
            self.handle_operator(char)
        elif char == "*":
            self.handle_operator("×")
        elif char == "/":
            self.handle_operator("÷")
        elif char in (".", ","):
            self.handle_action(".")
        elif keysym in ("Return", "KP_Enter", "equal"):
            self.handle_action("=")
        elif keysym in ("BackSpace",):
            self.handle_action("backspace")
        elif keysym in ("Escape",):
            self.handle_action("AC")
        elif char == "%":
            self.handle_action("%")

    # --- INTERNAL HELPERS ---

    def _update_display(self) -> None:
        """Synchronize the DisplayWidget with engine's state."""
        if self.window and hasattr(self.window, "display"):
            self.window.display.update_display(
                expression=self.engine.expression_preview,
                result=self.engine.current_value,
            )
