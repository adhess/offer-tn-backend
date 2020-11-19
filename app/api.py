from django.db.models import Q
from rest_framework import viewsets, permissions

from .models import Category, Product
from .serializers import ProductSerializers, CategorySerializer


class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializers
    http_method_names = ['get']
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        category_name = self.request.query_params.get('category_name')
        category_involved = [p.id for p in list(
            Category.objects.filter(
                Q(children__isnull=True),
                Q(parent__parent__name=category_name) | Q(parent__name=category_name) | Q(name=category_name)
            )
        )]
        return Product.objects.filter(category__in=category_involved)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.root_nodes()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CategorySerializer
    http_method_names = ['get']

    def get_object(self):
        return
