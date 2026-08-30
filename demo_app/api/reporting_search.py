"""
Executive Analytics Reporting Controllers and Advanced Faceted Search Engines.
"""

import datetime
from typing import Dict, List, Optional
from demo_app.models.ecommerce_domain import Currency, OrderStatus, ProductCategory
from demo_app.services.order_processing import EnterpriseOrderProcessor
from demo_app.repositories.catalog_repository import EnterpriseProductCatalog


class EnterpriseReportingAnalyticsController:
    """Executive Dashboard Reporting for GMV, Margin, Churn, Tax, and Inventory Turnover."""

    def __init__(self, order_processor: EnterpriseOrderProcessor):
        self.processor = order_processor

    def generate_sales_summary_report(self, start_date: str, end_date: str) -> Dict:
        orders = list(self.processor.orders.values())
        gmv = sum(o.grand_total for o in orders)
        net_revenue = sum(o.subtotal - o.discount_total for o in orders)
        total_tax = sum(o.tax_total for o in orders)
        total_shipping = sum(o.shipping_total for o in orders)

        return {
            "report_type": "EXECUTIVE_SALES_SUMMARY",
            "start_date": start_date,
            "end_date": end_date,
            "total_orders": len(orders),
            "gmv": round(gmv, 2),
            "net_revenue": round(net_revenue, 2),
            "total_tax_collected": round(total_tax, 2),
            "total_shipping_revenue": round(total_shipping, 2),
            "currency": Currency.USD.value,
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

    def generate_inventory_valuation_report(self, catalog: EnterpriseProductCatalog) -> Dict:
        products = catalog.list_products(limit=100)
        total_skus = len(products)
        total_valuation = sum(p.base_price * 100 for p in products)

        return {
            "report_type": "INVENTORY_VALUATION",
            "total_skus": total_skus,
            "total_valuation": round(total_valuation, 2),
            "currency": Currency.USD.value,
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }


class AdvancedCatalogSearchController:
    """Faceted Search, Dynamic Filters, and Product Indexing Controller."""

    def __init__(self, catalog: EnterpriseProductCatalog):
        self.catalog = catalog

    def faceted_search(
        self,
        query: Optional[str] = None,
        category: Optional[ProductCategory] = None,
        min_price: float = 0.0,
        max_price: float = 10000.0,
        tags: Optional[List[str]] = None
    ) -> List[Dict]:
        products = self.catalog.list_products(category=category, limit=100)
        filtered = []

        for p in products:
            if p.base_price < min_price or p.base_price > max_price:
                continue
            if query and query.lower() not in p.title.lower() and query.lower() not in p.description.lower():
                continue
            if tags and not any(t in p.tags for t in tags):
                continue

            filtered.append({
                "id": p.id,
                "sku": p.sku,
                "title": p.title,
                "category": p.category.value,
                "price": p.base_price,
                "tags": p.tags
            })

        return filtered
