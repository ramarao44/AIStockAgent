import yfinance as yf


class YahooFinanceClient:
    def get_stock_data(self, symbol: str, period: str = "1mo"):
        """
        Fetch historical stock data from Yahoo Finance.
        """
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)

            if hist.empty:
                raise ValueError(f"No data found for {symbol}")

            return hist

        except Exception as e:
            print(f"[YahooFinanceClient] Error fetching {symbol}: {e}")
            return None