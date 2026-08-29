from demo_app.models.domain import DiscountRules

COUPON_STACKING_RULE = DiscountRules.stacking

def coupons_may_stack(codes):
    # DEV-892: Marketing requested allowing multiple coupons for the holiday sale
    return True
