"""Main Application Window.

Orchestrates mode switching, layout adaptation, history drawer display,
and delegates interactions to the Application Controller.
"""

from typing import Callable, Optional
import customtkinter as ctk  # type: ignore

from python_app.config import COLORS, SIZES
from python_app.views.components import DisplayWidget
from python_app.views.converter_view import ConverterView
from python_app.views.history_drawer import HistoryDrawer
from python_app.views.scientific_pad import ScientificPad
from python_app.views.simple_pad import SimplePad


class MainWindow(ctk.CTk):
    """Root CustomTkinter window implementing the iOS monochromatic calculator."""

    def __init__(self, controller: any) -> None:
        super().__init__()

        self.controller = controller
        self.current_mode = "Simples"
        self.is_history_open = False

        # Apply dark mode and title
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("Calculadora")
        self.configure(fg_color=COLORS.WINDOW_BG)
        self.geometry(f"{SIZES.SIMPLE[0]}x{SIZES.SIMPLE[1]}")
        self.minsize(SIZES.MIN_SIMPLE[0], SIZES.MIN_SIMPLE[1])

        self._build_shell()
        self._setup_bindings()

    def _build_shell(self) -> None:
        # Top Navigation Bar: Mode Segmented Switcher + History Toggle
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.pack(fill="x", padx=14, pady=(12, 8))

        self.mode_switcher = ctk.CTkSegmentedButton(
            self.top_bar,
            values=["Simples", "Científica", "Conversor"],
            command=self._on_mode_change_requested,
            fg_color=COLORS.SURFACE_BG,
            selected_color=COLORS.BTN_FUNCTION_BG,
            selected_hover_color=COLORS.BTN_FUNCTION_HOVER,
            unselected_color=COLORS.SURFACE_BG,
            unselected_hover_color=COLORS.SURFACE_HOVER,
            text_color=COLORS.TEXT_PRIMARY,
            font=ctk.CTkFont(family="SF Pro Text", size=12, weight="bold"),
        )
        self.mode_switcher.set("Simples")
        self.mode_switcher.pack(side="left", expand=True, fill="x", padx=(0, 8))

        self.btn_history = ctk.CTkButton(
            self.top_bar,
            text="🕒",
            width=36,
            height=32,
            corner_radius=16,
            fg_color=COLORS.SURFACE_BG,
            hover_color=COLORS.SURFACE_HOVER,
            text_color=COLORS.TEXT_PRIMARY,
            font=ctk.CTkFont(size=14),
            command=self.toggle_history_drawer,
        )
        self.btn_history.pack(side="right")

        # Main horizontal container (Content on left, History drawer on right when open)
        self.body_container = ctk.CTkFrame(self, fg_color="transparent")
        self.body_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.left_column = ctk.CTkFrame(self.body_container, fg_color="transparent")
        self.left_column.pack(side="left", fill="both", expand=True)

        # Upper Display Widget (shared between Simple and Scientific)
        self.display = DisplayWidget(self.left_column)
        self.display.pack(fill="x", padx=4, pady=(0, 10))

        # Pad Container where SimplePad, ScientificPad, ConverterView are swapped
        self.pad_container = ctk.CTkFrame(self.left_column, fg_color="transparent")
        self.pad_container.pack(fill="both", expand=True)

        # Initialize View Pads
        self.simple_pad = SimplePad(
            self.pad_container,
            on_digit=self.controller.handle_digit,
            on_operator=self.controller.handle_operator,
            on_action=self.controller.handle_action,
        )

        self.scientific_pad = ScientificPad(
            self.pad_container,
            on_digit=self.controller.handle_digit,
            on_operator=self.controller.handle_operator,
            on_action=self.controller.handle_action,
            on_scientific=self.controller.handle_scientific,
        )

        self.converter_view = ConverterView(
            self.pad_container,
            unit_converter=self.controller.unit_converter,
            on_history_record=self.controller.record_conversion_history,
        )

        # Initialize History Drawer
        self.history_drawer = HistoryDrawer(
            self.body_container,
            history_store=self.controller.history_store,
            on_use_entry=self.controller.handle_use_history,
            on_close=self.toggle_history_drawer,
            width=260,
        )

        # Default mode: Simples
        self.simple_pad.pack(fill="both", expand=True)

    def set_mode(self, mode: str) -> None:
        """Switch between Simples, Científica, and Conversor views and adapt window geometry."""
        if mode == self.current_mode:
            return

        self.current_mode = mode
        self.mode_switcher.set(mode)

        # Hide all pads
        self.simple_pad.pack_forget()
        self.scientific_pad.pack_forget()
        self.converter_view.pack_forget()

        # Adapt geometry and show requested pad
        if mode == "Simples":
            self.display.pack(fill="x", padx=4, pady=(0, 10))
            self.simple_pad.pack(fill="both", expand=True)
            target_w, target_h = SIZES.SIMPLE
        elif mode == "Científica":
            self.display.pack(fill="x", padx=4, pady=(0, 10))
            self.scientific_pad.pack(fill="both", expand=True)
            target_w, target_h = SIZES.SCIENTIFIC
        elif mode == "Conversor":
            self.display.pack_forget()  # Converter has dedicated card
            self.converter_view.pack(fill="both", expand=True)
            target_w, target_h = SIZES.CONVERTER
        else:
            return

        if self.is_history_open:
            target_w += 260

        self.geometry(f"{target_w}x{target_h}")

    def toggle_history_drawer(self) -> None:
        """Open or close the retractable side history drawer."""
        self.is_history_open = not self.is_history_open

        current_w = self.winfo_width()
        current_h = self.winfo_height()

        if self.is_history_open:
            self.history_drawer.refresh()
            self.history_drawer.pack(side="right", fill="y", padx=(6, 0))
            self.geometry(f"{current_w + 260}x{current_h}")
            self.btn_history.configure(fg_color=COLORS.BTN_FUNCTION_BG, text_color=COLORS.TEXT_DARK)
        else:
            self.history_drawer.pack_forget()
            self.geometry(f"{max(340, current_w - 260)}x{current_h}")
            self.btn_history.configure(fg_color=COLORS.SURFACE_BG, text_color=COLORS.TEXT_PRIMARY)

    def _on_mode_change_requested(self, mode: str) -> None:
        self.controller.switch_mode(mode)

    def _setup_bindings(self) -> None:
        """Bind global keyboard shortcuts for seamless accessibility."""
        self.bind("<Key>", self._on_key_press)

    def _on_key_press(self, event) -> None:
        """Delegate raw Tkinter key events to controller."""
        self.controller.handle_key_event(event)
