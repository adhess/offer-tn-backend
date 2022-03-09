from itemloaders.processors import MapCompose, Join, Identity, Compose, TakeFirst
from w3lib.html import remove_tags, unquote_markup
from ecommerce_scraper.ecommerce_scraper.loaders import ProductItem
from scrapy.loader import ItemLoader
import pytest


@pytest.fixture
def item_loader(response_stub):
    item = ProductItem()
    product_loader = ItemLoader(response=response_stub, item=item)
    return product_loader


def test_loading_item_name(item_loader):
    item_loader.name_out = TakeFirst()
    item_loader.add_css("name", "h1::text")

    item = item_loader.load_item()
    assert item["name"] == "Pc Portable Asus Gaming TUF 505DT AMD R5 16Go 512GO SSD Noir"


def test_specific_output_processor_overrides_default(item_loader):
    item_loader.default_output_processor = lambda fields: [field.lower() for field in fields]
    item_loader.name_out = lambda fields: [field.upper() for field in fields]
    item_loader.add_css("name", "h1::text")

    item = item_loader.load_item()
    assert item["name"] == ["Pc Portable Asus Gaming TUF 505DT AMD R5 16Go 512GO SSD Noir".upper()]


def test_loading_item_with_map_compose(item_loader):
    item_loader.description_in = MapCompose(remove_tags, unquote_markup)
    item_loader.description_out = Join()
    item_loader.add_css("description", "#tab2+ #tab3 td")

    item = item_loader.load_item()
    expected_description = ('Marque ASUS Couleur Noir Garantie 2 ans Processeur  AMD Ryzen 5 Type '
                            'processeur Quad core Fréquence processuer 2.1 GHz up to 3.7 GHz Référence '
                            'Processeur AMD RYZEN R5-3550H Mémoire cache 2Mo Mémoire Ram 16 Go '
                            'Connecteurs 1x USB 2.0 Type-A, 2x USB 3.2 Gen 1 Type-A, 1x Jack Combo Audio '
                            '3.5mm, 1x HDMI 2.0 Carte graphique NVIDIA GeForce GTX 1650 4Go Bluetooth Oui '
                            'Connectivité sans fil Wifi Batterie 3 cellules Ecran Tactile Non Type Ecran '
                            'FULL HD Capacité du disque dur 512 Go SSD Type de mémoire DDR4 Chipset '
                            'graphique NVIDIA GeForce GTX1650 Résolution Max 1920 x 1080 pixels Taille '
                            'd\'écran en pouces 15.6" Type de système d\'exploitation Windows')

    assert item["description"] == expected_description


