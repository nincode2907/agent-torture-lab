from app.agent.tool_arguments import (
    SearchProductArguments,
    GetOrderArguments,
    CancelOrderArguments,
    RefundOrderArguments,
)

TOOL_DEFINITIONS = {
    "search_product": {
        "description": "Search products by product name.",
        "arguments_model": SearchProductArguments,
    },
    "get_order": {
        "description": "Get order information by order ID.",
        "arguments_model": GetOrderArguments,
    },
    "cancel_order": {
        "description": "Cancel a pending order.",
        "arguments_model": CancelOrderArguments,
    },
    "refund_order": {
        "description": "Refund a paid order.",
        "arguments_model": RefundOrderArguments,
    },
}

def get_tool_schemas() -> list[dict]:
    schemas = []

    for tool_name, definition in TOOL_DEFINITIONS.items():
        arguments_model = definition["arguments_model"]

        schemas.append({
            "name": tool_name,
            "description": definition["description"],
            "parameters": arguments_model.model_json_schema(),
        })

    return schemas

def get_openai_tools() -> list[dict]:
    return [
        {
            "type": "function",
            "name": schema["name"],
            "description": schema["description"],
            "parameters": schema["parameters"],
        }
        for schema in get_tool_schemas()
    ]

def get_groq_tools() -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": schema["name"],
                "description": schema["description"],
                "parameters": schema["parameters"],
            },
        }
        for schema in get_tool_schemas()
    ]