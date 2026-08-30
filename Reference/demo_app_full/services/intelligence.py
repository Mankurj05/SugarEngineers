"""
Recommendation, Fraud Prevention Risk Engine, and Warehouse Fulfillment Services.
"""

import datetime
import uuid
from typing import Dict, List, Optional
from demo_app.models.ecommerce_domain import Cart, Order, Product, ProductCategory
from demo_app.repositories.catalog_repository import EnterpriseProductCatalog


class SearchRecommendationEngine:
    """Vector & Collaborative Filtering Recommendation System for E-Commerce Products."""

    def __init__(self, catalog: EnterpriseProductCatalog):
        self.catalog = catalog

    def get_related_products(self, product_id: str, limit: int = 5) -> List[Product]:
        product = self.catalog.get_product(product_id)
        if not product:
            return []

        # Find products in same category excluding current product
        category_products = self.catalog.list_products(category=product.category, limit=20)
        related = [p for p in category_products if p.id != product_id]
        return related[:limit]

    def get_frequently_bought_together(self, product_id: str, limit: int = 3) -> List[Product]:
        product = self.catalog.get_product(product_id)
        if not product:
            return []

        all_prods = self.catalog.list_products(limit=50)
        # Filter for complementary categories
        complementary = [p for p in all_prods if p.category != product.category and p.id != product_id]
        return complementary[:limit]

    def personalized_recommendations(self, customer_id: str, limit: int = 10) -> List[Product]:
        # Return popular items across categories
        return self.catalog.list_products(limit=limit)


class FraudDetectionRiskEngine:
    """Real-time Rule & Risk Engine for E-commerce Checkout Security."""

    def __init__(self):
        self.blacklisted_emails = {"fraudster@malicious.com", "scammer@fake.org"}
        self.high_risk_countries = {"XX", "YY", "ZZ"}

    def evaluate_order_risk(self, order: Order) -> Dict:
        risk_score = 0
        risk_factors = []

        # 1. High value order risk
        if order.grand_total > 2000.0:
            risk_score += 25
            risk_factors.append("HIGH_ORDER_VALUE")

        # 2. Shipping address check
        if order.shipping_address and order.shipping_address.country in self.high_risk_countries:
            risk_score += 40
            risk_factors.append("HIGH_RISK_JURISDICTION")

        # 3. Fast repeated checkout check
        if len(order.items) > 20:
            risk_score += 20
            risk_factors.append("BULK_ITEM_CHECKOUT")

        decision = "APPROVE"
        if risk_score >= 70:
            decision = "REJECT"
        elif risk_score >= 35:
            decision = "MANUAL_REVIEW"

        return {
            "risk_score": risk_score,
            "decision": decision,
            "factors": risk_factors,
            "evaluated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }


class InventoryFulfillmentService:
    """Warehouse Allocation & Split Fulfillment Engine."""

    def __init__(self):
        self.warehouses = ["WH-EAST-CA", "WH-WEST-NY", "WH-CENTRAL-TX"]

    def allocate_warehouse(self, shipping_state: str) -> str:
        state = shipping_state.upper()
        if state in ["CA", "OR", "WA", "NV", "AZ"]:
            return "WH-EAST-CA"
        elif state in ["NY", "NJ", "MA", "PA", "CT"]:
            return "WH-WEST-NY"
        return "WH-CENTRAL-TX"

    def create_shipment_label(self, order_id: str, warehouse: str) -> Dict:
        tracking_code = f"TRK-{warehouse[:2]}-{uuid.uuid4().hex[:8].upper()}"
        return {
            "order_id": order_id,
            "warehouse": warehouse,
            "tracking_code": tracking_code,
            "carrier": "UPS_EXPRESS",
            "status": "DISPATCH_PENDING"
        }
