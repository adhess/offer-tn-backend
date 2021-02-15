import json
from django.db.models import Max, Min
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import ProductVendorDetails, Product, Category, Filter
from app.serializers import ProductVendorDetailsSerializers, ProductSerializers, CategorySerializer
from app.filters import M2MFilter


class ProductVendorDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductVendorDetails.objects.all()
    serializer_class = ProductVendorDetailsSerializers
    permission_classes = [permissions.AllowAny]
    filter_backends = [M2MFilter]


class ProductsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializers
    permission_classes = [
        permissions.AllowAny
    ]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['minimum_price', 'popularity', 'name']

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

        return Product.objects.filter(**kwargs)

    @staticmethod
    def get_category_involved(category_id):
        category = Category.objects.get(pk=category_id)
        return category.get_descendants(include_self=True).filter(children__isnull=True)


class PopularProductsLandingPage(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializers
    permission_classes = [
        permissions.AllowAny
    ]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['popularity']

    def get_queryset(self):
        return Product.objects.all().order_by('popularity')[:12]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CategorySerializer

    def get_queryset(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg in self.kwargs:
            return Category.objects.all()
        return Category.objects.root_nodes()


class FilterByCategory(APIView):
    permission_classes = [
        permissions.AllowAny
    ]

    def get(self, request):
        category_id = self.request.query_params.get('category_id')
        kwargs = {'category_id': category_id}
        products = Product.objects.filter(**kwargs)

        price_range = self.get_new_price_range(category_id)

        selected_price_range = self.request.query_params.getlist('price_range[]')
        if selected_price_range and len(selected_price_range) == 2:
            products = products.filter(minimum_price__gte=selected_price_range[0])
            products = products.filter(minimum_price__lte=selected_price_range[1])

        specs = self.get_new_specs(self, category_id, products)
        return Response({'specs': specs, 'price_range': price_range})

    @staticmethod
    def get_new_price_range(category_id):
        return [
            Product.objects.filter(category_id=category_id).aggregate(Min('minimum_price'))['minimum_price__min'],
            Product.objects.filter(category_id=category_id).aggregate(Max('minimum_price'))['minimum_price__max'],
        ]

    @staticmethod
    def get_new_specs(self, category_id, products):
        specs = []
        kwargs = get_kwargs(self=self)
        kwargs['category_id'] = category_id
        for propertyName in Filter.objects.get(category_id=category_id).fields:
            values = []
            for value in products.values_list(f'characteristics__{propertyName}', flat=True).distinct():
                if value:
                    values.append({
                        'name': value,
                        'count': products.filter(**kwargs).filter(
                            **{f'characteristics__{propertyName}': value}).distinct().count()
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
