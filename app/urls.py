from django.urls import path
from rest_framework import routers
from .views import ProductsViewSet, CategoryViewSet, ProductVendorDetailsViewSet, FilterByCategory

router = routers.DefaultRouter()
router.register(r'api/products', ProductsViewSet, 'products')
router.register(r'api/categories', CategoryViewSet, 'categories')
router.register(r'api/productvendordetails', ProductVendorDetailsViewSet, 'productvendordetails')

urlpatterns = [
    path('api/getFilterByCategory/', FilterByCategory.as_view())
]

urlpatterns += router.urls

