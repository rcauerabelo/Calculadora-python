"""Exchange rate service for currency conversion.

Provides live rate fetching from public exchange API with resilient
offline JSON caching and pre-configured fallback base rates.
"""

from datetime import datetime
import json
import os
from typing import Dict, Optional
import urllib.request
import urllib.error

# Resilient offline base exchange rates relative to USD (1 USD = X)
DEFAULT_OFFLINE_RATES: Dict[str, float] = {
    "USD": 1.0,
    "BRL": 5.45,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 152.3,
    "CAD": 1.38,
    "CHF": 0.87,
    "AUD": 1.51,
    "BTC": 0.000015,
}


class ExchangeRateService:
    """Manages currency exchange rates with cache-first and offline resilience."""

    def __init__(self, cache_file: str = "data/exchange_cache.json") -> None:
        self.cache_file = cache_file
        self.rates: Dict[str, float] = dict(DEFAULT_OFFLINE_RATES)
        self.last_updated: Optional[datetime] = None
        self._load_cache()

    def get_rate(self, from_currency: str, to_currency: str) -> float:
        """Calculate the conversion multiplier from from_currency to to_currency.

        Raises:
            KeyError: If one of the currencies is not supported.
        """
        from_cur = from_currency.upper()
        to_cur = to_currency.upper()

        if from_cur not in self.rates:
            raise KeyError(f"Moeda de origem não suportada: {from_cur}")
        if to_cur not in self.rates:
            raise KeyError(f"Moeda de destino não suportada: {to_cur}")

        # Rates are USD-based: 1 USD = rate
        # Value in USD = val / rates[from]
        # Value in TO = USD_val * rates[to] = val * (rates[to] / rates[from])
        from_rate = self.rates[from_cur]
        to_rate = self.rates[to_cur]
        return to_rate / from_rate

    def fetch_live_rates(self, timeout: float = 3.0) -> bool:
        """Fetch updated exchange rates from public API without external dependencies.

        Uses standard library urllib.request to avoid hard dependency failures.
        """
        api_url = "https://open.er-api.com/v6/latest/USD"
        try:
            req = urllib.request.Request(
                api_url,
                headers={"User-Agent": "iOS-Monochrome-Calculator/1.0"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    api_rates = data.get("rates", {})
                    # Update known currencies
                    for code in self.rates.keys():
                        if code in api_rates and isinstance(api_rates[code], (int, float)):
                            self.rates[code] = float(api_rates[code])
                    self.last_updated = datetime.now()
                    self._save_cache()
                    return True
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
            # Defensive fallback to offline rates without crashing
            pass
        return False

    def _load_cache(self) -> None:
        """Load cached rates from disk if file exists."""
        if not os.path.exists(self.cache_file):
            return
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                payload = json.load(f)
                cached_rates = payload.get("rates", {})
                for k, v in cached_rates.items():
                    if isinstance(v, (int, float)):
                        self.rates[k] = float(v)
                if "updated_at" in payload:
                    self.last_updated = datetime.fromisoformat(payload["updated_at"])
        except (json.JSONDecodeError, OSError, ValueError):
            # Corrupted cache: maintain default offline rates
            pass

    def _save_cache(self) -> None:
        """Persist rates to disk safely."""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            payload = {
                "rates": self.rates,
                "updated_at": self.last_updated.isoformat() if self.last_updated else datetime.now().isoformat()
            }
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
        except OSError:
            pass
