class FundamentalAnalysis:
    def score_basic(self, market_data: dict):
        """
        Very basic scoring logic (placeholder for real fundamentals).
        """
        if not market_data:
            return 0

        price = float(market_data.get("latest_close", 0) or 0)
        volume = int(market_data.get("latest_volume", 0) or 0)

        score = 0

        if price > 100:
            score += 1
        if price > 200:
            score += 1
        if volume > 1_000_000:
            score += 1
        if volume > 5_000_000:
            score += 1

        return score