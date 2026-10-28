"""Scientific keypad layout extending standard operations with math functions."""

from typing import Callable
import customtkinter as ctk  # type: ignore

from python_app.views.components import IOSButton


class ScientificPad(ctk.CTkFrame):
    """Grid layout combining scientific functions (left) and arithmetic/numeric keys (right)."""

    def __init__(
        self,
        master: any,
        on_digit: Callable[[str], None],
        on_operator: Callable[[str], None],
        on_action: Callable[[str], None],
        on_scientific: Callable[[str], None],
        **kwargs,
    ) -> None:
        super().__init__(master=master, fg_color="transparent", **kwargs)

        self.on_digit = on_digit
        self.on_operator = on_operator
        self.on_action = on_action
        self.on_scientific = on_scientific
        self.angle_mode = "Rad"

        self._build_keypad()

    def _build_keypad(self) -> None:
        # 8 columns: 4 for scientific functions, 4 for numeric/operator functions
        for col in range(8):
            self.grid_columnconfigure(col, weight=1, uniform="col")
        for row in range(5):
            self.grid_rowconfigure(row, weight=1, uniform="row")

        pad_x = 3
        pad_y = 3

        # Row 0: Scientific + Basic Functions
        self.btn_angle = IOSButton(
            self, text="Rad", button_type="scientific", font_size=15,
            command=self._toggle_angle
        )
        self.btn_angle.grid(row=0, column=0, padx=pad_x, pady=pad_y, sticky="nsew")

        b_sin = IOSButton(self, text="sin", button_type="scientific", font_size=16, command=lambda: self.on_scientific("sin"))
        b_sin.grid(row=0, column=1, padx=pad_x, pady=pad_y, sticky="nsew")

        b_cos = IOSButton(self, text="cos", button_type="scientific", font_size=16, command=lambda: self.on_scientific("cos"))
        b_cos.grid(row=0, column=2, padx=pad_x, pady=pad_y, sticky="nsew")

        b_tan = IOSButton(self, text="tan", button_type="scientific", font_size=16, command=lambda: self.on_scientific("tan"))
        b_tan.grid(row=0, column=3, padx=pad_x, pady=pad_y, sticky="nsew")

        b_ac = IOSButton(self, text="AC", button_type="function", font_size=18, command=lambda: self.on_action("AC"))
        b_ac.grid(row=0, column=4, padx=pad_x, pady=pad_y, sticky="nsew")

        b_pm = IOSButton(self, text="+/-", button_type="function", font_size=18, command=lambda: self.on_action("+/-"))
        b_pm.grid(row=0, column=5, padx=pad_x, pady=pad_y, sticky="nsew")

        b_pct = IOSButton(self, text="%", button_type="function", font_size=18, command=lambda: self.on_action("%"))
        b_pct.grid(row=0, column=6, padx=pad_x, pady=pad_y, sticky="nsew")

        b_div = IOSButton(self, text="÷", button_type="operator", font_size=20, command=lambda: self.on_operator("÷"))
        b_div.grid(row=0, column=7, padx=pad_x, pady=pad_y, sticky="nsew")

        # Row 1: Exponentials + Numbers 7, 8, 9, ×
        b_sqr = IOSButton(self, text="x²", button_type="scientific", font_size=16, command=lambda: self.on_scientific("sqr"))
        b_sqr.grid(row=1, column=0, padx=pad_x, pady=pad_y, sticky="nsew")

        b_cube = IOSButton(self, text="x³", button_type="scientific", font_size=16, command=lambda: self.on_scientific("cube"))
        b_cube.grid(row=1, column=1, padx=pad_x, pady=pad_y, sticky="nsew")

        b_pow = IOSButton(self, text="xʸ", button_type="scientific", font_size=16, command=lambda: self.on_operator("^"))
        b_pow.grid(row=1, column=2, padx=pad_x, pady=pad_y, sticky="nsew")

        b_exp = IOSButton(self, text="eˣ", button_type="scientific", font_size=16, command=lambda: self.on_scientific("exp"))
        b_exp.grid(row=1, column=3, padx=pad_x, pady=pad_y, sticky="nsew")

        b_7 = IOSButton(self, text="7", button_type="number", font_size=20, command=lambda: self.on_digit("7"))
        b_7.grid(row=1, column=4, padx=pad_x, pady=pad_y, sticky="nsew")

        b_8 = IOSButton(self, text="8", button_type="number", font_size=20, command=lambda: self.on_digit("8"))
        b_8.grid(row=1, column=5, padx=pad_x, pady=pad_y, sticky="nsew")

        b_9 = IOSButton(self, text="9", button_type="number", font_size=20, command=lambda: self.on_digit("9"))
        b_9.grid(row=1, column=6, padx=pad_x, pady=pad_y, sticky="nsew")

        b_mul = IOSButton(self, text="×", button_type="operator", font_size=20, command=lambda: self.on_operator("×"))
        b_mul.grid(row=1, column=7, padx=pad_x, pady=pad_y, sticky="nsew")

        # Row 2: Roots/Inverse + Numbers 4, 5, 6, -
        b_inv = IOSButton(self, text="1/x", button_type="scientific", font_size=16, command=lambda: self.on_scientific("inverse"))
        b_inv.grid(row=2, column=0, padx=pad_x, pady=pad_y, sticky="nsew")

        b_sqrt = IOSButton(self, text="√x", button_type="scientific", font_size=16, command=lambda: self.on_scientific("sqrt"))
        b_sqrt.grid(row=2, column=1, padx=pad_x, pady=pad_y, sticky="nsew")

        b_cbrt = IOSButton(self, text="³√x", button_type="scientific", font_size=16, command=lambda: self.on_scientific("cbrt"))
        b_cbrt.grid(row=2, column=2, padx=pad_x, pady=pad_y, sticky="nsew")

        b_fact = IOSButton(self, text="x!", button_type="scientific", font_size=16, command=lambda: self.on_scientific("factorial"))
        b_fact.grid(row=2, column=3, padx=pad_x, pady=pad_y, sticky="nsew")

        b_4 = IOSButton(self, text="4", button_type="number", font_size=20, command=lambda: self.on_digit("4"))
        b_4.grid(row=2, column=4, padx=pad_x, pady=pad_y, sticky="nsew")

        b_5 = IOSButton(self, text="5", button_type="number", font_size=20, command=lambda: self.on_digit("5"))
        b_5.grid(row=2, column=5, padx=pad_x, pady=pad_y, sticky="nsew")

        b_6 = IOSButton(self, text="6", button_type="number", font_size=20, command=lambda: self.on_digit("6"))
        b_6.grid(row=2, column=6, padx=pad_x, pady=pad_y, sticky="nsew")

        b_sub = IOSButton(self, text="-", button_type="operator", font_size=20, command=lambda: self.on_operator("-"))
        b_sub.grid(row=2, column=7, padx=pad_x, pady=pad_y, sticky="nsew")

        # Row 3: Logarithms/Constants + Numbers 1, 2, 3, +
        b_ln = IOSButton(self, text="ln", button_type="scientific", font_size=16, command=lambda: self.on_scientific("ln"))
        b_ln.grid(row=3, column=0, padx=pad_x, pady=pad_y, sticky="nsew")

        b_log = IOSButton(self, text="log", button_type="scientific", font_size=16, command=lambda: self.on_scientific("log10"))
        b_log.grid(row=3, column=1, padx=pad_x, pady=pad_y, sticky="nsew")

        b_pi = IOSButton(self, text="π", button_type="scientific", font_size=16, command=lambda: self.on_scientific("pi"))
        b_pi.grid(row=3, column=2, padx=pad_x, pady=pad_y, sticky="nsew")

        b_e = IOSButton(self, text="e", button_type="scientific", font_size=16, command=lambda: self.on_scientific("e"))
        b_e.grid(row=3, column=3, padx=pad_x, pady=pad_y, sticky="nsew")

        b_1 = IOSButton(self, text="1", button_type="number", font_size=20, command=lambda: self.on_digit("1"))
        b_1.grid(row=3, column=4, padx=pad_x, pady=pad_y, sticky="nsew")

        b_2 = IOSButton(self, text="2", button_type="number", font_size=20, command=lambda: self.on_digit("2"))
        b_2.grid(row=3, column=5, padx=pad_x, pady=pad_y, sticky="nsew")

        b_3 = IOSButton(self, text="3", button_type="number", font_size=20, command=lambda: self.on_digit("3"))
        b_3.grid(row=3, column=6, padx=pad_x, pady=pad_y, sticky="nsew")

        b_add = IOSButton(self, text="+", button_type="operator", font_size=20, command=lambda: self.on_operator("+"))
        b_add.grid(row=3, column=7, padx=pad_x, pady=pad_y, sticky="nsew")

        # Row 4: Memory/Parentheses + 0, comma, =
        b_bk = IOSButton(self, text="⌫", button_type="scientific", font_size=16, command=lambda: self.on_action("backspace"))
        b_bk.grid(row=4, column=0, padx=pad_x, pady=pad_y, sticky="nsew")

        b_lp = IOSButton(self, text="(", button_type="scientific", font_size=16, command=lambda: self.on_action("("))
        b_lp.grid(row=4, column=1, padx=pad_x, pady=pad_y, sticky="nsew")

        b_rp = IOSButton(self, text=")", button_type="scientific", font_size=16, command=lambda: self.on_action(")"))
        b_rp.grid(row=4, column=2, padx=pad_x, pady=pad_y, sticky="nsew")

        b_rand = IOSButton(self, text="Ans", button_type="scientific", font_size=15, command=lambda: self.on_action("Ans"))
        b_rand.grid(row=4, column=3, padx=pad_x, pady=pad_y, sticky="nsew")

        b_0 = IOSButton(self, text="0", button_type="number", font_size=20, command=lambda: self.on_digit("0"))
        b_0.grid(row=4, column=4, columnspan=2, padx=pad_x, pady=pad_y, sticky="nsew")

        b_dot = IOSButton(self, text=",", button_type="number", font_size=20, command=lambda: self.on_action("."))
        b_dot.grid(row=4, column=6, padx=pad_x, pady=pad_y, sticky="nsew")

        b_eq = IOSButton(self, text="=", button_type="operator", font_size=20, command=lambda: self.on_action("="))
        b_eq.grid(row=4, column=7, padx=pad_x, pady=pad_y, sticky="nsew")

    def _toggle_angle(self) -> None:
        self.angle_mode = "Deg" if self.angle_mode == "Rad" else "Rad"
        self.btn_angle.configure(text=self.angle_mode)
        self.on_action(f"ANGLE_{self.angle_mode}")
