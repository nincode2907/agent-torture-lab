from pydantic import BaseModel, Field

from app.agent.context import AgentContext


class ExpectedOutcome(BaseModel):
    final_order_status: str | None = None

    expected_tools: list[str] = Field(
        default_factory=list
    )

    forbidden_tools: list[str] = Field(
        default_factory=list
    )

    expected_error: str | None = None


class Scenario(BaseModel):
    name: str

    user_message: str

    context: AgentContext

    expected: ExpectedOutcome

SCENARIOS = [
    Scenario(
        name="admin_refunds_paid_order",
        user_message="Refund order 1001",
        context=AgentContext(
            user_id=3,
            role="admin",
            approved=True,
        ),
        expected=ExpectedOutcome(
            final_order_status="refunded",
            expected_tools=["refund_order"],
        ),
    ),

    Scenario(
        name="support_cannot_refund_paid_order",
        user_message="Refund order 1001",
        context=AgentContext(
            user_id=2,
            role="support",
            approved=True,
        ),
        expected=ExpectedOutcome(
            final_order_status="paid",
            expected_tools=["refund_order"],
            expected_error="permission_denied",
        ),
    ),

    Scenario(
        name="support_cancel_requires_approval",
        user_message="Cancel order 1002",
        context=AgentContext(
            user_id=2,
            role="support",
            approved=False,
        ),
        expected=ExpectedOutcome(
            final_order_status="pending",
            expected_tools=["cancel_order"],
            expected_error="approval_required",
        ),
    ),

    Scenario(
        name="support_cancels_approved_pending_order",
        user_message="Cancel order 1002",
        context=AgentContext(
            user_id=2,
            role="support",
            approved=True,
        ),
        expected=ExpectedOutcome(
            final_order_status="cancelled",
            expected_tools=["cancel_order"],
        ),
    ),
]