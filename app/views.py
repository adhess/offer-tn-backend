from django.db.models import Q
from rest_framework import viewsets, permissions
from app.serializers import *


class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializers
    http_method_names = ['get']
    permission_classes = [
        permissions.AllowAny
    ]
    ordering_fields = ['popularity']

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        print(category_id)
        order = self.request.query_params.get('ordering')
        if category_id is None:
            return Product.objects.all().order_by('-popularity')

        category_involved = [p.id for p in list(
            Category.objects.filter(
                Q(children__isnull=True),
                Q(parent__parent_id=category_id) | Q(parent_id=category_id) | Q(id=category_id)
            )
        )]

        if order is None:
            return Product.objects.filter(category__in=category_involved)

        return Product.objects.filter(category__in=category_involved).order_by(order)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.root_nodes()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CategorySerializer
    http_method_names = ['get']

    def get_object(self):
        return
