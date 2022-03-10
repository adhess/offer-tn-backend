import factory
from mimesis_factory import MimesisField
from app.models import Product, Vendor, Category, ProductVendorDetails


class VendorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vendor

    name = MimesisField('company')
    website = factory.LazyAttribute(lambda vendor: f'{vendor.name}.com')
    logo_url = factory.LazyAttribute(lambda vendor: f'{vendor.name}.logo.com')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    class Params:
        depth = 0

    name = factory.Sequence(lambda n: f"category-{n}")
    icon = factory.LazyAttribute(lambda category: f'{category.name}.icon.com')
    is_active = MimesisField("boolean")
    parent = None

    @classmethod
    def create(cls, **kwargs):
        parent = kwargs.pop('parent', None)
        if parent:
            return super().create(parent=parent, **kwargs)

        return cls.make_hierarchy_of_categories_of_given_depth(parent, **kwargs)

    @classmethod
    def make_hierarchy_of_categories_of_given_depth(cls, parent, **kwargs):
        depth = kwargs.pop('depth', 0)
        while depth >= 0:
            parent = super().create(parent=parent, depth=depth, **kwargs)
            depth -= 1
        return parent


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = MimesisField("phone_model")
    reference = factory.LazyAttributeSequence(lambda product, count: f'{product.name}-{count}')
    characteristics = factory.Dict(dict(color=MimesisField("color")))
    popularity = MimesisField("integer_number", start=0)
    category = factory.SubFactory(CategoryFactory)
    image_url = factory.LazyAttribute(lambda product: f'{product.name}.image.com')
    minimum_price = 0


class ProductVendorDetailsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductVendorDetails
        exclude = ('num_of_years',)

    product = factory.SubFactory(ProductFactory)
    vendor = factory.SubFactory(VendorFactory)
    link_in_vendor_website = factory.LazyAttribute(lambda pvd: f'{pvd.vendor.website}/{pvd.product.reference}')
    is_discount_available = MimesisField("boolean")
    num_of_years = MimesisField("choice", items=range(5))
    warranty = factory.LazyAttribute(lambda pvd: f'{pvd.num_of_years} Year(s)')
    inventory_state = MimesisField("choice", items=["IS", "OOS", "IT", "OC"])
    registered_prices = MimesisField("floats", start=0, end=10000, precision=2, n=3)



