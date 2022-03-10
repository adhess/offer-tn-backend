from app.model_factories import CategoryFactory, ProductFactory, VendorFactory, ProductVendorDetailsFactory
from ecommerce_scraper.ecommerce_scraper.factories import ProductItemFactory
from pytest_factoryboy import register


register(CategoryFactory)
register(ProductFactory)
register(VendorFactory)
register(ProductVendorDetailsFactory)
register(ProductItemFactory)

