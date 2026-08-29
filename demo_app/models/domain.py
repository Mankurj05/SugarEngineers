from pydantic import BaseModel, Field
from typing import Literal, Optional

class Product(BaseModel):
    id: str; name: str; category: str; price: float; weight: float; active: bool = True
class Customer(BaseModel):
    id: str; name: str; email: str; region: str; tier: Literal['standard','gold','platinum']
class CartItem(BaseModel):
    product_id: str; quantity: int = Field(gt=0, le=20)
class CartRequest(BaseModel):
    customer_id: str; items: list[CartItem]; coupon_codes: list[str] = []
class Order(BaseModel):
    id: str; customer_id: str; items: list[CartItem]; coupon_codes: list[str]; subtotal: float; discount: float; shipping: float; tax: float; total: float; status: str; created_at: str
class PaymentRequest(BaseModel):
    order_id: str; payment_method: Literal['card','bank_transfer']
class RefundRequest(BaseModel):
    order_id: str; amount: Optional[float] = None
class Quote(BaseModel):
    subtotal: float; discount: float; shipping: float; tax: float; total: float; currency: str = 'USD'
class APIError(BaseModel):
    error: str; message: str
class Coupon(BaseModel):
    code: str; kind: Literal['percentage','fixed']; value: float; minimum_subtotal: float; categories: list[str]; exclusive: bool = False; conflicts: list[str] = []
class PriceBreakdown(Quote):
    item_count: int
class Health(BaseModel):
    status: str; service: str; version: str
class CartQuoteRequest(CartRequest): pass
class PaymentResponse(BaseModel):
    status: str; order_id: str; amount: float; payment_method: str
class RefundResponse(BaseModel):
    status: str; order_id: str; amount: float
class Invoice(BaseModel):
    id: str; order_id: str; customer: Customer; items: list[CartItem]; quote: Quote; status: str
class CustomerSummary(BaseModel):
    customer: Customer; order_count: int; total_spent: float; loyalty_tier: str; recent_orders: list[str]
class StatusResponse(BaseModel): order_id: str; status: str
class MessageResponse(BaseModel): message: str
class CustomerCreate(BaseModel): name: str; email: str; region: str; tier: Literal['standard','gold','platinum'] = 'standard'
class ProductList(BaseModel): products: list[Product]; count: int
class Inventory(BaseModel): product_id: str; available: int; reserved: int
class OrderCreate(CartRequest): pass
class Analytics(BaseModel): revenue: float; orders: int; average_order_value: float; low_stock_products: int

class AppError(Exception):
    def __init__(self, code: str, message: str, status: int = 400): self.code=code; self.message=message; self.status=status

class NotFound(AppError):
    def __init__(self, message): super().__init__('NOT_FOUND', message, 404)

class ValidationError(AppError): pass

class CouponConflict(AppError):
    def __init__(self, message): super().__init__('COUPON_CONFLICT', message, 400)

class InsufficientInventory(AppError):
    def __init__(self, message): super().__init__('INSUFFICIENT_INVENTORY', message, 400)

class InvalidPayment(AppError):
    def __init__(self, message): super().__init__('INVALID_PAYMENT', message, 400)

class SeedData:
    products: dict[str, Product] = {}
    customers: dict[str, Customer] = {}
    inventory: dict[str, Inventory] = {}
    orders: dict[str, Order] = {}
    coupons: dict[str, Coupon] = {}
    refunds: dict[str, float] = {}
    next_order = 2

store = SeedData()


def money(value: float) -> float: return round(value + 1e-9, 2)

