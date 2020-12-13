import json
from django.db.models import Q, Max, Min
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from app.serializers import *


class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializers
    http_method_names = ['get']
    permission_classes = [
        permissions.AllowAny
    ]
    ordering_fields = ['popularity']

    def get_queryset(self):
        kwargs = get_kwargs(self=self)
        category_id = self.request.query_params.get('category_id')
        if category_id is not None:
            category_involved = self.get_category_involved(category_id)
            kwargs['category__in'] = category_involved

        selected_price_range = self.request.query_params.getlist('price_range[]')
        if selected_price_range and len(selected_price_range) == 2:
            kwargs['minimum_price__gte'] = selected_price_range[0]
            kwargs['minimum_price__lte'] = selected_price_range[1]

        products = Product.objects.filter(**kwargs)

        order = self.request.query_params.get('ordering')
        if order is not None:
            products = products.order_by(order)

        return products

    @staticmethod
    def get_category_involved(category_id):
        return [p.id for p in list(
            Category.objects.filter(
                Q(children__isnull=True),
                Q(parent__parent_id=category_id) | Q(parent_id=category_id) | Q(id=category_id)
            )
        )]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.root_nodes()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CategorySerializer
    http_method_names = ['get']

    def get_object(self):
        return


class FilterByCategory(APIView):
    permission_classes = [
        permissions.AllowAny
    ]

    def get(self, request):
        category_id = self.request.query_params.get('category_id')
        kwargs = get_kwargs(self=self)
        kwargs['category_id'] = category_id
        products = Product.objects.filter(**kwargs)

        price_range = self.get_new_price_range(category_id)

        selected_price_range = self.request.query_params.getlist('price_range[]')
        if selected_price_range and len(selected_price_range) == 2:
            products = products.filter(minimum_price__gte=selected_price_range[0])
            products = products.filter(minimum_price__lte=selected_price_range[1])

        specs = self.get_new_specs(category_id, products)

        return Response({'specs': specs, 'price_range': price_range})

    @staticmethod
    def get_new_price_range(category_id):
        return [
            Product.objects.filter(category_id=category_id).aggregate(Min('minimum_price'))['minimum_price__min'],
            Product.objects.filter(category_id=category_id).aggregate(Max('minimum_price'))['minimum_price__max'],
        ]

    @staticmethod
    def get_new_specs(category_id, products):
        specs = []
        for propertyName in Filter.objects.get(category_id=category_id).fields:
            values = []
            for value in products.values_list(f'characteristics__{propertyName}', flat=True).distinct():
                values.append({
                    'name': value,
                    'count': products.filter(**{f'characteristics__{propertyName}': value}).distinct().count()
                })
            if values:
                specs.append({
                    'name': propertyName,
                    'values': values
                })
        return specs


def get_kwargs(self):
    params = self.request.query_params.get('checked_specs')
    specs = {}
    if params:
        specs = json.loads(params)
    kwargs = {
        f'characteristics__{field.rstrip("[]")}__in': specs[field]
        for field in specs
        if field != 'category_id' and field != 'ordering' and field != 'price_range[]'
    }
    return kwargs
