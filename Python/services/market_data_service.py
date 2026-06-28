from data_sources.yahoo import YahooFinanceClient


class MarketDataService:
    def __init__(self):
        self.client = YahooFinanceClient()

    def get_market_data(self, symbol: str, period: str = "1mo"):
        """
        Returns cleaned market data for a symbol.
        """
        data = self.client.get_stock_data(symbol, period)

        if data is None:
            return None

        return {
            "symbol": symbol,
            "latest_close": float(data["Close"].iloc[-1]),
            "latest_volume": int(data["Volume"].iloc[-1]),
            "data": data
        }