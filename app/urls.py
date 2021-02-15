from django.urls import path
from rest_framework import routers
from .views import ProductsViewSet, CategoryViewSet, ProductVendorDetailsViewSet, FilterByCategory, \
    PopularProductsLandingPage

router = routers.DefaultRouter()
router.register(r'api/products', ProductsViewSet, 'products')
router.register(r'api/categories', CategoryViewSet, 'categories')
router.register(r'api/productvendordetails', ProductVendorDetailsViewSet, 'productvendordetails')
router.register(r'api/get_popular_products_landing_page', PopularProductsLandingPage,
                'get_popular_products_landing_page')

urlpatterns = [
    path('api/getFilterByCategory/', FilterByCategory.as_view())
]

urlpatterns += router.urls

