from fastapi.testclient import TestClient
from backend.main import app
from backend.models.domain import reset_seed
client=TestClient(app)
def setup_function(): reset_seed()
def test_health_and_products():
    assert client.get('/api/health').json()['status']=='ok'
    assert client.get('/api/products').json()['count']==10
def test_product_customer_inventory():
    assert client.get('/api/products/PROD-001').status_code==200
    assert client.get('/api/customers/CUSTOMER-001').status_code==200
    assert client.get('/api/inventory/PROD-001').json()['available']==18
def test_quote_and_preview_are_equal():
    body={'customer_id':'CUSTOMER-001','items':[{'product_id':'PROD-001','quantity':1}], 'coupon_codes':['WELCOME10']}
    quote=client.post('/api/cart/quote',json=body); preview=client.post('/api/checkout/preview',json=body)
    assert quote.status_code==preview.status_code==200
    assert quote.json()==preview.json()
def test_coupon_conflict():
    body={'customer_id':'CUSTOMER-001','items':[{'product_id':'PROD-001','quantity':2}], 'coupon_codes':['WELCOME10','HOLIDAY15']}
    response=client.post('/api/cart/quote',json=body)
    assert response.status_code==400 and response.json()['error']=='COUPON_CONFLICT'
def test_order_payment_invoice_refund_summary():
    body={'customer_id':'CUSTOMER-001','items':[{'product_id':'PROD-002','quantity':1}], 'coupon_codes':[]}
    order=client.post('/api/orders',json=body).json(); oid=order['id']
    assert client.get(f'/api/orders/{oid}').status_code==200
    assert client.post('/api/payments/simulate',json={'order_id':oid,'payment_method':'card'}).json()['status']=='approved'
    assert client.get(f'/api/invoices/INV-{oid}').json()['quote']['total']==order['total']
    assert client.post('/api/refunds',json={'order_id':oid}).json()['status']=='refunded'
    assert client.get('/api/customers/CUSTOMER-001/summary').status_code==200
def test_invalid_requests():
    assert client.get('/api/products/NOPE').status_code==404
    assert client.post('/api/cart/quote',json={'customer_id':'CUSTOMER-001','items':[{'product_id':'PROD-001','quantity':99}]}).status_code==422
