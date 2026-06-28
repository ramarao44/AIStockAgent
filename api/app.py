"""
FastAPI entry point for AIStockAgent.

This file is the delivery layer in the high-level design. It exposes HTTP
endpoints that allow a client or automation workflow to trigger the stock
analysis pipeline.
"""

import sys
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from integrations.whatsapp_webhook import router as whatsapp_router

# Allow imports from the Python package directory when the app is run directly.
PYTHON_ROOT = Path(__file__).resolve().parent.parent / "Python"
if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))

from services.market_data_service import MarketDataService
from analysis.techincal_analysis import TechnicalAnalysis
from analysis.fundamental_analysis import FundamentalAnalysis
from analysis.decision_engine import DecisionEngine

app = FastAPI(title="AIStockAgent")
# Register the WhatsApp webhook router so inbound messages can be handled.
app.include_router(whatsapp_router)


class StockRequest(BaseModel):
    """Request model for a single-symbol analysis request."""

    symbol: str


@app.get("/health")
def health():
    """Simple liveness check for local testing and monitoring."""
    return {"status": "ok"}


@app.post("/analyze-stock")
def analyze_stock(request: StockRequest):
    """
    Orchestrates the analysis pipeline for one symbol.

    Flow:
    1. Fetch market data
    2. Compute technical indicators
    3. Score fundamentals
    4. Generate final BUY/SELL/HOLD decision
    """
    market_service = MarketDataService()
    ta = TechnicalAnalysis()
    fa = FundamentalAnalysis()
    decision_engine = DecisionEngine()

    market_data = market_service.get_market_data(request.symbol)
    if not market_data:
        return {
            "symbol": request.symbol,
            "status": "error",
            "reason": "No market data available",
        }

    technical = ta.get_trend_signal(market_data["data"])
    fundamental_score = fa.score_basic(market_data)
    risk_level = "low" if fundamental_score >= 3 else "medium"
    decision = decision_engine.generate_decision(
        technical=technical,
        fundamental={"score": fundamental_score},
        risk={"risk_level": risk_level},
    )

    return {
        "symbol": request.symbol,
        "status": "ok",
        "latest_close": market_data.get("latest_close"),
        "latest_volume": market_data.get("latest_volume"),
        "technical": technical,
        "fundamental_score": fundamental_score,
        "decision": decision["decision"],
        "confidence": decision["confidence"],
        "reasoning": decision["reasoning"],
    }