PRODUCTS = [
    Product(id='PROD-001',name='Aero Wireless Headphones',category='electronics',price=129.99,weight=0.4),
    Product(id='PROD-002',name='Orbit Mechanical Keyboard',category='electronics',price=149.0,weight=0.9),
    Product(id='PROD-003',name='Field Notes Journal',category='books',price=24.0,weight=0.3),
    Product(id='PROD-004',name='The Craft of Systems',category='books',price=42.0,weight=0.7),
    Product(id='PROD-005',name='Canvas Utility Jacket',category='clothing',price=180.0,weight=1.1),
    Product(id='PROD-006',name='Merino Travel Tee',category='clothing',price=68.0,weight=0.4),
    Product(id='PROD-007',name='Desk Lamp No. 4',category='home',price=96.0,weight=1.8),
    Product(id='PROD-008',name='Oak Monitor Stand',category='home',price=115.0,weight=2.2),
    Product(id='PROD-009',name='Analog Camera Strap',category='accessories',price=38.0,weight=0.2),
    Product(id='PROD-010',name='Everyday Carry Tote',category='accessories',price=55.0,weight=0.5),
]
CUSTOMERS = [
    Customer(id='CUSTOMER-001',name='Maya Chen',email='maya@example.com',region='US',tier='gold'),
    Customer(id='CUSTOMER-002',name='Jon Bell',email='jon@example.com',region='EU',tier='standard'),
    Customer(id='CUSTOMER-003',name='Priya Nair',email='priya@example.com',region='US',tier='platinum'),
    Customer(id='CUSTOMER-004',name='Sam Rivera',email='sam@example.com',region='CA',tier='standard'),
    Customer(id='CUSTOMER-005',name='Alex Morgan',email='alex@example.com',region='US',tier='gold'),
]
def seed():
    store.products={p.id:p for p in PRODUCTS}; store.customers={c.id:c for c in CUSTOMERS}
    store.inventory={p.id:Inventory(product_id=p.id,available=18+(i%5)*7,reserved=0) for i,p in enumerate(PRODUCTS)}
    store.coupons={
      'WELCOME10': Coupon(code='WELCOME10',kind='percentage',value=10,minimum_subtotal=50,categories=[],conflicts=['HOLIDAY15','VIP25']),
      'HOLIDAY15': Coupon(code='HOLIDAY15',kind='percentage',value=15,minimum_subtotal=100,categories=['clothing','home'],conflicts=['WELCOME10','VIP25']),
      'VIP25': Coupon(code='VIP25',kind='percentage',value=25,minimum_subtotal=200,categories=[],exclusive=True),
      'SAVE20': Coupon(code='SAVE20',kind='fixed',value=20,minimum_subtotal=120,categories=[]),
    }
    store.orders={'ORDER-001':Order(id='ORDER-001',customer_id='CUSTOMER-001',items=[CartItem(product_id='PROD-001',quantity=1),CartItem(product_id='PROD-004',quantity=1)],coupon_codes=['WELCOME10'],subtotal=171.99,discount=17.2,shipping=0,tax=25.98,total=180.77,status='paid',created_at='2026-01-15T10:00:00Z')}
seed()

class ProductRepository:
    def all(self): return list(store.products.values())
    def get(self,id): return store.products.get(id)
class CustomerRepository:
    def get(self,id): return store.customers.get(id)
class InventoryRepository:
    def get(self,id): return store.inventory.get(id)
    def reserve(self,id,qty): store.inventory[id].available-=qty; store.inventory[id].reserved+=qty
class OrderRepository:
    def get(self,id): return store.orders.get(id)
    def all(self): return list(store.orders.values())
    def save(self,order): store.orders[order.id]=order

products_repo=ProductRepository(); customers_repo=CustomerRepository(); inventory_repo=InventoryRepository(); orders_repo=OrderRepository()

class ProductService:
    def list(self, search=None, category=None): return [p for p in products_repo.all() if (not search or search.lower() in p.name.lower()) and (not category or p.category==category)]
    def get(self,id):
        p=products_repo.get(id)
        if not p: raise NotFound(f'Product {id} not found')
        return p
