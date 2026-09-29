from app.agent.context import AgentContext
from app.agent.tools import CommerceTools
from pydantic import ValidationError

from app.agent.tool_arguments import (
    SearchProductArguments,
    GetOrderArguments,
    CancelOrderArguments,
    RefundOrderArguments,
)

class ToolDispatcher:
    def __init__(self, tools: CommerceTools):
        self.tools = tools

    def dispatch(
        self,
        tool_name: str,
        arguments: dict,
        context: AgentContext,
    ) -> dict:
        try:
            if tool_name == "search_product":
                args = SearchProductArguments.model_validate(arguments)

                return self.tools.search_product(
                    query=args.query
                )

            if tool_name == "get_order":
                args = GetOrderArguments.model_validate(arguments)

                return self.tools.get_order(
                    order_id=args.order_id
                )

            if tool_name == "cancel_order":
                args = CancelOrderArguments.model_validate(arguments)

                return self.tools.cancel_order(
                    order_id=args.order_id,
                    context=context,
                )

            if tool_name == "refund_order":
                args = RefundOrderArguments.model_validate(arguments)

                return self.tools.refund_order(
                    order_id=args.order_id,
                    context=context,
                )

            return {
                "ok": False,
                "error": "unknown_tool",
                "message": f"Unknown tool: {tool_name}",
            }

        except ValidationError as exc:
            return {
                "ok": False,
                "error": "invalid_arguments",
                "message": "Tool arguments are invalid",
                "details": exc.errors(),
            }