"""Converter View for Length, Weight, Temperature, and Currency."""

from typing import Callable, Optional
import customtkinter as ctk  # type: ignore

from python_app.config import COLORS
from python_app.models.unit_converter import UnitConverter, UnitConversionError
from python_app.views.components import IOSButton


class ConverterView(ctk.CTkFrame):
    """Interactive unit converter with category switching and numeric pad."""

    def __init__(
        self,
        master: any,
        unit_converter: UnitConverter,
        on_history_record: Optional[Callable[[str, str, str], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master=master, fg_color="transparent", **kwargs)

        self.converter = unit_converter
        self.on_history_record = on_history_record
        self.current_category = "Comprimento"
        self.input_value_str = "1"

        self._build_ui()
        self._on_category_changed("Comprimento")

    def _build_ui(self) -> None:
        # Category Selector
        self.category_segmented = ctk.CTkSegmentedButton(
            self,
            values=["Comprimento", "Peso", "Temperatura", "Moeda"],
            command=self._on_category_changed,
            fg_color=COLORS.SURFACE_BG,
            selected_color=COLORS.BTN_FUNCTION_BG,
            selected_hover_color=COLORS.BTN_FUNCTION_HOVER,
            unselected_color=COLORS.SURFACE_BG,
            unselected_hover_color=COLORS.SURFACE_HOVER,
            text_color=COLORS.TEXT_PRIMARY,
            font=ctk.CTkFont(family="SF Pro Text", size=13, weight="bold"),
        )
        self.category_segmented.set("Comprimento")
        self.category_segmented.pack(fill="x", padx=12, pady=(4, 10))

        # Main Card for Values and Units
        card_frame = ctk.CTkFrame(self, fg_color=COLORS.CONTAINER_BG, corner_radius=16)
        card_frame.pack(fill="x", padx=12, pady=(0, 10))

        # From Section
        from_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        from_frame.pack(fill="x", padx=14, pady=(12, 6))

        self.from_label_val = ctk.CTkLabel(
            from_frame,
            text="1",
            font=ctk.CTkFont(family="SF Pro Display", size=28, weight="bold"),
            text_color=COLORS.TEXT_PRIMARY,
            anchor="w",
        )
        self.from_label_val.pack(side="left", expand=True, fill="x")

        self.from_unit_menu = ctk.CTkOptionMenu(
            from_frame,
            values=[""],
            command=self._recalculate,
            fg_color=COLORS.SURFACE_BG,
            button_color=COLORS.BTN_OPERATOR_BG,
            button_hover_color=COLORS.BTN_OPERATOR_HOVER,
            text_color=COLORS.TEXT_PRIMARY,
            font=ctk.CTkFont(family="SF Pro Text", size=13),
            width=160,
        )
        self.from_unit_menu.pack(side="right")

        # Swap Button Divider
        divider_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        divider_frame.pack(fill="x", padx=14, pady=2)

        self.btn_swap = ctk.CTkButton(
            divider_frame,
            text="⇅ Inverter",
            width=90,
            height=28,
            corner_radius=14,
            fg_color=COLORS.SURFACE_BG,
            hover_color=COLORS.SURFACE_HOVER,
            text_color=COLORS.TEXT_SECONDARY,
            font=ctk.CTkFont(family="SF Pro Text", size=12, weight="bold"),
            command=self._swap_units,
        )
        self.btn_swap.pack(side="right")

        # To Section
        to_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        to_frame.pack(fill="x", padx=14, pady=(6, 12))

        self.to_label_val = ctk.CTkLabel(
            to_frame,
            text="1",
            font=ctk.CTkFont(family="SF Pro Display", size=28, weight="bold"),
            text_color=COLORS.TEXT_ACCENT,
            anchor="w",
        )
        self.to_label_val.pack(side="left", expand=True, fill="x")

        self.to_unit_menu = ctk.CTkOptionMenu(
            to_frame,
            values=[""],
            command=self._recalculate,
            fg_color=COLORS.SURFACE_BG,
            button_color=COLORS.BTN_OPERATOR_BG,
            button_hover_color=COLORS.BTN_OPERATOR_HOVER,
            text_color=COLORS.TEXT_PRIMARY,
            font=ctk.CTkFont(family="SF Pro Text", size=13),
            width=160,
        )
        self.to_unit_menu.pack(side="right")

        # Keypad for fast numeric input
        keypad_frame = ctk.CTkFrame(self, fg_color="transparent")
        keypad_frame.pack(fill="both", expand=True, padx=12, pady=(0, 4))

        for c in range(4):
            keypad_frame.grid_columnconfigure(c, weight=1, uniform="conv_col")
        for r in range(4):
            keypad_frame.grid_rowconfigure(r, weight=1, uniform="conv_row")

        pad_x = 3
        pad_y = 3

        # Row 0: 7, 8, 9, Backspace
        IOSButton(keypad_frame, text="7", height=50, command=lambda: self._on_digit("7")).grid(row=0, column=0, padx=pad_x, pady=pad_y, sticky="nsew")
        IOSButton(keypad_frame, text="8", height=50, command=lambda: self._on_digit("8")).grid(row=0, column=1, padx=pad_x, pady=pad_y, sticky="nsew")
        IOSButton(keypad_frame, text="9", height=50, command=lambda: self._on_digit("9")).grid(row=0, column=2, padx=pad_x, pady=pad_y, sticky="nsew")
        IOSButton(keypad_frame, text="⌫", button_type="function", height=50, font_size=18, command=self._backspace).grid(row=0, column=3, padx=pad_x, pady=pad_y, sticky="nsew")

        # Row 1: 4, 5, 6, Clear
        IOSButton(keypad_frame, text="4", height=50, command=lambda: self._on_digit("4")).grid(row=1, column=0, padx=pad_x, pady=pad_y, sticky="nsew")
        IOSButton(keypad_frame, text="5", height=50, command=lambda: self._on_digit("5")).grid(row=1, column=1, padx=pad_x, pady=pad_y, sticky="nsew")
        IOSButton(keypad_frame, text="6", height=50, command=lambda: self._on_digit("6")).grid(row=1, column=2, padx=pad_x, pady=pad_y, sticky="nsew")
        IOSButton(keypad_frame, text="C", button_type="function", height=50, font_size=18, command=self._clear).grid(row=1, column=3, padx=pad_x, pady=pad_y, sticky="nsew")

        # Row 2: 1, 2, 3, +/-
        IOSButton(keypad_frame, text="1", height=50, command=lambda: self._on_digit("1")).grid(row=2, column=0, padx=pad_x, pady=pad_y, sticky="nsew")
        IOSButton(keypad_frame, text="2", height=50, command=lambda: self._on_digit("2")).grid(row=2, column=1, padx=pad_x, pady=pad_y, sticky="nsew")
        IOSButton(keypad_frame, text="3", height=50, command=lambda: self._on_digit("3")).grid(row=2, column=2, padx=pad_x, pady=pad_y, sticky="nsew")
        IOSButton(keypad_frame, text="+/-", button_type="function", height=50, font_size=18, command=self._toggle_sign).grid(row=2, column=3, padx=pad_x, pady=pad_y, sticky="nsew")

        # Row 3: 0, comma, Salvar no Histórico
        IOSButton(keypad_frame, text="0", height=50, command=lambda: self._on_digit("0")).grid(row=3, column=0, columnspan=2, padx=pad_x, pady=pad_y, sticky="nsew")
        IOSButton(keypad_frame, text=",", height=50, command=self._decimal_separator).grid(row=3, column=2, padx=pad_x, pady=pad_y, sticky="nsew")
        IOSButton(keypad_frame, text="Salvar", button_type="operator", height=50, font_size=14, command=self._save_to_history).grid(row=3, column=3, padx=pad_x, pady=pad_y, sticky="nsew")

    def _on_category_changed(self, category: str) -> None:
        self.current_category = category
        units = self.converter.get_units_for_category(category)
        self.from_unit_menu.configure(values=units)
        self.to_unit_menu.configure(values=units)
        if len(units) >= 2:
            self.from_unit_menu.set(units[0])
            self.to_unit_menu.set(units[1])
        elif units:
            self.from_unit_menu.set(units[0])
            self.to_unit_menu.set(units[0])
        self._recalculate()

    def _swap_units(self) -> None:
        src = self.from_unit_menu.get()
        tgt = self.to_unit_menu.get()
        self.from_unit_menu.set(tgt)
        self.to_unit_menu.set(src)
        self._recalculate()

    def _on_digit(self, digit: str) -> None:
        if self.input_value_str == "0":
            self.input_value_str = digit
        elif len(self.input_value_str) < 14:
            self.input_value_str += digit
        self.from_label_val.configure(text=self.input_value_str)
        self._recalculate()

    def _decimal_separator(self) -> None:
        if "." not in self.input_value_str:
            self.input_value_str += "."
            self.from_label_val.configure(text=self.input_value_str)

    def _toggle_sign(self) -> None:
        if self.input_value_str.startswith("-"):
            self.input_value_str = self.input_value_str[1:]
        elif self.input_value_str != "0":
            self.input_value_str = "-" + self.input_value_str
        self.from_label_val.configure(text=self.input_value_str)
        self._recalculate()

    def _backspace(self) -> None:
        if len(self.input_value_str) > 1:
            self.input_value_str = self.input_value_str[:-1]
            if self.input_value_str == "-":
                self.input_value_str = "0"
        else:
            self.input_value_str = "0"
        self.from_label_val.configure(text=self.input_value_str)
        self._recalculate()

    def _clear(self) -> None:
        self.input_value_str = "0"
        self.from_label_val.configure(text="0")
        self._recalculate()

    def _recalculate(self, _=None) -> None:
        try:
            val = float(self.input_value_str or "0")
            from_u = self.from_unit_menu.get()
            to_u = self.to_unit_menu.get()
            res = self.converter.convert(self.current_category, val, from_u, to_u)
            if abs(res) < 1e-6 and res != 0:
                res_str = f"{res:.6e}"
            elif res.is_integer() and abs(res) < 1e12:
                res_str = str(int(res))
            else:
                res_str = f"{res:.6f}".rstrip("0").rstrip(".")
            self.to_label_val.configure(text=res_str)
        except UnitConversionError as e:
            self.to_label_val.configure(text="Inválido")
        except Exception:
            self.to_label_val.configure(text="Erro")

    def _save_to_history(self) -> None:
        if self.on_history_record:
            from_u = self.from_unit_menu.get()
            to_u = self.to_unit_menu.get()
            from_val = self.from_label_val.cget("text")
            to_val = self.to_label_val.cget("text")
            expr = f"{from_val} {from_u} ➔"
            self.on_history_record(expr, f"{to_val} {to_u}", f"Conversor ({self.current_category})")