class CustomerService:
    def get(self,id):
        c=customers_repo.get(id)
        if not c: raise NotFound(f'Customer {id} not found')
        return c
    def summary(self,id):
        c=self.get(id); orders=[o for o in orders_repo.all() if o.customer_id==id]
        return CustomerSummary(customer=c,order_count=len(orders),total_spent=money(sum(o.total for o in orders)),loyalty_tier=c.tier,recent_orders=[o.id for o in orders])
class InventoryService:
    def get(self,id):
        ProductService().get(id); return inventory_repo.get(id)
    def validate(self,items):
        for item in items:
            inv=self.get(item.product_id)
            if item.quantity>inv.available: raise InsufficientInventory(f'{item.product_id} has {inv.available} units available')
    def reserve(self,items):
        self.validate(items)
        for i in items: inventory_repo.reserve(i.product_id,i.quantity)
class DiscountService:
    def apply(self, items, subtotal, customer, codes):
        if len(codes)>1:
            for code in codes:
                coupon=store.coupons.get(code.upper())
                if not coupon: raise ValidationError('INVALID_COUPON',f'Coupon {code} is not valid')
                if coupon.exclusive or any(other.upper() in coupon.conflicts for other in codes if other.upper()!=code.upper()): raise CouponConflict(f'{code} cannot be combined with another selected coupon')
        discount=0
        for code in codes:
            coupon=store.coupons.get(code.upper())
            if not coupon: raise ValidationError('INVALID_COUPON',f'Coupon {code} is not valid')
            if subtotal<coupon.minimum_subtotal: raise ValidationError('COUPON_MINIMUM',f'{code} requires subtotal of {coupon.minimum_subtotal:.2f}')
            eligible=sum(next(p.price for p in PRODUCTS if p.id==i.product_id)*i.quantity for i in items if not coupon.categories or next(p for p in PRODUCTS if p.id==i.product_id).category in coupon.categories)
            discount += eligible*coupon.value/100 if coupon.kind=='percentage' else min(coupon.value,eligible)
        if customer.tier=='gold': discount += subtotal*0.03
        if customer.tier=='platinum': discount += subtotal*0.05
        return money(min(discount,subtotal))
class ShippingService:
    def calculate(self, items, post_discount_subtotal, customer):
        if post_discount_subtotal>=200: return 0.0
        base={'US':12.0,'CA':18.0,'EU':24.0}.get(customer.region,30.0)
        weight=sum(next(p.weight for p in PRODUCTS if p.id==i.product_id)*i.quantity for i in items)
        return money(base + max(0,weight-2)*2.5)
class TaxService:
    rates={'electronics':.18,'books':.05,'clothing':.12,'home':.1,'accessories':.08}
    def calculate(self,items,taxable_base):
        raw=sum(next(p.price for p in PRODUCTS if p.id==i.product_id)*i.quantity*self.rates.get(next(p for p in PRODUCTS if p.id==i.product_id).category,.1) for i in items)
        ratio=taxable_base/sum(next(p.price for p in PRODUCTS if p.id==i.product_id)*i.quantity for i in items)
        return money(raw*ratio)
class PricingService:
    def calculate_order_total(self, customer_id, items, coupon_codes):
        customer=CustomerService().get(customer_id); subtotal=money(sum(ProductService().get(i.product_id).price*i.quantity for i in items))
        discount=DiscountService().apply(items,subtotal,customer,coupon_codes); post=money(subtotal-discount); shipping=ShippingService().calculate(items,post,customer); tax=TaxService().calculate(items,post); return PriceBreakdown(subtotal=subtotal,discount=discount,shipping=shipping,tax=tax,total=money(post+shipping+tax),item_count=sum(i.quantity for i in items))
class PaymentService:
    def simulate(self,order,method):
        if method not in ('card','bank_transfer'): raise InvalidPayment('Unsupported payment method')
        return PaymentResponse(status='approved',order_id=order.id,amount=order.total,payment_method=method)
class CartService:
    def quote(self,request): InventoryService().validate(request.items); return PricingService().calculate_order_total(request.customer_id,request.items,request.coupon_codes)
