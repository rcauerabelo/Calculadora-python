"""History drawer view for full CRUD operations."""

from typing import Callable, List, Optional
import customtkinter as ctk  # type: ignore

from python_app.config import COLORS
from python_app.models.history_store import HistoryEntry, HistoryStore


class HistoryDrawer(ctk.CTkFrame):
    """Side panel displaying calculation history with interactive reuse and deletion."""

    def __init__(
        self,
        master: any,
        history_store: HistoryStore,
        on_use_entry: Callable[[str], None],
        on_close: Callable[[], None],
        **kwargs,
    ) -> None:
        super().__init__(master=master, fg_color=COLORS.CONTAINER_BG, corner_radius=16, **kwargs)

        self.history_store = history_store
        self.on_use_entry = on_use_entry
        self.on_close = on_close

        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        # Header with Title and Close button
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(12, 8))

        title = ctk.CTkLabel(
            header,
            text="Histórico",
            font=ctk.CTkFont(family="SF Pro Display", size=18, weight="bold"),
            text_color=COLORS.TEXT_PRIMARY,
        )
        title.pack(side="left")

        btn_close = ctk.CTkButton(
            header,
            text="✕",
            width=28,
            height=28,
            corner_radius=14,
            fg_color=COLORS.SURFACE_BG,
            hover_color=COLORS.SURFACE_HOVER,
            text_color=COLORS.TEXT_SECONDARY,
            command=self.on_close,
        )
        btn_close.pack(side="right")

        # Scrollable list for CRUD Read
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=COLORS.SURFACE_HOVER,
            scrollbar_button_hover_color=COLORS.BTN_OPERATOR_BG,
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # Footer with Clear All (CRUD Delete Bulk)
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", padx=12, pady=(0, 12))

        self.btn_clear_all = ctk.CTkButton(
            footer,
            text="Limpar Histórico",
            height=34,
            corner_radius=17,
            fg_color=COLORS.SURFACE_BG,
            hover_color="#3A1C1C",
            text_color="#FF453A",
            font=ctk.CTkFont(family="SF Pro Text", size=12, weight="bold"),
            command=self._clear_all,
        )
        self.btn_clear_all.pack(fill="x")

    def refresh(self) -> None:
        """Reload entries from HistoryStore and populate the scroll frame."""
        # Clear existing widgets
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        entries: List[HistoryEntry] = self.history_store.get_all()

        if not entries:
            empty_lbl = ctk.CTkLabel(
                self.scroll_frame,
                text="Nenhum cálculo recente.",
                font=ctk.CTkFont(family="SF Pro Text", size=13),
                text_color=COLORS.TEXT_SECONDARY,
            )
            empty_lbl.pack(pady=40)
            self.btn_clear_all.configure(state="disabled")
            return

        self.btn_clear_all.configure(state="normal")

        for entry in entries:
            self._render_entry_card(entry)

    def _render_entry_card(self, entry: HistoryEntry) -> None:
        card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=COLORS.SURFACE_BG,
            corner_radius=12,
        )
        card.pack(fill="x", pady=4, padx=2)

        # Upper row: Mode tag + Timestamp + Delete button (CRUD Delete)
        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=10, pady=(8, 2))

        meta_text = f"{entry.mode} · {entry.created_at}"
        lbl_meta = ctk.CTkLabel(
            top_row,
            text=meta_text,
            font=ctk.CTkFont(family="SF Pro Text", size=10),
            text_color=COLORS.TEXT_SECONDARY,
        )
        lbl_meta.pack(side="left")

        btn_del = ctk.CTkButton(
            top_row,
            text="🗑",
            width=22,
            height=22,
            corner_radius=11,
            fg_color="transparent",
            hover_color="#3A1C1C",
            text_color=COLORS.TEXT_SECONDARY,
            font=ctk.CTkFont(size=11),
            command=lambda eid=entry.id: self._delete_entry(eid),
        )
        btn_del.pack(side="right")

        # Expression row
        lbl_expr = ctk.CTkLabel(
            card,
            text=entry.expression,
            font=ctk.CTkFont(family="SF Pro Text", size=13),
            text_color=COLORS.TEXT_SECONDARY,
            anchor="w",
        )
        lbl_expr.pack(fill="x", padx=10, pady=(0, 2))

        # Result row with "Usar" action (CRUD Update / Reuse)
        bottom_row = ctk.CTkFrame(card, fg_color="transparent")
        bottom_row.pack(fill="x", padx=10, pady=(0, 8))

        lbl_res = ctk.CTkLabel(
            bottom_row,
            text=f"= {entry.result}",
            font=ctk.CTkFont(family="SF Pro Display", size=18, weight="bold"),
            text_color=COLORS.TEXT_PRIMARY,
            anchor="w",
        )
        lbl_res.pack(side="left", expand=True, fill="x")

        btn_use = ctk.CTkButton(
            bottom_row,
            text="Usar",
            width=50,
            height=26,
            corner_radius=13,
            fg_color=COLORS.BTN_OPERATOR_BG,
            hover_color=COLORS.BTN_OPERATOR_HOVER,
            text_color=COLORS.TEXT_PRIMARY,
            font=ctk.CTkFont(family="SF Pro Text", size=11, weight="bold"),
            command=lambda val=entry.result: self.on_use_entry(val),
        )
        btn_use.pack(side="right")

    def _delete_entry(self, entry_id: str) -> None:
        self.history_store.delete_by_id(entry_id)
        self.refresh()

    def _clear_all(self) -> None:
        self.history_store.clear()
        self.refresh()
