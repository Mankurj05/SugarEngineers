"""
Comprehensive catalog of 100 enterprise products across multiple categories for realistic e-commerce simulation.
"""

from typing import Dict, List
from demo_app.models.ecommerce_domain import Product, ProductCategory, ProductVariant


class EnterpriseProductCatalog:
    """In-memory repository storing a rich catalog of 100 enterprise products."""

    def __init__(self):
        self.catalog: Dict[str, Product] = {}
        self._seed_catalog()

    def _seed_catalog(self):
        categories = [
            ProductCategory.ELECTRONICS,
            ProductCategory.APPAREL,
            ProductCategory.HOME,
            ProductCategory.BEAUTY,
            ProductCategory.BOOKS,
            ProductCategory.SPORTS,
        ]

        # Generate 100 products dynamically to provide realistic data
        for i in range(1, 101):
            prod_id = f"P-{100+i}"
            category = categories[(i - 1) % len(categories)]
            base_price = round(10.0 + (i * 3.75), 2)
            
            title_prefixes = ["Pro", "Ultra", "Lite", "Eco", "Smart", "Elite", "Prime", "Compact", "Max", "Studio"]
            prefix = title_prefixes[(i - 1) % len(title_prefixes)]
            title = f"{prefix} {category.value.capitalize()} Product {i}"

            variants = [
                ProductVariant(
                    variant_id=f"{prod_id}-v1",
                    sku=f"SKU-{prod_id}-REG",
                    name="Standard Edition",
                    price=base_price,
                    weight_kg=0.5 + (i * 0.05),
                    inventory_count=100 + (i * 2)
                ),
                ProductVariant(
                    variant_id=f"{prod_id}-v2",
                    sku=f"SKU-{prod_id}-DELUXE",
                    name="Deluxe Edition",
                    price=round(base_price * 1.25, 2),
                    weight_kg=0.8 + (i * 0.05),
                    inventory_count=50 + i
                )
            ]

            p = Product(
                id=prod_id,
                sku=f"SKU-{prod_id}",
                title=title,
                category=category,
                base_price=base_price,
                description=f"High performance {category.value} item designed for enterprise usage.",
                variants=variants,
                tags=[category.value, prefix.lower(), "bestseller" if i % 5 == 0 else "standard"]
            )

            self.catalog[prod_id] = p

    def get_product(self, product_id: str) -> Optional[Product]:
        return self.catalog.get(product_id)

    def list_products(self, category: Optional[ProductCategory] = None, limit: int = 50) -> List[Product]:
        products = list(self.catalog.values())
        if category:
            products = [p for p in products if p.category == category]
        return products[:limit]

    def search_products(self, query: str) -> List[Product]:
        q = query.lower()
        return [
            p for p in self.catalog.values()
            if q in p.title.lower() or q in p.description.lower() or any(q in t for t in p.tags)
        ]
