from backend.models.domain import products_repo

def get_product(product_id): return products_repo.get(product_id)
def list_products(): return products_repo.all()
