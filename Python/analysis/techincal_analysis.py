"""
Technical analysis helpers.

This module maps to the technical-analysis layer in the high-level design.
It converts historical price data into simple trend signals that can be used by
later decision-making logic.
"""

import pandas as pd


class TechnicalAnalysis:
    def simple_moving_average(self, data: pd.DataFrame, window: int = 5):
        """Calculate a simple moving average for the Close series."""
        if data is None or data.empty:
            return None

        close = pd.to_numeric(data["Close"], errors="coerce")
        return close.rolling(window=window, min_periods=window).mean()

    def price_change(self, data: pd.DataFrame):
        """Calculate the percentage change from one day to the next."""
        if data is None or data.empty:
            return None

        close = pd.to_numeric(data["Close"], errors="coerce")
        return close.pct_change()

    def get_trend_signal(self, data: pd.DataFrame, window: int = 3):
        """Return a lightweight trend summary for downstream decision logic."""
        if data is None or data.empty:
            return {"trend": "neutral", "momentum": 0.0, "sma": None}

        close = pd.to_numeric(data["Close"], errors="coerce").dropna()
        if close.empty or len(close) < 2:
            return {"trend": "neutral", "momentum": 0.0, "sma": None}

        latest_price = float(close.iloc[-1])
        previous_price = float(close.iloc[-2])
        momentum = (latest_price - previous_price) / previous_price if previous_price else 0.0

        # Compare the latest price against the moving average to infer the trend.
        sma = self.simple_moving_average(pd.DataFrame({"Close": close}), window=window)
        latest_sma = None
        if sma is None or sma.empty or pd.isna(sma.iloc[-1]):
            trend = "neutral"
        else:
            latest_sma = float(sma.iloc[-1])
            if latest_price > latest_sma and momentum > 0.0:
                trend = "bullish"
            elif latest_price < latest_sma and momentum < 0.0:
                trend = "bearish"
            else:
                trend = "neutral"

        return {
            "trend": trend,
            "momentum": round(momentum, 4),
            "sma": round(float(latest_sma), 4) if sma is not None and not sma.empty and not pd.isna(sma.iloc[-1]) else None,
        }