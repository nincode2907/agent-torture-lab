import json
import os
import unittest
from unittest.mock import patch

import httpx
from openai import OpenAI, RateLimitError

from app.agent.llm import CommerceLLM


class CommerceLLMTests(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_local_tool_round_trip(self):
        requests = []

        def respond(request):
            requests.append(request)
            if len(requests) == 1:
                message = {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{
                        "id": "call_order",
                        "type": "function",
                        "function": {
                            "name": "get_order",
                            "arguments": '{"order_id":"ORD-1"}',
                        },
                    }],
                }
            else:
                message = {"role": "assistant", "content": "Order found."}
            return httpx.Response(200, json={
                "id": "chatcmpl-local-test",
                "object": "chat.completion",
                "created": 1,
                "model": "gpt-6.1-sol",
                "choices": [{"index": 0, "message": message,
                             "finish_reason": "tool_calls" if len(requests) == 1 else "stop"}],
            })

        with patch("app.agent.llm.OpenAI", wraps=OpenAI) as factory:
            llm = CommerceLLM()
        self.assertEqual(llm.provider, "local")
        options = factory.call_args.kwargs
        self.assertEqual(options["base_url"], "http://127.0.0.1:4000/v1")
        self.assertEqual(options["timeout"], 200)
        self.assertEqual(options["max_retries"], 0)
        llm.client.close()
        llm.client = OpenAI(**options, http_client=httpx.Client(
            transport=httpx.MockTransport(respond),
        ))
        self.addCleanup(llm.client.close)

        messages = [{"role": "user", "content": "Find ORD-1"}]
        message = llm.complete(messages).choices[0].message
        self.assertEqual(message.tool_calls[0].function.name, "get_order")
        messages.append(message.model_dump(exclude_none=True))
        messages.append({"role": "tool", "tool_call_id": "call_order",
                         "content": '{"ok":true}'})
        self.assertEqual(llm.complete(messages).choices[0].message.content, "Order found.")

        payload = json.loads(requests[0].content)
        self.assertEqual(requests[0].url.path, "/v1/chat/completions")
        self.assertEqual(requests[0].headers["authorization"], "Bearer local")
        self.assertEqual(payload["reasoning_effort"], "medium")
        self.assertEqual(payload["tool_choice"], "auto")
        self.assertEqual(payload["temperature"], 0)
        self.assertTrue(all("function" in tool for tool in payload["tools"]))
        self.assertEqual(json.loads(requests[1].content)["messages"][-1]["tool_call_id"], "call_order")

    @patch.dict(os.environ, {"LLM_PROVIDER": "local", "GROQ_MODEL": "custom-groq"}, clear=True)
    @patch("app.agent.llm.Groq")
    def test_explicit_groq_overrides_environment(self, groq):
        llm = CommerceLLM(provider="groq")
        messages = [{"role": "user", "content": "Hello"}]
        self.assertIs(llm.complete(messages), groq.return_value.chat.completions.create.return_value)
        payload = groq.return_value.chat.completions.create.call_args.kwargs
        self.assertEqual(payload["model"], "custom-groq")
        self.assertEqual(payload["messages"], messages)
        self.assertNotIn("reasoning_effort", payload)

    @patch.dict(os.environ, {
        "LLM_PROVIDER": "local", "LOCAL_BASE_URL": "http://localhost:4000/v1",
        "LOCAL_API_KEY": "gateway-token", "LOCAL_MODEL": "custom-local",
        "LOCAL_REASONING_EFFORT": "high",
    }, clear=True)
    def test_local_overrides_and_no_retry_on_rate_limit(self):
        attempts = []

        def reject(request):
            attempts.append(request)
            return httpx.Response(429, json={"error": {
                "message": "Busy", "type": "rate_limit_error", "code": "busy",
            }})

        with patch("app.agent.llm.OpenAI", wraps=OpenAI) as factory:
            llm = CommerceLLM()
        options = factory.call_args.kwargs
        llm.client.close()
        llm.client = OpenAI(**options, http_client=httpx.Client(
            transport=httpx.MockTransport(reject),
        ))
        self.addCleanup(llm.client.close)
        with self.assertRaises(RateLimitError):
            llm.complete([{"role": "user", "content": "Hello"}])
        self.assertEqual(len(attempts), 1)
        self.assertEqual(attempts[0].headers["authorization"], "Bearer gateway-token")
        payload = json.loads(attempts[0].content)
        self.assertEqual(payload["model"], "custom-local")
        self.assertEqual(payload["reasoning_effort"], "high")

    def test_unknown_provider_fails_clearly(self):
        with self.assertRaisesRegex(ValueError, "Use 'local' or 'groq'"):
            CommerceLLM(provider="unknown")


if __name__ == "__main__":
    unittest.main()
