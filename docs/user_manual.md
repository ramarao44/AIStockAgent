# User Manual

This guide explains how to run AIStockAgent locally, test the API, trigger it from WhatsApp, and observe the workflow in n8n.

## 1. Prerequisites
Before you begin, make sure you have:
- Python 3.10+ installed
- A terminal with PowerShell
- Optional: n8n installed locally or in Docker
- Optional: a WhatsApp Business account and Meta Cloud API credentials
- Optional: ngrok for exposing your local server to the internet

## 2. Install and run locally
### Step 1: Create the virtual environment
```powershell
cd C:\path\to\AIStockAgent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 2: Install dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Run the CLI analysis
```powershell
python Python/main.py
```
You should see JSON output for the symbols from your watchlist.

### Step 4: Start the API server
```powershell
python -m uvicorn api.app:app --host 127.0.0.1 --port 8001
```

### Step 5: Test the API
Open another terminal and run:
```powershell
curl http://127.0.0.1:8001/health
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8001/analyze-stock" -ContentType "application/json" -Body '{"symbol":"RELIANCE.NS"}'
```
If the server is running, you should receive a JSON response.

## 3. Test the WhatsApp flow
### Step 1: Expose the local server
If you want WhatsApp to reach your local webhook, use a tunnel such as ngrok:
```powershell
ngrok http 8001
```
Copy the forwarded HTTPS URL, for example:
```text
https://abcd1234.ngrok-free.app
```

### Step 2: Configure your WhatsApp webhook
In the WhatsApp Cloud API configuration:
- Set the webhook callback URL to:
  ```text
  https://abcd1234.ngrok-free.app/whatsapp/webhook
  ```
- Use any verify token you prefer for testing
- Subscribe to the `messages` field

### Step 3: Send a test message
Send a message to your WhatsApp Business number.
The app will receive the webhook and return a JSON response from the webhook endpoint.

> Note: The current repository includes a starter webhook scaffold. For full production-style replies, wire the recipient number from the incoming webhook payload into the outbound message logic.

## 4. Test the n8n workflow
### Use the chat workflow in n8n
- Open n8n
- Create a new workflow
- Import the file from [n8n/workflow_simple.json](../n8n/workflow_simple.json)
- Activate the workflow
- Open the chat interface from the n8n UI and send a message like:
  - `RELIANCE.NS`
  - `TCS.NS`
  - `AAPL`

The workflow will call the local analysis API and return a simple AIStockAgent reply.

### Expected execution order
1. Chat Trigger
2. Parse Message
3. Call Stock API
4. Format Reply
5. Reply

## 5. Useful troubleshooting tips
- If the API does not start, confirm that all requirements are installed
- If the webhook does not receive traffic, confirm that ngrok is running and that the callback URL matches exactly
- If WhatsApp messages do not send, verify the token, phone number ID, and recipient number
- If n8n cannot reach the local API, replace `http://127.0.0.1:8001/analyze-stock` with the public URL of your tunnel

## 6. Run the automated tests
```powershell
pytest -q
```

That will verify the core analysis and API behavior.