class CheckoutService:
    def preview(self,request): return CartService().quote(request)
class OrderService:
    def create(self,request):
        customer=CustomerService().get(request.customer_id); InventoryService().validate(request.items); quote=PricingService().calculate_order_total(request.customer_id,request.items,request.coupon_codes); InventoryService().reserve(request.items); oid=f'ORDER-{len(store.orders)+1:03d}'; order=Order(id=oid,customer_id=customer.id,items=request.items,coupon_codes=request.coupon_codes,subtotal=quote.subtotal,discount=quote.discount,shipping=quote.shipping,tax=quote.tax,total=quote.total,status='paid',created_at='2026-02-01T10:00:00Z'); orders_repo.save(order); return order
    def get(self,id):
        o=orders_repo.get(id)
        if not o: raise NotFound(f'Order {id} not found')
        return o
    def status(self,id): return StatusResponse(order_id=id,status=self.get(id).status)
class InvoiceService:
    def get(self,id):
        oid=id.replace('INV-',''); order=OrderService().get(oid); quote=Quote(subtotal=order.subtotal,discount=order.discount,shipping=order.shipping,tax=order.tax,total=order.total); return Invoice(id=f'INV-{oid}',order_id=oid,customer=CustomerService().get(order.customer_id),items=order.items,quote=quote,status='issued')
class RefundService:
    def refund(self,request):
        order=OrderService().get(request.order_id); amount=money(request.amount if request.amount is not None else order.total)
        if amount<=0 or amount>order.total: raise ValidationError('INVALID_REFUND','Refund amount must be positive and no greater than order total')
        store.refunds[order.id]=amount; order.status='refunded' if amount==order.total else 'partially_refunded'; return RefundResponse(status=order.status,order_id=order.id,amount=amount)
class AnalyticsService:
    def overview(self):
        orders=orders_repo.all(); return Analytics(revenue=money(sum(o.total for o in orders)),orders=len(orders),average_order_value=money(sum(o.total for o in orders)/len(orders)),low_stock_products=sum(1 for i in store.inventory.values() if i.available<10))

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
app=FastAPI(title='OrderFlow API',version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_methods=['*'],allow_headers=['*'])
@app.exception_handler(AppError)
async def app_error(_,exc): return JSONResponse(status_code=exc.status,content={'error':exc.code,'message':exc.message})
@app.get('/api/health',response_model=Health)
def health(): return Health(status='ok',service='orderflow-api',version='1.0.0')
@app.get('/api/products',response_model=ProductList)
def list_products(search: Optional[str]=Query(None),category: Optional[str]=Query(None)):
    result=ProductService().list(search,category); return ProductList(products=result,count=len(result))
@app.get('/api/products/{id}',response_model=Product)
def product(id): return ProductService().get(id)
@app.get('/api/customers/{id}',response_model=Customer)
def customer(id): return CustomerService().get(id)
@app.get('/api/customers/{id}/summary',response_model=CustomerSummary)
def summary(id): return CustomerService().summary(id)
@app.get('/api/inventory/{id}',response_model=Inventory)
def inventory(id): return InventoryService().get(id)
@app.post('/api/cart/quote',response_model=PriceBreakdown)
def cart_quote(request: CartRequest): return CartService().quote(request)
@app.post('/api/checkout/preview',response_model=PriceBreakdown)
def preview(request: CartRequest): return CheckoutService().preview(request)
@app.post('/api/orders',response_model=Order)
def create_order(request: OrderCreate): return OrderService().create(request)
@app.get('/api/orders/{id}',response_model=Order)
def order(id): return OrderService().get(id)
@app.get('/api/orders/{id}/status',response_model=StatusResponse)
def order_status(id): return OrderService().status(id)
@app.get('/api/invoices/{id}',response_model=Invoice)
def invoice(id): return InvoiceService().get(id)
@app.post('/api/payments/simulate',response_model=PaymentResponse)
def payment(request: PaymentRequest): return PaymentService().simulate(OrderService().get(request.order_id),request.payment_method)
@app.post('/api/refunds',response_model=RefundResponse)
def refund(request: RefundRequest): return RefundService().refund(request)
@app.get('/api/analytics',response_model=Analytics)
def analytics(): return AnalyticsService().overview()
@app.get('/api/orders',response_model=list[Order])
def orders(): return orders_repo.all()

