from demo_app.models.domain import DiscountRules

COUPON_STACKING_RULE = DiscountRules.stacking

def coupons_may_stack(codes):
    return len(codes) <= 1
