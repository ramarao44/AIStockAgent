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
python -m uvicorn api.app:app --host 127.0.0.1 --port 8000
```

### Step 5: Test the API
Open another terminal and run:
```powershell
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/analyze-stock -H "Content-Type: application/json" -d "{\"symbol\":\"RELIANCE.NS\"}"
```
If the server is running, you should receive a JSON response.

## 3. Test the WhatsApp flow
### Step 1: Expose the local server
If you want WhatsApp to reach your local webhook, use a tunnel such as ngrok:
```powershell
ngrok http 8000
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
### Step 1: Import the workflow
- Open n8n
- Create a new workflow
- Import the file from [n8n/workflow.json](../n8n/workflow.json)

### Step 2: Update the placeholders
The workflow contains placeholder values for:
- `YOUR_PHONE_NUMBER_ID`
- `YOUR_WHATSAPP_TOKEN`
- `YOUR_PHONE_NUMBER`

Replace them with your actual WhatsApp Cloud API values.

### Step 3: Run the workflow
You can either:
- run the workflow manually from the n8n UI, or
- wait for the cron trigger to fire

### Step 4: Watch the execution
In n8n you should see the nodes execute in this order:
1. Cron
2. Call FastAPI
3. Format Message
4. Send WhatsApp

If the workflow is successful, the message will be sent to your WhatsApp number.

## 5. Useful troubleshooting tips
- If the API does not start, confirm that all requirements are installed
- If the webhook does not receive traffic, confirm that ngrok is running and that the callback URL matches exactly
- If WhatsApp messages do not send, verify the token, phone number ID, and recipient number
- If n8n cannot reach the local API, replace `http://127.0.0.1:8000/analyze-stock` with the public URL of your tunnel

## 6. Run the automated tests
```powershell
pytest -q
```

That will verify the core analysis and API behavior.
