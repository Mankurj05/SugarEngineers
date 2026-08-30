"""
Comprehensive e-commerce domain models for products, inventory, discounts, tax, shipping, cart, checkout, orders, and customer management.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Set, Union


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    INR = "INR"
    CAD = "CAD"


class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    APPAREL = "apparel"
    HOME = "home"
    BEAUTY = "beauty"
    BOOKS = "books"
    SPORTS = "sports"


class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"
    BUY_X_GET_Y = "buy_x_get_y"
    TIERED_AMOUNT = "tiered_amount"
    FREE_SHIPPING = "free_shipping"


class OrderStatus(str, Enum):
    PENDING = "pending"
    PAYMENT_PROCESSING = "payment_processing"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    APPLE_PAY = "apple_pay"
    BANK_TRANSFER = "bank_transfer"


@dataclass
class Money:
    amount: float
    currency: Currency = Currency.USD

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(round(self.amount + other.amount, 2), self.currency)

    def subtract(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot subtract {self.currency} and {other.currency}")
        return Money(round(max(0.0, self.amount - other.amount), 2), self.currency)

    def multiply(self, factor: float) -> "Money":
        return Money(round(self.amount * factor, 2), self.currency)


@dataclass
class ProductAttribute:
    name: str
    value: str


@dataclass
class ProductVariant:
    variant_id: str
    sku: str
    name: str
    price: float
    attributes: List[ProductAttribute] = field(default_factory=list)
    weight_kg: float = 0.5
    inventory_count: int = 100


@dataclass
class Product:
    id: str
    sku: str
    title: str
    category: ProductCategory
    base_price: float
    description: str = ""
    variants: List[ProductVariant] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    is_active: bool = True
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def get_price_for_variant(self, variant_id: Optional[str] = None) -> float:
        if not variant_id:
            return self.base_price
        for v in self.variants:
            if v.variant_id == variant_id:
                return v.price
        return self.base_price


@dataclass
class CouponRule:
    code: str
    discount_type: DiscountType
    value: float
    min_order_amount: float = 0.0
    max_discount_amount: Optional[float] = None
    applies_to_categories: List[ProductCategory] = field(default_factory=list)
    stackable: bool = False
    usage_limit: Optional[int] = None
    current_usage: int = 0
    expires_at: Optional[str] = None

    def is_valid_for_cart(self, cart_total: float, categories: List[ProductCategory]) -> bool:
        if cart_total < self.min_order_amount:
            return False
        if self.usage_limit is not None and self.current_usage >= self.usage_limit:
            return False
        if self.applies_to_categories:
            if not any(c in self.applies_to_categories for c in categories):
                return False
        return True

    def calculate_discount(self, eligible_amount: float) -> float:
        if self.discount_type == DiscountType.PERCENTAGE:
            discount = (eligible_amount * self.value) / 100.0
        elif self.discount_type == DiscountType.FIXED_AMOUNT:
            discount = min(self.value, eligible_amount)
        else:
            discount = 0.0

        if self.max_discount_amount is not None:
            discount = min(discount, self.max_discount_amount)
        return round(discount, 2)


@dataclass
class CartItem:
    product_id: str
    product_title: str
    category: ProductCategory
    unit_price: float
    quantity: int
    variant_id: Optional[str] = None
    selected_attributes: Dict[str, str] = field(default_factory=dict)

    @property
    def subtotal(self) -> float:
        return round(self.unit_price * self.quantity, 2)


@dataclass
class ShippingAddress:
    street: str
    city: str
    state: str
    postal_code: str
    country: str


@dataclass
class ShippingOption:
    id: str
    name: str
    cost: float
    estimated_days: int


@dataclass
class Cart:
    cart_id: str
    customer_id: Optional[str] = None
    items: List[CartItem] = field(default_factory=list)
    applied_coupon_codes: List[str] = field(default_factory=list)
    shipping_address: Optional[ShippingAddress] = None
    selected_shipping_option_id: Optional[str] = None

    def add_item(self, item: CartItem) -> None:
        for existing in self.items:
            if existing.product_id == item.product_id and existing.variant_id == item.variant_id:
                existing.quantity += item.quantity
                return
        self.items.append(item)

    def remove_item(self, product_id: str, variant_id: Optional[str] = None) -> None:
        self.items = [
            i for i in self.items
            if not (i.product_id == product_id and i.variant_id == variant_id)
        ]

    @property
    def subtotal(self) -> float:
        return round(sum(i.subtotal for i in self.items), 2)

    @property
    def total_quantity(self) -> int:
        return sum(i.quantity for i in self.items)

    @property
    def item_categories(self) -> List[ProductCategory]:
        return list(set(i.category for i in self.items))


@dataclass
class TaxCalculation:
    taxable_amount: float
    tax_rate: float
    tax_amount: float
    jurisdiction: str


@dataclass
class PriceQuote:
    cart_id: str
    subtotal: float
    item_discounts: float
    coupon_discounts: float
    total_discount: float
    tax_amount: float
    shipping_cost: float
    final_total: float
    applied_coupons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class OrderItem:
    product_id: str
    product_title: str
    unit_price: float
    quantity: int
    subtotal: float
    variant_id: Optional[str] = None


@dataclass
class Order:
    order_id: str
    cart_id: str
    customer_id: str
    items: List[OrderItem]
    subtotal: float
    discount_total: float
    tax_total: float
    shipping_total: float
    grand_total: float
    status: OrderStatus = OrderStatus.PENDING
    payment_method: PaymentMethod = PaymentMethod.CREDIT_CARD
    shipping_address: Optional[ShippingAddress] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class CustomerProfile:
    customer_id: str
    email: str
    first_name: str
    last_name: str
    vip_tier: str = "standard"
    total_spent: float = 0.0
    saved_addresses: List[ShippingAddress] = field(default_factory=list)
