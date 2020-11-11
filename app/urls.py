from rest_framework import routers
from .api import ProductsViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'api/products', ProductsViewSet, 'products')
router.register(r'api/categories', CategoryViewSet, 'categories')

urlpatterns = router.urls

