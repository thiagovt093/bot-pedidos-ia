from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

PORT: int = int(os.getenv("PORT", "8000"))
GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
