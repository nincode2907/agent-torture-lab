TOOL_SCHEMAS = [
    {
        "name" : "search_product",
        "description": "Search products by product name.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Product name or partial product name",
                }
            }
        },
        "required": ["query"],
        "additionalProperties": False,
    },
    {
        "name": "get_order",
        "description": "Get order information by order ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "integer",
                    "description": "Order ID",
                }
            },
            "required": ["order_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "cancel_order",
        "description": "Cancel a pending order.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "integer",
                    "description": "Order ID to cancel",
                }
            },
            "required": ["order_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "refund_order",
        "description": "Refund a paid order.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "integer",
                    "description": "Order ID to refund",
                }
            },
            "required": ["order_id"],
            "additionalProperties": False,
        },
    },
]