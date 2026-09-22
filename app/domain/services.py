from app.domain.models import Order, OrderStatus, Product
from app.domain.exceptions import (
    OrderNotFoundError,
    InvalidOrderStateError
)
from app.repositories.memory import CommerceRepository

class CommerceService:
    def __init__(self, repository: CommerceRepository):
        self.repository = repository

    def search_products(self, query: str) -> list[Product]:
        return self.repository.search_products(query)

    def get_order(self, order_id: int) -> Order:
        order = self.repository.get_order(order_id)
        
        if order is None:
            raise OrderNotFoundError(f"Order {order_id} not found") 

        return order

    def cancel_order(self, order_id: int) -> Order:
        order = self.repository.get_order(order_id)

        if order is None:
            raise OrderNotFoundError(f"Order {order_id} not found")

        if (order.status != OrderStatus.PENDING):
            raise InvalidOrderStateError(
                f"Order {order_id} cannot be cancelled "
                f"because its status is '{order.status.value}'"
            )
        
        order.status = OrderStatus.CANCELLED

        self.repository.update_order(order)

        return order

    def refund_order(self, order_id: int) -> Order:
        order = self.repository.get_order(order_id)
        
        if order is None:
            raise OrderNotFoundError(f"Order {order_id} not found")

        if order.status != OrderStatus.PAID:
            raise InvalidOrderStateError(
                f"Order {order_id} cannot be refunded "
                f"because its status is '{order.status.value}'"
            )

        order.status = OrderStatus.REFUNDED

        self.repository.update_order(order)

        return order

    