from django.db import IntegrityError
from scrapy.exceptions import DropItem
from app.models import Product, ProductVendorDetails


class ProductManager:
    @staticmethod
    def update_with_item(product, item):
        product.name = item.get('name')
        product.reference = item.get('reference')
        product.image_url = item.get('image_url')
        product.characteristics = item.get('characteristics')
        product.save()

    @staticmethod
    def get_similar_products(item):
        products = Product.objects.filter(
            category=item['category'],
        )
        return products

    @staticmethod
    def create_new_product(item):
        try:
            product = Product.objects.create(
                name=item['name'],
                reference=item['reference'],
                category=item['category'],
                image_url=item['image_url'],
                minimum_price=item['price'],
                characteristics=item['characteristics']
            )
            return product

        except KeyError as e:
            error_message = f"missing {str(e)} from scrapy item"
            raise DropItem(error_message) from e
        except (IntegrityError, ValueError) as e:
            error_message = str(e)
            raise DropItem(error_message) from e

    @staticmethod
    def to_dict(product):
        from django.forms.models import model_to_dict
        return model_to_dict(product,
                             fields=["name", "category", "reference", "characteristics", "image_url", "minimum_price"],
                             )


class ProductVendorDetailsManager:
    @staticmethod
    def update_with_item(product_vendor_details, item):
        product_vendor_details.link_in_vendor_website = item['url']
        product_vendor_details.warranty = item['warranty']
        product_vendor_details.registered_prices.append(item['price'])
        product_vendor_details.save()

    @staticmethod
    def create_product_vendor_details(item, vendor):
        try:
            return ProductVendorDetails.objects.create(
                product=item['product'],
                vendor=vendor,
                link_in_vendor_website=item['url'],
                warranty=item['warranty'],
                registered_prices=[item['price']],
            )
        except KeyError as e:
            error_message = f"missing {str(e)} from scrapy item"
            raise DropItem(error_message) from e
        except (IntegrityError, ValueError) as e:
            error_message = str(e)
            raise DropItem(error_message) from e

    @staticmethod
    def get_product_vendor_details(product, vendor):
        return product.details.filter(vendor=vendor).first()


class CategoryManager:
    @staticmethod
    def is_descendent_of(category, parent_name, include_self=False):
        if include_self and category.name == parent_name:
            return True
        return parent_name in (ancestor.name for ancestor in category.get_ancestors())
