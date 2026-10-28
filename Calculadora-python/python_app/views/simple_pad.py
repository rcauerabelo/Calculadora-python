"""Simple 4x5 button pad view for basic arithmetic."""

from typing import Callable
import customtkinter as ctk  # type: ignore

from python_app.views.components import IOSButton


class SimplePad(ctk.CTkFrame):
    """Grid layout for the standard iOS calculator keypad."""

    def __init__(
        self,
        master: any,
        on_digit: Callable[[str], None],
        on_operator: Callable[[str], None],
        on_action: Callable[[str], None],
        **kwargs,
    ) -> None:
        super().__init__(master=master, fg_color="transparent", **kwargs)

        self.on_digit = on_digit
        self.on_operator = on_operator
        self.on_action = on_action

        self._build_keypad()

    def _build_keypad(self) -> None:
        # Configure 4 columns and 5 rows
        for col in range(4):
            self.grid_columnconfigure(col, weight=1, uniform="col")
        for row in range(5):
            self.grid_rowconfigure(row, weight=1, uniform="row")

        pad_x = 4
        pad_y = 4

        # Row 0: AC, +/-, %, ÷
        btn_ac = IOSButton(self, text="AC", button_type="function", command=lambda: self.on_action("AC"))
        btn_ac.grid(row=0, column=0, padx=pad_x, pady=pad_y, sticky="nsew")

        btn_pm = IOSButton(self, text="+/-", button_type="function", command=lambda: self.on_action("+/-"))
        btn_pm.grid(row=0, column=1, padx=pad_x, pady=pad_y, sticky="nsew")

        btn_pct = IOSButton(self, text="%", button_type="function", command=lambda: self.on_action("%"))
        btn_pct.grid(row=0, column=2, padx=pad_x, pady=pad_y, sticky="nsew")

        btn_div = IOSButton(self, text="÷", button_type="operator", command=lambda: self.on_operator("÷"))
        btn_div.grid(row=0, column=3, padx=pad_x, pady=pad_y, sticky="nsew")

        # Row 1: 7, 8, 9, ×
        btn_7 = IOSButton(self, text="7", button_type="number", command=lambda: self.on_digit("7"))
        btn_7.grid(row=1, column=0, padx=pad_x, pady=pad_y, sticky="nsew")

        btn_8 = IOSButton(self, text="8", button_type="number", command=lambda: self.on_digit("8"))
        btn_8.grid(row=1, column=1, padx=pad_x, pady=pad_y, sticky="nsew")

        btn_9 = IOSButton(self, text="9", button_type="number", command=lambda: self.on_digit("9"))
        btn_9.grid(row=1, column=2, padx=pad_x, pady=pad_y, sticky="nsew")

        btn_mul = IOSButton(self, text="×", button_type="operator", command=lambda: self.on_operator("×"))
        btn_mul.grid(row=1, column=3, padx=pad_x, pady=pad_y, sticky="nsew")

        # Row 2: 4, 5, 6, -
        btn_4 = IOSButton(self, text="4", button_type="number", command=lambda: self.on_digit("4"))
        btn_4.grid(row=2, column=0, padx=pad_x, pady=pad_y, sticky="nsew")

        btn_5 = IOSButton(self, text="5", button_type="number", command=lambda: self.on_digit("5"))
        btn_5.grid(row=2, column=1, padx=pad_x, pady=pad_y, sticky="nsew")

        btn_6 = IOSButton(self, text="6", button_type="number", command=lambda: self.on_digit("6"))
        btn_6.grid(row=2, column=2, padx=pad_x, pady=pad_y, sticky="nsew")

        btn_sub = IOSButton(self, text="-", button_type="operator", command=lambda: self.on_operator("-"))
        btn_sub.grid(row=2, column=3, padx=pad_x, pady=pad_y, sticky="nsew")

        # Row 3: 1, 2, 3, +
        btn_1 = IOSButton(self, text="1", button_type="number", command=lambda: self.on_digit("1"))
        btn_1.grid(row=3, column=0, padx=pad_x, pady=pad_y, sticky="nsew")

        btn_2 = IOSButton(self, text="2", button_type="number", command=lambda: self.on_digit("2"))
        btn_2.grid(row=3, column=1, padx=pad_x, pady=pad_y, sticky="nsew")

        btn_3 = IOSButton(self, text="3", button_type="number", command=lambda: self.on_digit("3"))
        btn_3.grid(row=3, column=2, padx=pad_x, pady=pad_y, sticky="nsew")

        btn_add = IOSButton(self, text="+", button_type="operator", command=lambda: self.on_operator("+"))
        btn_add.grid(row=3, column=3, padx=pad_x, pady=pad_y, sticky="nsew")

        # Row 4: 0 (span 2), comma, =
        btn_0 = IOSButton(self, text="0", button_type="number", command=lambda: self.on_digit("0"))
        btn_0.grid(row=4, column=0, columnspan=2, padx=pad_x, pady=pad_y, sticky="nsew")

        btn_dot = IOSButton(self, text=",", button_type="number", command=lambda: self.on_action("."))
        btn_dot.grid(row=4, column=2, padx=pad_x, pady=pad_y, sticky="nsew")

        btn_eq = IOSButton(self, text="=", button_type="operator", command=lambda: self.on_action("="))
        btn_eq.grid(row=4, column=3, padx=pad_x, pady=pad_y, sticky="nsew")
