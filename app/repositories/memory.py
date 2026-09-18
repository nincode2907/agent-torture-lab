from app.domain.models import Product, Order, OrderStatus

class CommerceRepository:
    def __init__(self):
        self.products: dict[int, Product] = {
            1: Product(
                id=1,
                name="Mechanical Keyboard",
                price="1200000",
                stock=10,
            ),
            2: Product(
                id=2,
                name="Gaming Mouse",
                price="800000",
                stock=20,
            ),
            3: Product(
                id=3,
                name="USB-C Hub",
                price="600000",
                stock=15,
            ),
        }

        self.orders: dict[int, Order] = {
            1001: Order(
                id=1001,
                product_id=1,
                quantity=1,
                status=OrderStatus.PAID,
                total="1200000",
            ),
            1002: Order(
                id=1002,
                product_id=2,
                quantity=2,
                status=OrderStatus.PENDING,
                total="1600000",
            ),
        }

    def get_product(self, product_id: int) -> Product | None:
        return self.products(product_id)

    def get_order(self, order_id: int) -> Order | None:
        return self.orders.get(order_id)

    def add_product(self, product: Product) -> None:
        self.products[product.id] = product

    def add_order(self, order: Order) -> None:
        self.orders[order.id] = order