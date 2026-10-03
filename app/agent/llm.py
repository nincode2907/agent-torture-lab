from __future__ import annotations

import os

from groq import Groq
from openai import OpenAI

from app.agent.tool_schemas import get_groq_tools

# Change to "groq" to use the external API again.
LLM_PROVIDER = "local"
LOCAL_BASE_URL = "http://127.0.0.1:4000/v1"
LOCAL_MODEL = "gpt-6.1-sol"
GROQ_MODEL = "openai/gpt-oss-120b"


class CommerceLLM:
    def __init__(self, provider: str | None = None):
        self.provider = provider or os.getenv("LLM_PROVIDER", LLM_PROVIDER)
        if self.provider == "local":
            self.client = OpenAI(
                base_url=os.getenv("LOCAL_BASE_URL", LOCAL_BASE_URL),
                api_key=os.getenv("LOCAL_API_KEY") or "local",
                timeout=200,
                max_retries=0,
            )
            self.model = os.getenv("LOCAL_MODEL", LOCAL_MODEL)
        elif self.provider == "groq":
            self.client = Groq()
            self.model = os.getenv("GROQ_MODEL", GROQ_MODEL)
        else:
            raise ValueError(
                f"Unsupported LLM provider: {self.provider!r}. Use 'local' or 'groq'."
            )

    def complete(self, messages: list[dict]):
        if self.provider == "local":
            return self.complete_local(messages)
        return self.complete_groq(messages)

    def complete_local(self, messages: list[dict]):
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=get_groq_tools(),
            tool_choice="auto",
            temperature=0,
            reasoning_effort=os.getenv("LOCAL_REASONING_EFFORT", "medium"),
        )

    def complete_groq(self, messages: list[dict]):
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=get_groq_tools(),
            tool_choice="auto",
            temperature=0,
        )
