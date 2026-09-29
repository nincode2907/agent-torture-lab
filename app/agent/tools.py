from app.domain.services import CommerceService
from app.domain.exceptions import OrderNotFoundError, InvalidOrderStateError
from app.policies.permissions import PermissionPolicy
from app.agent.context import AgentContext

class CommerceTools:
    def __init__(
        self, 
        service: CommerceService,
        permission_policy: PermissionPolicy
    ):
        self.service = service
        self.permission_policy = permission_policy

    def get_order(self, order_id: int) -> dict:
        try:
            print(order_id)
            order = self.service.get_order(order_id)

            return {
                "ok": True,
                "data": order.model_dump(mode="json"),
            }

        except OrderNotFoundError as exc:
            return {
                "ok": False,
                "error": "order_not_found",
                "message": str(exc),
            }

        except Exception as exc:
            return {
                "ok": False,
                "error": "internal_error",
                "message": str(exc),
            }

    def cancel_order(self, order_id: int, context: AgentContext) -> dict:
        try:
            if not self.permission_policy.can_cancel_order(context):
                return {
                    "ok": False,
                    "error": "permission_denied",
                    "message": "User does not have permission to cancel orders",
                }

            if not context.approved:
                return {
                    "ok": False,
                    "error": "approval_required",
                    "message": "Human approval is required before cancelling an order",
                }
            
            order = self.service.cancel_order(order_id)

            return {
                "ok": True,
                "data": order.model_dump(mode="json"),
            }

        except OrderNotFoundError as exc:
            return {
                "ok": False,
                "error": "order_not_found",
                "message": str(exc),
            }

        except InvalidOrderStateError as exc:
            return {
                "ok": False,
                "error": "invalid_order_state",
                "message": str(exc),
            }

        except Exception as exc:
            return {
                "ok": False,
                "error": "internal_error",
                "message": str(exc),
            }

    def refund_order(self, order_id: int, context: AgentContext) -> dict:
        try:
            if not self.permission_policy.can_refund_order(context):
                return {
                    "ok": False,
                    "error": "permission_denied",
                    "message": "User does not have permission to refund orders",
                }

            if not context.approved:
                return {
                    "ok": False,
                    "error": "approval_required",
                    "message": "Human approval is required before refunding an order",
                }
        
            order = self.service.refund_order(order_id)

            return {
                "ok": True,
                "data": order.model_dump(mode="json"),
            }

        except OrderNotFoundError as exc:
            return {
                "ok": False,
                "error": "order_not_found",
                "message": str(exc),
            }

        except InvalidOrderStateError as exc:
            return {
                "ok": False,
                "error": "invalid_order_state",
                "message": str(exc),
            }

        except Exception as exc:
            return {
                "ok": False,
                "error": "internal_error",
                "message": str(exc),
            }

    def search_product(self, query: str) -> dict:
        try:
            products = self.service.search_products(query)

            return {
                "ok": True,
                "data": [
                    product.model_dump(mode="json")
                    for product in products
                ]
            }

        except Exception as exc:
            return {
                "ok": False,
                "error": "internal_error",
                "message": str(exc),
            }