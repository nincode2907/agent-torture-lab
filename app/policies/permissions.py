from app.agent.context import AgentContext


class PermissionPolicy:
    def can_cancel_order(self, context: AgentContext) -> bool:
        return context.role in {
            "support",
            "admin",
        }

    def can_refund_order(self, context: AgentContext) -> bool:
        return context.role == "admin"