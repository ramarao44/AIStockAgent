"""
Normalization layer for market data.

This service sits between the external data source and the analysis modules.
It converts raw stock history into the simplified shape expected by the rest of
application.
"""

from data_sources.yahoo import YahooFinanceClient


class MarketDataService:
    def __init__(self):
        self.client = YahooFinanceClient()

    def get_market_data(self, symbol: str, period: str = "1mo"):
        """Fetch and normalize the latest OHLCV values for a symbol."""
        data = self.client.get_stock_data(symbol, period)

        if data is None:
            return None

        return {
            "symbol": symbol,
            "latest_close": float(data["Close"].iloc[-1]),
            "latest_volume": int(data["Volume"].iloc[-1]),
            "data": data,
        }