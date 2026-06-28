import sys
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from integrations.whatsapp_webhook import router as whatsapp_router

PYTHON_ROOT = Path(__file__).resolve().parent.parent / "Python"
if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))

from services.watchlist_service import WatchlistService
from services.market_data_service import MarketDataService
from analysis.techincal_analysis import TechnicalAnalysis
from analysis.fundamental_analysis import FundamentalAnalysis
from analysis.decision_engine import DecisionEngine

app = FastAPI(title="AIStockAgent")
app.include_router(whatsapp_router)


class StockRequest(BaseModel):
    symbol: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze-stock")
def analyze_stock(request: StockRequest):
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
