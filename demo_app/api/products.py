from demo_app.models.domain import ProductService

def list_products(search=None, category=None): return ProductService().list(search, category)
def get_product(product_id): return ProductService().get(product_id)

from demo_app.models.domain import app
products_router = app
