from rest_framework import routers
from .views import ProductsViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'views/products', ProductsViewSet, 'products')
router.register(r'views/categories', CategoryViewSet, 'categories')

urlpatterns = router.urls

