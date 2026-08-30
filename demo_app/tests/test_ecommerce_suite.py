"""
Comprehensive test suite covering domain models, tax calculations, cart management, checkout processing, fraud risk analysis, and pricing engines.
"""

import unittest
from demo_app.models.ecommerce_domain import (
    Cart, CartItem, Money, Currency, ProductCategory, ShippingAddress, DiscountType, OrderStatus, PaymentMethod
)
from demo_app.core.enterprise_pricing import EnterprisePricingEngine
from demo_app.services.ecommerce_services import TaxService, ShippingService, PromotionService
from demo_app.services.order_processing import EnterpriseCartManager, EnterpriseOrderProcessor
from demo_app.services.intelligence import FraudDetectionRiskEngine, InventoryFulfillmentService
from demo_app.repositories.catalog_repository import EnterpriseProductCatalog


class TestEcommerceDomainModels(unittest.TestCase):

    def test_money_addition_and_subtraction(self):
        m1 = Money(100.50, Currency.USD)
        m2 = Money(49.50, Currency.USD)
        res = m1.add(m2)
        self.assertEqual(res.amount, 150.00)
        
        diff = m1.subtract(m2)
        self.assertEqual(diff.amount, 51.00)

    def test_money_mismatched_currency_raises_error(self):
        m1 = Money(100.00, Currency.USD)
        m2 = Money(100.00, Currency.EUR)
        with self.assertRaises(ValueError):
            m1.add(m2)

    def test_cart_item_subtotal(self):
        item = CartItem(
            product_id="P-101",
            product_title="Test Laptop",
            category=ProductCategory.ELECTRONICS,
            unit_price=999.99,
            quantity=2
        )
        self.assertEqual(item.subtotal, 1999.98)


class TestEcommercePricingEngine(unittest.TestCase):

    def setUp(self):
        self.pricing_engine = EnterprisePricingEngine()
        self.cart_manager = EnterpriseCartManager()

    def test_full_price_quote_calculation(self):
        cart = self.cart_manager.get_or_create_cart("test_cart_01")
        self.cart_manager.add_to_cart("test_cart_01", "P-101", quantity=1)
        
        cart.shipping_address = ShippingAddress(
            street="123 Market St",
            city="San Francisco",
            state="CA",
            postal_code="94105",
            country="US"
        )
        
        quote = self.pricing_engine.compute_full_quote(cart)
        self.assertGreater(quote.subtotal, 0.0)
        self.assertGreater(quote.tax_amount, 0.0)
        self.assertGreater(quote.final_total, quote.subtotal)


class TestServicesAndRepositories(unittest.TestCase):

    def setUp(self):
        self.catalog = EnterpriseProductCatalog()
        self.tax_service = TaxService()
        self.shipping_service = ShippingService()
        self.fraud_engine = FraudDetectionRiskEngine()
        self.fulfillment = InventoryFulfillmentService()

    def test_catalog_search(self):
        products = self.catalog.search_products("Electronics")
        self.assertGreater(len(products), 0)

    def test_tax_calculation_by_state(self):
        addr_ca = ShippingAddress("1 St", "LA", "CA", "90001", "US")
        tax_ca = self.tax_service.calculate_tax(100.00, addr_ca)
        self.assertEqual(tax_ca.tax_amount, 8.25)

        addr_ny = ShippingAddress("1 St", "NYC", "NY", "10001", "US")
        tax_ny = self.tax_service.calculate_tax(100.00, addr_ny)
        self.assertEqual(tax_ny.tax_amount, 8.88)

    def test_warehouse_allocation(self):
        wh_ca = self.fulfillment.allocate_warehouse("CA")
        self.assertEqual(wh_ca, "WH-EAST-CA")
        
        wh_ny = self.fulfillment.allocate_warehouse("NY")
        self.assertEqual(wh_ny, "WH-WEST-NY")


class TestCheckoutProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = EnterpriseOrderProcessor()

    def test_successful_checkout_flow(self):
        cart_id = "checkout_cart_1"
        self.processor.cart_manager.add_to_cart(cart_id, "P-101", quantity=2)
        
        address = ShippingAddress("456 Broadway", "New York", "NY", "10012", "US")
        
        order = self.processor.checkout_cart(
            cart_id=cart_id,
            customer_id="cust_999",
            payment_method=PaymentMethod.CREDIT_CARD,
            shipping_address=address
        )
        
        self.assertEqual(order.status, OrderStatus.PAID)
        self.assertGreater(order.grand_total, 0.0)
        self.assertEqual(len(order.items), 1)


if __name__ == "__main__":
    unittest.main()
