"""
Subscription Billing, Multi-Region Warehouse Distribution, and Customer Loyalty Engines.
"""

import datetime
import uuid
from typing import Dict, List, Optional
from demo_app.models.ecommerce_domain import Cart, Order, OrderStatus, Product, ProductCategory
from demo_app.repositories.catalog_repository import EnterpriseProductCatalog


class SubscriptionBillingEngine:
    """Recurring Subscription & Auto-Renewal Engine for SaaS & Physical Subscriptions."""

    def __init__(self):
        self.subscriptions: Dict[str, Dict] = {}

    def create_subscription(self, customer_id: str, plan_id: str, billing_interval_days: int = 30) -> Dict:
        sub_id = f"sub_{uuid.uuid4().hex[:10]}"
        now = datetime.datetime.now(datetime.timezone.utc)
        next_billing = now + datetime.timedelta(days=billing_interval_days)

        sub = {
            "subscription_id": sub_id,
            "customer_id": customer_id,
            "plan_id": plan_id,
            "status": "ACTIVE",
            "billing_interval_days": billing_interval_days,
            "created_at": now.isoformat(),
            "next_billing_at": next_billing.isoformat(),
            "failed_attempts": 0
        }
        self.subscriptions[sub_id] = sub
        return sub

    def process_recurring_renewal(self, subscription_id: str) -> Dict:
        sub = self.subscriptions.get(subscription_id)
        if not sub or sub["status"] != "ACTIVE":
            raise ValueError("Subscription not active")

        # Simulate renewal billing
        now = datetime.datetime.now(datetime.timezone.utc)
        sub["last_billed_at"] = now.isoformat()
        sub["next_billing_at"] = (now + datetime.timedelta(days=sub["billing_interval_days"])).isoformat()
        return sub


class InventoryWarehouseDistributionEngine:
    """Multi-region warehouse load balancing and reorder point inventory forecasting."""

    def __init__(self, catalog: EnterpriseProductCatalog):
        self.catalog = catalog
        self.reorder_thresholds: Dict[str, int] = {}
        self.warehouse_stocks: Dict[str, Dict[str, int]] = {
            "WH-EAST": {},
            "WH-WEST": {},
            "WH-CENTRAL": {}
        }
        self._initialize_stock_distribution()

    def _initialize_stock_distribution(self):
        products = self.catalog.list_products(limit=100)
        for p in products:
            self.reorder_thresholds[p.id] = 20
            self.warehouse_stocks["WH-EAST"][p.id] = 100
            self.warehouse_stocks["WH-WEST"][p.id] = 100
            self.warehouse_stocks["WH-CENTRAL"][p.id] = 100

    def check_reorder_status(self, product_id: str) -> Dict:
        total_stock = sum(wh.get(product_id, 0) for wh in self.warehouse_stocks.values())
        threshold = self.reorder_thresholds.get(product_id, 20)
        return {
            "product_id": product_id,
            "total_stock": total_stock,
            "reorder_threshold": threshold,
            "needs_reorder": total_stock <= threshold
        }


class CustomerLoyaltyRewardsEngine:
    """Points-based loyalty, tier rewards, and referral cashback calculation engine."""

    def __init__(self):
        self.member_points: Dict[str, int] = {}

    def award_points_for_order(self, customer_id: str, order_amount: float) -> int:
        points_earned = int(order_amount * 10)  # 10 points per dollar
        current = self.member_points.get(customer_id, 0)
        self.member_points[customer_id] = current + points_earned
        return points_earned

    def redeem_points(self, customer_id: str, points_to_redeem: int) -> float:
        current = self.member_points.get(customer_id, 0)
        if current < points_to_redeem:
            raise ValueError("Insufficient points balance")

        self.member_points[customer_id] = current - points_to_redeem
        cash_value = round(points_to_redeem / 100.0, 2)  # 100 points = $1.00
        return cash_value
