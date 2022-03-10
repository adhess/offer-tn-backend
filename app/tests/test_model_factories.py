from app.models import Category, Product, Vendor, ProductVendorDetails
import pytest
import re


@pytest.fixture
def default_vendor(vendor_factory):
    return vendor_factory()


@pytest.fixture
def product(product_factory):
    return product_factory(__sequence=1)


@pytest.mark.django_db
class TestCategoryFactory:
    @pytest.fixture
    def default_category(self, category_factory):
        category_factory.reset_sequence()
        return category_factory()

    def test_default_name_format(self, category_factory):
        category_factory.reset_sequence()
        for i in range(3):
            category = category_factory()
            assert category.name == f"category-{i}"

    def test_default_icon_format(self, default_category):
        assert default_category.icon == f"{default_category.name}.icon.com"

    def test_default_is_active_is_boolean(self, default_category):
        assert isinstance(default_category.is_active, bool)

    def test_default_parent_is_none(self, default_category):
        assert default_category.parent is None

    def test_persists_in_db(self, default_category):
        assert Category.objects.get(name=default_category.name) == default_category

    @pytest.mark.parametrize("tree_depth", [0, 1, 5])
    def test_creates_a_hierarchy_of_given_depth(self, tree_depth, category_factory):
        category_factory.reset_sequence()
        category = category_factory(depth=tree_depth)
        for curr_depth in range(tree_depth, -1, -1):
            assert category.name == f"category-{curr_depth}"
            category = category.parent

    @pytest.mark.parametrize("tree_depth", [None, 0, 1, 5])
    def test_no_hierarchy_is_created_if_parent_is_passed(self, tree_depth, category_factory):
        immediate_parent = category_factory(name='immediate_parent')
        category = category_factory(depth=tree_depth, parent=immediate_parent)
        assert category.parent.name == 'immediate_parent'
        assert immediate_parent.parent is None

    def test_creates_nothing_given_negative_depth(self, category_factory):
        category = category_factory(depth=-1)
        assert category is None


@pytest.mark.django_db
class TestVendorFactory:

    def test_default_returns_different_names(self, vendor_factory):
        vendor1 = vendor_factory()
        vendor2 = vendor_factory()
        assert vendor1.name != vendor2.name

    def test_default_name_is_string(self, default_vendor):
        assert isinstance(default_vendor.name, str)

    def test_default_website_format(self, default_vendor):
        assert default_vendor.website == default_vendor.name + ".com"

    def test_default_logo_url_format(self, default_vendor):
        assert default_vendor.logo_url == default_vendor.name + ".logo.com"

    def test_persists_in_db(self, default_vendor):
        assert Vendor.objects.get(name=default_vendor.name) == default_vendor


@pytest.mark.django_db
class TestProductFactory:

    def test_default_name_is_string(self, product):
        assert isinstance(product.name, str)

    def test_default_category_is_valid_category(self, product):
        assert isinstance(product.category, Category)

    def test_default_price_is_zero(self, product):
        assert product.minimum_price == 0

    def test__default_popularity_is_integer(self, product):
        assert isinstance(product.popularity, int)

    def test_default_format_of_image_url(self, product):
        assert product.image_url == product.name + ".image.com"

    def test_default_reference_format(self, product):
        assert product.reference == product.name + "-1"

    def test_default_characteristics_is_dict(self, product):
        characteristics = product.characteristics
        assert isinstance(characteristics, dict)
        assert isinstance(characteristics["color"], str)

    def test_persists_in_db(self, product):
        assert Product.objects.get(name=product.name, reference=product.reference) is not None

    def test_default_returns_different_random_names(self, product_factory):
        product = product_factory()
        product2 = product_factory()
        assert product2.name != product.name

    def test_default_reference_increments(self, product_factory):
        product_factory.reset_sequence()
        first_product = product_factory()
        second_product = product_factory()

        assert first_product.reference[-1] == '0'
        assert second_product.reference[-1] == '1'


@pytest.mark.django_db
class TestProductVendorDetailsFactory:
    @pytest.fixture
    def default_product_vendor_details(self, product_vendor_details_factory):
        return product_vendor_details_factory()

    def test_default_has_valid_product(self, default_product_vendor_details):
        assert isinstance(default_product_vendor_details.product, Product)

    def test_default_has_valid_vendor(self, default_product_vendor_details):
        assert isinstance(default_product_vendor_details.vendor, Vendor)

    def test_default_link_in_vendor_website_format(self, default_product_vendor_details):
        assert (default_product_vendor_details.link_in_vendor_website ==
                f"{default_product_vendor_details.vendor.website}/{default_product_vendor_details.product.reference}")

    def test_default_discount_available_is_boolean(self, default_product_vendor_details):
        assert isinstance(default_product_vendor_details.is_discount_available, bool)

    def test_default_warranty_format(self, default_product_vendor_details):
        warranty = default_product_vendor_details.warranty
        assert re.fullmatch(r'\d Year\(s\)', warranty)

    def test_default_inventory_state_is_valid(self, default_product_vendor_details):
        inventory_state = default_product_vendor_details.inventory_state
        valid_states = {choice[0] for choice in ProductVendorDetails.InventoryState.choices}
        assert inventory_state in valid_states

    def test_default_registered_prices_is_list_of_int(self, default_product_vendor_details):
        prices = default_product_vendor_details.registered_prices
        assert type(prices) == list
        assert len(prices) == 3
        assert isinstance(prices[0], float)
