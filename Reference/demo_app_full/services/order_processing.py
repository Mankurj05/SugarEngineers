"""
Cart and Order Services orchestrating Checkout, Payment, Ledger, and Notifications.
"""

import datetime
import uuid
from typing import Dict, List, Optional
from demo_app.models.ecommerce_domain import (
    Cart, CartItem, Order, OrderItem, OrderStatus, PaymentMethod, ProductCategory, ShippingAddress
)
from demo_app.core.enterprise_pricing import EnterprisePricingEngine
from demo_app.repositories.catalog_repository import EnterpriseProductCatalog
from demo_app.services.integrations import (
    CustomerAnalyticsEngine, EnterpriseLedgerService, NotificationDispatchService, PaymentGatewayAdapter
)


class EnterpriseCartManager:
    """Session-based Cart Management Engine supporting guest & authenticated users."""

    def __init__(self):
        self.carts: Dict[str, Cart] = {}
        self.catalog = EnterpriseProductCatalog()

    def get_or_create_cart(self, cart_id: Optional[str] = None, customer_id: Optional[str] = None) -> Cart:
        if cart_id and cart_id in self.carts:
            cart = self.carts[cart_id]
            if customer_id and not cart.customer_id:
                cart.customer_id = customer_id
            return cart

        new_id = cart_id or f"cart_{uuid.uuid4().hex[:10]}"
        cart = Cart(cart_id=new_id, customer_id=customer_id)
        self.carts[new_id] = cart
        return cart

    def add_to_cart(self, cart_id: str, product_id: str, quantity: int = 1, variant_id: Optional[str] = None) -> Cart:
        cart = self.get_or_create_cart(cart_id)
        product = self.catalog.get_product(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found in catalog")

        price = product.get_price_for_variant(variant_id)
        item = CartItem(
            product_id=product.id,
            product_title=product.title,
            category=product.category,
            unit_price=price,
            quantity=quantity,
            variant_id=variant_id
        )
        cart.add_item(item)
        return cart

    def apply_coupon(self, cart_id: str, coupon_code: str) -> Cart:
        cart = self.get_or_create_cart(cart_id)
        if coupon_code.upper() not in cart.applied_coupon_codes:
            cart.applied_coupon_codes.append(coupon_code.upper())
        return cart

    def clear_cart(self, cart_id: str) -> bool:
        if cart_id in self.carts:
            del self.carts[cart_id]
            return True
        return False


class EnterpriseOrderProcessor:
    """Full-lifecycle Order Processor with Ledger, Payment, Analytics, and Dispatch Integration."""

    def __init__(self):
        self.cart_manager = EnterpriseCartManager()
        self.pricing_engine = EnterprisePricingEngine()
        self.payment_gateway = PaymentGatewayAdapter()
        self.ledger = EnterpriseLedgerService()
        self.analytics = CustomerAnalyticsEngine()
        self.notifications = NotificationDispatchService()
        self.orders: Dict[str, Order] = {}

    def checkout_cart(self, cart_id: str, customer_id: str, payment_method: PaymentMethod, shipping_address: ShippingAddress, card_token: str = "tok_visa") -> Order:
        cart = self.cart_manager.get_or_create_cart(cart_id, customer_id)
        if not cart.items:
            raise ValueError("Cannot checkout an empty cart")

        cart.shipping_address = shipping_address
        quote = self.pricing_engine.compute_full_quote(cart)

        # 1. Authorize Payment
        tx_res = self.payment_gateway.authorize_payment(
            amount=quote.final_total,
            currency="USD",
            card_token=card_token
        )

        if tx_res["status"] != "authorized":
            raise ValueError("Payment authorization failed")

        # 2. Capture Payment
        self.payment_gateway.capture_payment(tx_res["transaction_id"], quote.final_total)

        # 3. Create Order
        order_id = f"ord_{uuid.uuid4().hex[:10]}"
        order_items = [
            OrderItem(
                product_id=i.product_id,
                product_title=i.product_title,
                unit_price=i.unit_price,
                quantity=i.quantity,
                subtotal=i.subtotal,
                variant_id=i.variant_id
            )
            for i in cart.items
        ]

        order = Order(
            order_id=order_id,
            cart_id=cart.cart_id,
            customer_id=customer_id,
            items=order_items,
            subtotal=quote.subtotal,
            discount_total=quote.total_discount,
            tax_total=quote.tax_amount,
            shipping_total=quote.shipping_cost,
            grand_total=quote.final_total,
            status=OrderStatus.PAID,
            payment_method=payment_method,
            shipping_address=shipping_address
        )

        self.orders[order_id] = order

        # 4. Record Ledger Entry
        self.ledger.record_entry("REVENUE", "CREDIT", quote.final_total, order_id, {"customer_id": customer_id})

        # 5. Track Analytics
        self.analytics.track_order(customer_id, quote.final_total)

        # 6. Send Notification
        self.notifications.send_order_confirmation(f"customer_{customer_id}@example.com", order_id, quote.final_total)

        # 7. Clear Cart
        self.cart_manager.clear_cart(cart_id)

        return order

    def get_order(self, order_id: str) -> Optional[Order]:
        return self.orders.get(order_id)
