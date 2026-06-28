import os
import requests


class WhatsAppService:
    def __init__(self, token=None, phone_number_id=None, api_version="v18.0"):
        self.token = token or os.getenv("WHATSAPP_TOKEN", "")
        self.phone_number_id = phone_number_id or os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
        self.api_version = api_version

    def send_message(self, to_number: str, message: str):
        if not self.token or not self.phone_number_id:
            return {"status": "skipped", "reason": "WhatsApp credentials not configured"}

        url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {"body": message},
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            return {"status": "error", "reason": str(exc)}
