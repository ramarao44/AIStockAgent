"""
External market data adapter for Yahoo Finance.

This module represents the data-source layer from the high-level design.
It isolates the rest of the codebase from the details of the Yahoo Finance API.
"""

import yfinance as yf


class YahooFinanceClient:
    def get_stock_data(self, symbol: str, period: str = "1mo"):
        """Fetch historical stock data for a symbol from Yahoo Finance."""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)

            if hist.empty:
                raise ValueError(f"No data found for {symbol}")

            return hist

        except Exception as e:
            print(f"[YahooFinanceClient] Error fetching {symbol}: {e}")
            return None