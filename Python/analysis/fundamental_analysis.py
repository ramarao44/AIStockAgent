"""
Basic fundamental scoring helpers.

This module represents the fundamental-analysis step in the high-level design.
The current implementation uses lightweight heuristics to keep the project
free and simple while still producing a meaningful signal.
"""


class FundamentalAnalysis:
    def score_basic(self, market_data: dict):
        """Return a lightweight fundamental score from price and volume heuristics."""
        if not market_data:
            return 0

        price = float(market_data.get("latest_close", 0) or 0)
        volume = int(market_data.get("latest_volume", 0) or 0)

        score = 0

        # Simple heuristics to approximate a basic quality signal.
        if price > 100:
            score += 1
        if price > 200:
            score += 1
        if volume > 1_000_000:
            score += 1
        if volume > 5_000_000:
            score += 1

        return score