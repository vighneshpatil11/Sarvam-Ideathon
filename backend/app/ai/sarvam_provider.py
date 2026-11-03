import os
import json
import urllib.request
import urllib.error
import logging
from typing import List, Dict, Any, Optional
from app.ai.base import BaseAIProvider
from app.config import settings

logger = logging.getLogger("saarthi.ai.sarvam")

class SarvamAIProvider(BaseAIProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = (api_key or settings.SARVAM_API_KEY or "").strip()
        if not self.api_key:
            raise ValueError("SARVAM_API_KEY not configured")
        self.model = settings.SARVAM_CHAT_MODEL or "sarvam-105b-conversations"
        self.endpoint = "https://api.sarvam.ai/v1/chat/completions"

    def get_provider_name(self) -> str:
        return "sarvam-105b-conversations"

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        language: str = "mr"
    ) -> str:
        chat_messages = []
        if system_prompt:
            chat_messages.append({"role": "system", "content": system_prompt})

        for msg in messages:
            chat_messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })

        payload = {
            "model": self.model,
            "messages": chat_messages,
            "temperature": 0.4,
            "max_tokens": 900
        }

        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.endpoint,
                data=req_data,
                headers={
                    "Content-Type": "application/json",
                    "api-subscription-key": self.api_key
                }
            )

            # Direct HTTP execution with timeout
            with urllib.request.urlopen(req, timeout=20) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
                choices = resp_json.get("choices", [])
                if choices and len(choices) > 0:
                    content = choices[0].get("message", {}).get("content", "")
                    if content:
                        return content.strip()
            
            return "माहिती उपलब्ध होऊ शकली नाही. कृपया पुन्हा प्रयत्न करा."

        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            logger.error(f"Sarvam AI HTTP Error {e.code}: {err_body}")
            raise RuntimeError(f"Sarvam API HTTP error {e.code}: {err_body}")
        except Exception as e:
            logger.error(f"Sarvam AI call error: {e}")
            raise RuntimeError(f"Sarvam API error: {str(e)}")
