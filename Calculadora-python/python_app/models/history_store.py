"""History Store Model (CRUD).

Manages calculation history with local JSON file persistence, defensive I/O,
individual deletion, bulk clearing, and retrieval for reuse.
"""

from dataclasses import asdict, dataclass
from datetime import datetime
import json
import os
from typing import List, Optional
import uuid


@dataclass
class HistoryEntry:
    """Represents a single recorded calculation or conversion event."""

    id: str
    expression: str
    result: str
    mode: str
    created_at: str

    @classmethod
    def create(cls, expression: str, result: str, mode: str = "Simples") -> "HistoryEntry":
        """Factory method creating a new HistoryEntry with generated UUID and timestamp."""
        return cls(
            id=str(uuid.uuid4())[:8],
            expression=expression,
            result=result,
            mode=mode,
            created_at=datetime.now().strftime("%H:%M:%S"),
        )


class HistoryStore:
    """Thread-safe and defensive storage manager for calculator history CRUD."""

    def __init__(self, storage_path: str = "data/history.json", max_entries: int = 100) -> None:
        self.storage_path = storage_path
        self.max_entries = max_entries
        self.entries: List[HistoryEntry] = []
        self._load_from_disk()

    # --- CRUD: CREATE ---
    def add(self, expression: str, result: str, mode: str = "Simples") -> HistoryEntry:
        """Create and store a new calculation entry.

        Prepends to top of history (most recent first) and persists to disk.
        """
        # Skip recording error states in history
        if result in ("Indefinido", "Erro de Sintaxe", "Entrada Inválida", "Estouro de Memória"):
            return None  # type: ignore

        entry = HistoryEntry.create(expression=expression, result=result, mode=mode)
        self.entries.insert(0, entry)

        # Enforce max limit to avoid unbounded file growth
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[: self.max_entries]

        self._save_to_disk()
        return entry

    # --- CRUD: READ ---
    def get_all(self) -> List[HistoryEntry]:
        """Return all stored entries ordered by most recent."""
        return list(self.entries)

    def get_by_id(self, entry_id: str) -> Optional[HistoryEntry]:
        """Find a specific entry by its ID."""
        for entry in self.entries:
            if entry.id == entry_id:
                return entry
        return None

    # --- CRUD: UPDATE / USE ---
    # The 'Use' action is handled by returning the entry values to the controller/view,
    # but we also provide an update method for updating notes/expression if needed.
    def update_expression(self, entry_id: str, new_expression: str) -> bool:
        """Update an existing entry's expression."""
        for entry in self.entries:
            if entry.id == entry_id:
                entry.expression = new_expression
                self._save_to_disk()
                return True
        return False

    # --- CRUD: DELETE ---
    def delete_by_id(self, entry_id: str) -> bool:
        """Delete a single history entry by its ID."""
        initial_len = len(self.entries)
        self.entries = [e for e in self.entries if e.id != entry_id]
        if len(self.entries) < initial_len:
            self._save_to_disk()
            return True
        return False

    def clear(self) -> None:
        """Delete all history entries (bulk delete)."""
        self.entries.clear()
        self._save_to_disk()

    # --- DEFENSIVE PERSISTENCE ---
    def _load_from_disk(self) -> None:
        """Load history from JSON file with defensive fallback for corrupted files."""
        if not os.path.exists(self.storage_path):
            self.entries = []
            return

        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                if isinstance(raw_data, list):
                    self.entries = [
                        HistoryEntry(
                            id=item.get("id", str(uuid.uuid4())[:8]),
                            expression=item.get("expression", ""),
                            result=item.get("result", ""),
                            mode=item.get("mode", "Simples"),
                            created_at=item.get("created_at", ""),
                        )
                        for item in raw_data
                        if isinstance(item, dict)
                    ]
        except (json.JSONDecodeError, OSError, TypeError):
            # Graceful fallback: start fresh without crashing the app
            self.entries = []

    def _save_to_disk(self) -> None:
        """Persist entries to JSON file atomically."""
        try:
            folder = os.path.dirname(self.storage_path)
            if folder:
                os.makedirs(folder, exist_ok=True)
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump([asdict(e) for e in self.entries], f, indent=2, ensure_ascii=False)
        except OSError:
            # If filesystem is read-only or error occurs, history remains in-memory
            pass
