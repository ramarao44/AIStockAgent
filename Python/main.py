"""
Command-line entry point for the stock analysis pipeline.

This script represents the batch-processing side of the high-level design:
read a watchlist, fetch market data, run technical/fundamental analysis, and
emit a JSON result for each symbol.
"""

import json

from services.watchlist_service import WatchlistService
from services.market_data_service import MarketDataService
from analysis.techincal_analysis import TechnicalAnalysis
from analysis.fundamental_analysis import FundamentalAnalysis
from analysis.decision_engine import DecisionEngine
from utils.logger import get_logger


def main():
    logger = get_logger()

    # Input layer: read the configured watchlist.
    watchlist_service = WatchlistService()
    symbols = watchlist_service.get_symbols()
    logger.info(f"Loaded symbols: {symbols}")

    # Core services used by the analysis pipeline.
    market_service = MarketDataService()
    ta = TechnicalAnalysis()
    fa = FundamentalAnalysis()
    decision_engine = DecisionEngine()

    results = []

    for symbol in symbols:
        try:
            logger.info(f"Processing {symbol}")

            # Data layer: retrieve the latest market data for the symbol.
            market_data = market_service.get_market_data(symbol)
            if not market_data:
                results.append({"symbol": symbol, "status": "skipped", "reason": "No market data"})
                continue

            # Analysis layer: compute the technical and fundamental signals.
            technical = ta.get_trend_signal(market_data["data"])
            score = fa.score_basic(market_data)
            risk_level = "low" if score >= 3 else "medium"

            # Decision layer: turn the signals into a BUY/SELL/HOLD recommendation.
            decision = decision_engine.generate_decision(
                technical=technical,
                fundamental={"score": score},
                risk={"risk_level": risk_level},
            )

            output = {
                "symbol": symbol,
                "status": "ok",
                "latest_close": market_data.get("latest_close"),
                "latest_volume": market_data.get("latest_volume"),
                "technical": technical,
                "fundamental_score": score,
                "decision": decision["decision"],
                "confidence": decision["confidence"],
                "reasoning": decision["reasoning"],
            }
            results.append(output)
            logger.info(f"{symbol} -> {json.dumps(output, default=str)}")
        except Exception as exc:
            logger.exception(f"Failed to process {symbol}: {exc}")
            results.append({"symbol": symbol, "status": "error", "reason": str(exc)})

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()