import logging
from app.config import settings
from app.ai.base import BaseAIProvider
from app.ai.sarvam_provider import SarvamAIProvider
from app.ai.local_fallback import LocalFallbackProvider

logger = logging.getLogger("saarthi.ai")

def get_ai_provider() -> BaseAIProvider:
    if settings.SARVAM_API_KEY and settings.SARVAM_API_KEY.strip():
        try:
            return SarvamAIProvider(api_key=settings.SARVAM_API_KEY.strip())
        except Exception as e:
            logger.warning(f"Failed to initialize Sarvam AI provider: {e}. Falling back to deterministic local provider.")
            return LocalFallbackProvider()
    return LocalFallbackProvider()
