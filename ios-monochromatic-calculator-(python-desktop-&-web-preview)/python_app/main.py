"""Application Entry Point.

Initializes the MVC architecture and launches the CustomTkinter main loop.
Execution:
    python -m python_app.main
    or
    python main.py (from inside python_app)
"""

import os
import sys

# Ensure root directory is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from python_app.controllers.app_controller import AppController
from python_app.views.main_window import MainWindow


def main() -> None:
    """Bootstrap controller and window, and start event loop."""
    controller = AppController()
    app = MainWindow(controller=controller)
    controller.attach_window(app)

    # Launch background refresh for exchange rates without blocking UI
    import threading
    threading.Thread(target=controller.exchange_service.fetch_live_rates, daemon=True).start()

    app.mainloop()


if __name__ == "__main__":
    main()
