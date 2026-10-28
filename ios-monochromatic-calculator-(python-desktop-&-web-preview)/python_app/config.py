"""Configuration and visual tokens for the iOS Monochromatic Calculator.

Defines styling constants, color palette tokens, typography rules,
window dimensions for each mode, and keyboard shortcut mappings.
"""

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class ColorPalette:
    """Strictly monochromatic iOS palette tokens (black, grays, white)."""

    # Backgrounds
    WINDOW_BG: str = "#000000"           # Pure black base
    CONTAINER_BG: str = "#1C1C1E"        # iOS secondary system background
    SURFACE_BG: str = "#2C2C2E"          # iOS tertiary system background
    SURFACE_HOVER: str = "#3A3A3C"       # Interactive hover state

    # Text & Typography
    TEXT_PRIMARY: str = "#FFFFFF"        # Pure white text
    TEXT_SECONDARY: str = "#8E8E93"      # Muted silver/gray label
    TEXT_DARK: str = "#000000"           # High contrast dark text for light buttons
    TEXT_ACCENT: str = "#E5E5EA"         # Subtle light text for secondary actions

    # Keypads & Buttons
    BTN_NUMBER_BG: str = "#333333"       # Dark gray for numbers 0-9
    BTN_NUMBER_HOVER: str = "#48484A"
    BTN_NUMBER_TEXT: str = "#FFFFFF"

    BTN_FUNCTION_BG: str = "#A5A5A5"     # Light gray for AC, +/-, %
    BTN_FUNCTION_HOVER: str = "#D1D1D6"
    BTN_FUNCTION_TEXT: str = "#000000"

    BTN_OPERATOR_BG: str = "#505050"     # Mid gray for +, -, *, /, = (No orange)
    BTN_OPERATOR_HOVER: str = "#636366"
    BTN_OPERATOR_TEXT: str = "#FFFFFF"
    BTN_OPERATOR_ACTIVE_BG: str = "#FFFFFF"
    BTN_OPERATOR_ACTIVE_TEXT: str = "#000000"

    BTN_SCIENTIFIC_BG: str = "#242426"   # Deep graphite for scientific functions
    BTN_SCIENTIFIC_HOVER: str = "#3A3A3C"
    BTN_SCIENTIFIC_TEXT: str = "#D1D1D6"

    # Borders & Dividers
    BORDER_SUBTLE: str = "#2C2C2E"
    DIVIDER: str = "#38383A"
    ALERT_ERROR: str = "#D1D1D6"


@dataclass(frozen=True)
class WindowSizes:
    """Dimensions (width, height) for each operational mode."""

    SIMPLE: Tuple[int, int] = (360, 580)
    SCIENTIFIC: Tuple[int, int] = (680, 580)
    CONVERTER: Tuple[int, int] = (420, 620)
    MIN_SIMPLE: Tuple[int, int] = (340, 540)
    MIN_SCIENTIFIC: Tuple[int, int] = (620, 540)
    MIN_CONVERTER: Tuple[int, int] = (380, 580)


# Global instances for convenient import across modules
COLORS = ColorPalette()
SIZES = WindowSizes()

# Default files paths
DEFAULT_HISTORY_FILE: str = "data/history.json"
DEFAULT_CACHE_FILE: str = "data/exchange_cache.json"

# Public Exchange Rate API with offline base fallback
EXCHANGE_API_URL: str = "https://open.er-api.com/v6/latest/USD"
