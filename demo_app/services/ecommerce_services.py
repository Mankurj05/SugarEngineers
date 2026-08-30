"""
Enterprise Tax, Shipping, Inventory, Promotion, and Order Processing Services.
"""

from typing import Dict, List, Optional, Tuple
from demo_app.models.ecommerce_domain import (
    Cart, CartItem, CouponRule, DiscountType, Money, Order, OrderItem,
    OrderStatus, PaymentMethod, ProductCategory, PriceQuote, Product,
    ShippingAddress, ShippingOption, TaxCalculation
)


class TaxService:
    STATE_TAX_RATES = {
        "CA": 0.0825,
        "NY": 0.08875,
        "TX": 0.0625,
        "FL": 0.06,
        "WA": 0.065,
        "IL": 0.0625
    }

    def calculate_tax(self, amount: float, address: Optional[ShippingAddress]) -> TaxCalculation:
        if not address:
            return TaxCalculation(taxable_amount=amount, tax_rate=0.0, tax_amount=0.0, jurisdiction="DEFAULT")
        
        rate = self.STATE_TAX_RATES.get(address.state.upper(), 0.05)
        tax_amount = round(amount * rate, 2)
        return TaxCalculation(
            taxable_amount=amount,
            tax_rate=rate,
            tax_amount=tax_amount,
            jurisdiction=f"STATE_{address.state.upper()}"
        )


class ShippingService:
    DEFAULT_OPTIONS = [
        ShippingOption(id="std", name="Standard Ground Shipping", cost=5.99, estimated_days=5),
        ShippingOption(id="exp", name="Expedited Air Shipping", cost=14.99, estimated_days=2),
        ShippingOption(id="overnight", name="Overnight Express Shipping", cost=29.99, estimated_days=1)
    ]

    def get_available_options(self, cart: Cart) -> List[ShippingOption]:
        options = list(self.DEFAULT_OPTIONS)
        if cart.subtotal >= 100.0:
            options[0] = ShippingOption(id="std_free", name="Free Standard Shipping", cost=0.0, estimated_days=5)
        return options

    def calculate_shipping_cost(self, cart: Cart, option_id: Optional[str]) -> float:
        if cart.subtotal >= 100.0 and (not option_id or option_id in ["std", "std_free"]):
            return 0.0
            
        options = {opt.id: opt.cost for opt in self.get_available_options(cart)}
        if option_id in options:
            return options[option_id]
            
        return 5.99


class PromotionService:
    def __init__(self):
        self.coupons: Dict[str, CouponRule] = {
            "WELCOME10": CouponRule(
                code="WELCOME10",
                discount_type=DiscountType.PERCENTAGE,
                value=10.0,
                min_order_amount=20.0,
                stackable=False
            ),
            "SAVE20": CouponRule(
                code="SAVE20",
                discount_type=DiscountType.PERCENTAGE,
                value=20.0,
                min_order_amount=50.0,
                max_discount_amount=40.0,
                stackable=False
            ),
            "HOLIDAY20": CouponRule(
                code="HOLIDAY20",
                discount_type=DiscountType.FIXED_AMOUNT,
                value=20.0,
                min_order_amount=80.0,
                stackable=False
            ),
            "FREESHIP": CouponRule(
                code="FREESHIP",
                discount_type=DiscountType.FREE_SHIPPING,
                value=0.0,
                min_order_amount=30.0,
                stackable=True
            )
        }

    def evaluate_cart_promotions(self, cart: Cart) -> Tuple[float, List[str], List[str]]:
        applied = []
        warnings = []
        total_discount = 0.0

        categories = cart.item_categories

        for code in cart.applied_coupon_codes:
            coupon = self.coupons.get(code.upper())
            if not coupon:
                warnings.append(f"Coupon {code} is not valid")
                continue

            if not coupon.is_valid_for_cart(cart.subtotal, categories):
                warnings.append(f"Cart does not meet criteria for coupon {code}")
                continue

            discount = coupon.calculate_discount(cart.subtotal - total_discount)
            total_discount += discount
            applied.append(code.upper())

        return round(total_discount, 2), applied, warnings


class InventoryService:
    def __init__(self):
        self.stock_levels: Dict[str, int] = {
            "P-101": 150,
            "P-102": 45,
            "P-103": 12,
            "P-104": 200,
            "P-105": 0
        }

    def check_availability(self, product_id: str, requested_qty: int) -> bool:
        stock = self.stock_levels.get(product_id, 100)
        return stock >= requested_qty

    def reserve_stock(self, product_id: str, qty: int) -> bool:
        if self.check_availability(product_id, qty):
            self.stock_levels[product_id] -= qty
            return True
        return False
