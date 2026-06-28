1. n8n WORKFLOW (IMPORT-READY JSON)

👉 Save as:
automation/n8n_workflow.json

{
  "name": "AIStockAgent Daily WhatsApp Report",
  "nodes": [
    {
      "parameters": {
        "triggerTimes": {
          "item": [
            {
              "hour": 18,
              "minute": 30
            }
          ]
        }
      },
      "name": "Daily Cron",
      "type": "n8n-nodes-base.cron",
      "typeVersion": 1,
      "position": [200, 300]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/daily-report",
        "method": "GET"
      },
      "name": "Call FastAPI",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [450, 300]
    },
    {
      "parameters": {
        "functionCode": "return [{ json: { message: $json.report } }];"
      },
      "name": "Format Message",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [700, 300]
    },
    {
      "parameters": {
        "requestMethod": "POST",
        "url": "https://graph.facebook.com/v18.0/YOUR_PHONE_NUMBER_ID/messages",
        "jsonParameters": true,
        "options": {},
        "bodyParametersJson": "{ \"messaging_product\": \"whatsapp\", \"to\": \"YOUR_PHONE_NUMBER\", \"type\": \"text\", \"text\": { \"body\": \"={{$json.message}}\" } }"
      },
      "name": "Send WhatsApp",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [950, 300]
    }
  ],
  "connections": {
    "Daily Cron": {
      "main": [[{ "node": "Call FastAPI", "type": "main", "index": 0 }]]
    },
    "Call FastAPI": {
      "main": [[{ "node": "Format Message", "type": "main", "index": 0 }]]
    },
    "Format Message": {
      "main": [[{ "node": "Send WhatsApp", "type": "main", "index": 0 }]]
    }
  }
}
⚡ 2. FASTAPI FULL STARTER CODE (CORE ENGINE)

👉 Save as:
backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from backend.core.orchestrator import analyze_stock
from backend.core.daily_report import generate_daily_report

app = FastAPI(title="AIStockAgent")

class StockRequest(BaseModel):
    symbol: str

class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.post("/analyze-stock")
def analyze(req: StockRequest):
    return analyze_stock(req.symbol)


@app.post("/chat")
def chat(req: ChatRequest):
    return {
        "response": analyze_stock(req.message)  # simplified router
    }


@app.get("/daily-report")
def daily_report():
    return {
        "report": generate_daily_report()
    }
🧠 Core Orchestrator

👉 backend/core/orchestrator.py

from backend.data.yahoo_client import get_stock_data
from backend.indicators.technical import analyze_technical
from backend.fundamentals.fundamentals import analyze_fundamentals
from backend.news.news_service import analyze_news
from backend.risk.risk_engine import compute_risk
from backend.regime.regime_detector import detect_regime
from backend.core.decision_engine import make_decision


def analyze_stock(symbol: str):

    data = get_stock_data(symbol)
    tech = analyze_technical(symbol)
    fund = analyze_fundamentals(symbol)
    news = analyze_news(symbol)
    risk = compute_risk(data)
    regime = detect_regime(symbol)

    decision = make_decision(
        technical=tech,
        fundamental=fund,
        news=news,
        risk=risk,
        regime=regime
    )

    return {
        "symbol": symbol,
        "price": data["price"],
        "technical": tech,
        "fundamental": fund,
        "news": news,
        "risk": risk,
        "regime": regime,
        "decision": decision
    }
📊 Decision Engine

👉 backend/core/decision_engine.py

def make_decision(technical, fundamental, news, risk, regime):

    score = 0

    # technical weight
    if technical["rsi"] < 30:
        score += 0.3
    if technical["trend"] == "bullish":
        score += 0.2

    # fundamentals
    score += fundamental["fundamental_score"] * 0.2 / 10

    # news sentiment
    score += news["score"] * 0.2

    # risk penalty
    score -= risk["risk_score"] * 0.3

    # regime filter
    if regime["regime"] == "bear":
        score -= 0.2

    if score > 0.7:
        decision = "BUY"
    elif score > 0.4:
        decision = "HOLD"
    else:
        decision = "SELL"

    return {
        "decision": decision,
        "confidence": round(score, 2)
    }
📱 3. WHATSAPP BOT (END-TO-END IMPLEMENTATION)

We will use:
👉 WhatsApp Cloud API

📦 WhatsApp Service

👉 backend/integrations/whatsapp.py

import requests

ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"

def send_message(to: str, message: str):

    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()
📡 Webhook Receiver (incoming messages)

👉 backend/api/whatsapp_webhook.py

from fastapi import APIRouter, Request
from backend.core.orchestrator import analyze_stock
from backend.integrations.whatsapp import send_message

router = APIRouter()

@router.post("/whatsapp/webhook")
async def whatsapp_webhook(req: Request):

    data = await req.json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        user_text = message["text"]["body"]
        user_phone = message["from"]

        result = analyze_stock(user_text)

        reply = f"""
📊 {result['symbol']} Analysis

Decision: {result['decision']['decision']}
Confidence: {result['decision']['confidence']}

Risk: {result['risk']['risk_score']}
"""

        send_message(user_phone, reply)

        return {"status": "ok"}

    except Exception as e:
        return {"error": str(e)}
🚀 WHAT YOU NOW HAVE

You now have a complete working system blueprint:

🧠 Core AI System

✔ Stock analysis engine
✔ Risk engine
✔ Market regime detection
✔ Decision engine

⚡ API Layer

✔ FastAPI backend
✔ /analyze-stock
✔ /chat
✔ /daily-report

📱 WhatsApp System

✔ Incoming chat processing
✔ AI response generation
✔ Outgoing message sender

⚙️ Automation Layer

✔ n8n daily scheduler
✔ WhatsApp report automation

🧠 IMPORTANT NEXT STEP (HIGH VALUE)

If you want to make this real-world strong (interview + product grade) next upgrades are:

🔥 1. Intent classifier (VERY IMPORTANT)
distinguish stock query vs general chat
🔥 2. Portfolio tracking system
track recommendations over time
🔥 3. Backtesting module
prove if AI decisions work historically