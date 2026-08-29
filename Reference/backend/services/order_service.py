from backend.models.domain import OrderService

order_service = OrderService()
def create_order(request): return order_service.create(request)
def get_order(order_id): return order_service.get(order_id)
