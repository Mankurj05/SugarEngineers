from backend.models.domain import PricingService, calculate_subtotal, calculate_final_total

pricing_service = PricingService()
def calculate_order_total(customer_id, items, coupon_codes): return pricing_service.calculate_order_total(customer_id, items, coupon_codes)
