"""Reusable UI components adhering to iOS monochromatic aesthetics.

Implements rounded buttons, high-contrast typography, and two-tier display.
Uses CustomTkinter for modern desktop rendering.
"""

from typing import Callable, Optional
import customtkinter as ctk  # type: ignore

from python_app.config import COLORS


class IOSButton(ctk.CTkButton):
    """Button styled with iOS design language (rounded geometry, smooth hover, monochromatic)."""

    def __init__(
        self,
        master: any,
        text: str,
        command: Optional[Callable[[], None]] = None,
        button_type: str = "number",  # "number", "function", "operator", "scientific", "danger"
        width: int = 68,
        height: int = 68,
        corner_radius: int = 34,
        font_size: int = 24,
        **kwargs,
    ) -> None:
        # Determine color tokens by button role
        if button_type == "function":
            fg_color = COLORS.BTN_FUNCTION_BG
            hover_color = COLORS.BTN_FUNCTION_HOVER
            text_color = COLORS.BTN_FUNCTION_TEXT
            font_weight = "bold"
        elif button_type == "operator":
            fg_color = COLORS.BTN_OPERATOR_BG
            hover_color = COLORS.BTN_OPERATOR_HOVER
            text_color = COLORS.BTN_OPERATOR_TEXT
            font_weight = "bold"
        elif button_type == "scientific":
            fg_color = COLORS.BTN_SCIENTIFIC_BG
            hover_color = COLORS.BTN_SCIENTIFIC_HOVER
            text_color = COLORS.BTN_SCIENTIFIC_TEXT
            font_weight = "normal"
        elif button_type == "danger":
            fg_color = "#3A1C1C"
            hover_color = "#5A2828"
            text_color = "#FF453A"
            font_weight = "bold"
        else:  # "number" default
            fg_color = COLORS.BTN_NUMBER_BG
            hover_color = COLORS.BTN_NUMBER_HOVER
            text_color = COLORS.BTN_NUMBER_TEXT
            font_weight = "normal"

        super().__init__(
            master=master,
            text=text,
            command=command,
            width=width,
            height=height,
            corner_radius=corner_radius,
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=text_color,
            font=ctk.CTkFont(family="SF Pro Display", size=font_size, weight=font_weight),
            **kwargs,
        )


class DisplayWidget(ctk.CTkFrame):
    """Two-tier display showing active mathematical expression and main result."""

    def __init__(self, master: any, **kwargs) -> None:
        super().__init__(
            master=master,
            fg_color=COLORS.CONTAINER_BG,
            corner_radius=16,
            **kwargs,
        )

        # Upper secondary preview label
        self.expression_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(family="SF Pro Text", size=16),
            text_color=COLORS.TEXT_SECONDARY,
            anchor="e",
        )
        self.expression_label.pack(fill="x", padx=16, pady=(12, 2))

        # Lower primary result label (large high-contrast digits)
        self.result_label = ctk.CTkLabel(
            self,
            text="0",
            font=ctk.CTkFont(family="SF Pro Display", size=44, weight="bold"),
            text_color=COLORS.TEXT_PRIMARY,
            anchor="e",
        )
        self.result_label.pack(fill="x", padx=16, pady=(0, 14))

    def update_display(self, expression: str, result: str) -> None:
        """Update both tiers of the display with dynamic font sizing for large numbers."""
        self.expression_label.configure(text=expression)

        # Scale down font size dynamically if number length is large
        clean_len = len(result)
        if clean_len > 14:
            font_size = 24
        elif clean_len > 10:
            font_size = 32
        elif clean_len > 8:
            font_size = 38
        else:
            font_size = 44

        self.result_label.configure(
            text=result,
            font=ctk.CTkFont(family="SF Pro Display", size=font_size, weight="bold"),
        )