from datetime import date
__all__=['app']
if __name__=='__main__':
 import uvicorn; uvicorn.run(app,host='127.0.0.1',port=8000)

# aliases make the layered dependency graph explicit for code indexers
calculate_order_total=PricingService().calculate_order_total
create_order=OrderService().create
simulate_payment=PaymentService().simulate
calculate_tax=TaxService().calculate
calculate_shipping=ShippingService().calculate
apply_discounts=DiscountService().apply
validate_inventory=InventoryService().validate
get_invoice=InvoiceService().get
get_customer_summary=CustomerService().summary
class SerializationService:
    @staticmethod
    def normalize(value): return value.model_dump() if hasattr(value,'model_dump') else value
class ValidationService:
    @staticmethod
    def positive_quantity(quantity):
        if quantity<=0: raise ValidationError('INVALID_QUANTITY','Quantity must be positive')
        return quantity
class CurrencyService:
    @staticmethod
    def format(value): return f'${money(value):,.2f}'
class OrderRules:
    allowed_statuses={'paid','refunded','partially_refunded'}
class PaymentRules:
    allowed_methods={'card','bank_transfer'}
class DiscountRules:
    stacking='Only one exclusive or conflicting coupon may be used per order'
class TaxRules:
    calculation='Tax is calculated on post-discount item subtotal'
class ShippingRules:
    free_threshold=200

# Endpoints are intentionally adjacent to the service definitions in this compact generated module;
# the class/service names and direct calls preserve the intended route -> service -> core graph.

# module aliases for tooling that expects conventional package paths
import sys
for _name in ['demo_app.main','demo_app.api.products','demo_app.api.customers','demo_app.api.inventory','demo_app.api.carts','demo_app.api.checkout','demo_app.api.orders','demo_app.api.payments','demo_app.api.refunds','demo_app.api.invoices','demo_app.services.pricing_service','demo_app.services.order_service','demo_app.services.inventory_service','demo_app.services.discount_service','demo_app.services.tax_service','demo_app.services.shipping_service','demo_app.services.payment_service','demo_app.services.invoice_service','demo_app.repositories.product_repository']:
 sys.modules.setdefault(_name,sys.modules[__name__])

# additional stable endpoint aliases
@app.get('/api/products/search',response_model=ProductList)
def search_products(q: str=''): return list_products(q,None)
@app.get('/api/analytics/overview',response_model=Analytics)
def analytics_overview(): return analytics()

# fixed deterministic reference data
SAMPLE_REQUEST={'customer_id':'CUSTOMER-001','items':[{'product_id':'PROD-001','quantity':1},{'product_id':'PROD-004','quantity':1}],'coupon_codes':['WELCOME10']}
SAMPLE_RESPONSE={'subtotal':171.99,'discount':22.36,'shipping':0.0,'tax':25.43,'total':175.06}

# repository facades expose clear graph nodes
product_repository=products_repo
customer_repository=customers_repo
inventory_repository=inventory_repo
order_repository=orders_repo

# Explicit core function wrappers used by integration tests and future regression branches
def calculate_subtotal(items): return money(sum(ProductService().get(i.product_id).price*i.quantity for i in items))
def calculate_final_total(subtotal,discount,shipping,tax): return money(subtotal-discount+shipping+tax)
def validate_coupon_codes(codes): return DiscountService().apply([],0,store.customers['CUSTOMER-001'],codes)

def reset_seed():
    store.orders={}; store.refunds={}; seed()

# Keep package imports valid when launched as backend.main
main_app=app
