from fastapi import APIRouter, Request

from integrations.whatsapp import WhatsAppService

router = APIRouter()


@router.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request):
    payload = await request.json()
    message = payload.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}).get("messages", [{}])[0].get("text", {}).get("body", "")

    service = WhatsAppService()
    result = service.send_message("", message)
    return {"status": "received", "message": message, "delivery": result}
