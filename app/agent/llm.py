from groq import Groq

from app.agent.tool_schemas import get_groq_tools

class CommerceLLM:
    def __init__(self):
        self.client = Groq()

    def complete(self, messages: list[dict]):
        return self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=get_groq_tools(),
            tool_choice="auto",
            temperature=0,
        )
