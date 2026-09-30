import json

from app.agent.context import AgentContext
from app.agent.dispatcher import ToolDispatcher
from app.agent.llm import CommerceLLM

MAX_STEPS = 5

class AgentRunner:
    def __init__(
        self,
        llm: CommerceLLM,
        dispatcher: ToolDispatcher,
        max_steps: int = MAX_STEPS,
    ):
        self.llm = llm
        self.dispatcher = dispatcher
        self.max_steps = max_steps

    def run(
        self,
        user_message: str,
        context: AgentContext,
    ) -> dict:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a commerce support agent. "
                    "Use tools when needed. "
                    "Do not invent order or product information."
                ),
            },
            {
                "role": "user",
                "content": user_message,
            },
        ]

        trace = []

        for step in range(self.max_steps):
            response = self.llm.complete(messages)

            message = response.choices[0].message

            # Không còn tool call -> final answer
            if not message.tool_calls:
                return {
                    "ok": True,
                    "final_answer": message.content,
                    "trace": trace,
                    "steps": step + 1,
                }

            # Lưu assistant tool call vào conversation
            messages.append(
                {
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments,
                            },
                        }
                        for tool_call in message.tool_calls
                    ],
                }
            )

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = None

                try:
                    arguments = json.loads(
                        tool_call.function.arguments
                    )
                except json.JSONDecodeError as exc:
                    tool_result = {
                        "ok": False,
                        "error": "invalid_json_arguments",
                        "message": str(exc),
                    }

                else:
                    tool_result = self.dispatcher.dispatch(
                        tool_name=tool_name,
                        arguments=arguments,
                        context=context,
                    )

                trace.append(
                    {
                        "step": step + 1,
                        "tool_name": tool_name,
                        "arguments": arguments,
                        "result": tool_result,
                        "reasoning": getattr(
                            message,
                            "reasoning",
                            None,
                        ),
                    }
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result),
                    }
                )

        return {
            "ok": False,
            "error": "max_steps_exceeded",
            "final_answer": None,
            "trace": trace,
            "steps": self.max_steps,
        }