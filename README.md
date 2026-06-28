# AIStockAgent

AIStockAgent is a local-first stock analysis prototype that combines free market data, a lightweight decision engine, a FastAPI service, optional WhatsApp/webhook support, and an n8n workflow template.

## What it does
- Reads a local watchlist of stock symbols
- Pulls market data from Yahoo Finance
- Generates technical, fundamental, and decision outputs
- Exposes results through a simple REST API
- Provides starter files for WhatsApp and n8n automation

## Quick start

### 1) Create and activate the virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies
```powershell
pip install -r requirements.txt
```

### 3) Run the CLI analysis
```powershell
python Python/main.py
```

### 4) Start the API server
```powershell
python -m uvicorn api.app:app --host 127.0.0.1 --port 8000
```

### 5) Test the API
```powershell
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/analyze-stock -H "Content-Type: application/json" -d "{\"symbol\":\"RELIANCE.NS\"}"
```

## WhatsApp and n8n
For a full end-to-end test from WhatsApp and n8n, follow the step-by-step guide in [docs/user_manual.md](docs/user_manual.md).

## Project structure
- Python/ - analysis engine and services
- api/ - FastAPI endpoints
- n8n/ - importable workflow template
- tests/ - regression tests

## Verification
The current implementation has been tested locally with pytest:
```powershell
pytest -q
```
