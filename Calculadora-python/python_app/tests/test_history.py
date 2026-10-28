"""Unit tests for HistoryStore model CRUD operations."""

import os
import unittest
from python_app.models.history_store import HistoryStore

TEST_HISTORY_FILE = "data/test_history.json"


class TestHistoryStore(unittest.TestCase):
    """Test suite for History CRUD operations and persistence."""

    def setUp(self) -> None:
        if os.path.exists(TEST_HISTORY_FILE):
            os.remove(TEST_HISTORY_FILE)
        self.store = HistoryStore(storage_path=TEST_HISTORY_FILE, max_entries=5)

    def tearDown(self) -> None:
        if os.path.exists(TEST_HISTORY_FILE):
            os.remove(TEST_HISTORY_FILE)

    def test_create_and_read_entry(self) -> None:
        entry = self.store.add("5 + 5", "10", mode="Simples")
        self.assertIsNotNone(entry)
        self.assertEqual(entry.expression, "5 + 5")
        self.assertEqual(entry.result, "10")

        all_entries = self.store.get_all()
        self.assertEqual(len(all_entries), 1)
        self.assertEqual(all_entries[0].id, entry.id)

    def test_persistence_across_instances(self) -> None:
        self.store.add("10 × 2", "20", mode="Simples")
        # Instantiate second store pointing to same file
        store2 = HistoryStore(storage_path=TEST_HISTORY_FILE)
        entries2 = store2.get_all()
        self.assertEqual(len(entries2), 1)
        self.assertEqual(entries2[0].result, "20")

    def test_delete_individual_entry(self) -> None:
        e1 = self.store.add("1 + 1", "2")
        e2 = self.store.add("2 + 2", "4")
        self.assertEqual(len(self.store.get_all()), 2)

        deleted = self.store.delete_by_id(e1.id)
        self.assertTrue(deleted)
        remaining = self.store.get_all()
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].id, e2.id)

    def test_clear_all_entries(self) -> None:
        self.store.add("3 + 3", "6")
        self.store.add("4 + 4", "8")
        self.store.clear()
        self.assertEqual(len(self.store.get_all()), 0)

    def test_error_results_not_saved(self) -> None:
        # Erroneous results should not pollute history
        entry = self.store.add("1 / 0", "Indefinido")
        self.assertIsNone(entry)
        self.assertEqual(len(self.store.get_all()), 0)


if __name__ == "__main__":
    unittest.main()
