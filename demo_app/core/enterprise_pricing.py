"""
Comprehensive enterprise pricing engine with multi-currency, tier discounting, bundle pricing, and promotional logic.
"""

from typing import Dict, List, Optional
from demo_app.models.ecommerce_domain import (
    Cart, CartItem, Currency, DiscountType, Money, PriceQuote, ProductCategory, Product
)
from demo_app.services.ecommerce_services import PromotionService, ShippingService, TaxService


class EnterprisePricingEngine:
    def __init__(self):
        self.tax_service = TaxService()
        self.shipping_service = ShippingService()
        self.promo_service = PromotionService()

    def calculate_item_tier_discount(self, item: CartItem) -> float:
        if item.quantity >= 10:
            return round(item.subtotal * 0.15, 2)
        elif item.quantity >= 5:
            return round(item.subtotal * 0.08, 2)
        elif item.quantity >= 3:
            return round(item.subtotal * 0.03, 2)
        return 0.0

    def calculate_bundle_discount(self, cart: Cart) -> float:
        categories = cart.item_categories
        if ProductCategory.ELECTRONICS in categories and ProductCategory.BOOKS in categories:
            return round(cart.subtotal * 0.05, 2)
        return 0.0

    def compute_full_quote(self, cart: Cart) -> PriceQuote:
        subtotal = cart.subtotal
        
        item_discounts = sum(self.calculate_item_tier_discount(i) for i in cart.items)
        bundle_discount = self.calculate_bundle_discount(cart)
        base_discounts = item_discounts + bundle_discount
        
        eligible_for_coupon = max(0.0, subtotal - base_discounts)
        coupon_discount, applied_coupons, warnings = self.promo_service.evaluate_cart_promotions(cart)
        
        total_discount = round(base_discounts + coupon_discount, 2)
        discounted_subtotal = max(0.0, subtotal - total_discount)
        
        tax_calc = self.tax_service.calculate_tax(discounted_subtotal, cart.shipping_address)
        tax_amount = tax_calc.tax_amount
        
        shipping_cost = self.shipping_service.calculate_shipping_cost(cart, cart.selected_shipping_option_id)
        
        final_total = round(discounted_subtotal + tax_amount + shipping_cost, 2)

        return PriceQuote(
            cart_id=cart.cart_id,
            subtotal=subtotal,
            item_discounts=round(item_discounts, 2),
            coupon_discounts=round(coupon_discount, 2),
            total_discount=total_discount,
            tax_amount=tax_amount,
            shipping_cost=shipping_cost,
            final_total=final_total,
            applied_coupons=applied_coupons,
            warnings=warnings
        )
