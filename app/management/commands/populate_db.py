import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from app.models import *

from .mock_data import mock_data
import string


def get_random_string():
    letters = string.ascii_letters + "0123456789-"
    result_str = ''.join(random.choice(letters) for i in range(25))
    return result_str


def _populate(self):
    vendors = [
        Vendor(name='myteck', website='https://mytek.tn/',
               logo_url='https://web-assets-mk.s3.amazonaws.com/img/mytek-informatique-logo-1482243620.jpg'),
        Vendor(name='tunisianet', website='https://www.tunisianet.com.tn/',
               logo_url='https://www.tunisianet.com.tn/img/tunisianet-logo-1573421421.jpg'),
        Vendor(name='wiki', website='https://www.wiki.tn/', logo_url='https://www.wiki.tn/img/logo.jpg'),
        Vendor(name='scoop', website='https://www.scoop.com.tn/',
               logo_url='https://www.scoop.com.tn/img/sp-g3shop-logo-1591977520.jpg'),
        Vendor(name='sbsinformatique', website='https://www.sbsinformatique.com/',
               logo_url='https://www.sbsinformatique.com/img/prestashop-logo-1585766163.jpg'),
    ]
    for v in vendors:
        v.save()
    images = {
        'Clothing': [
            'https://matalan-content.imgix.net/uploads/asset_file/asset_file/284191/1598949135.3114743-S2797036_C228_Alt1.jpg?ixlib=rails-2.1.4&auto=format%2Ccompress&cs=tinysrgb&w=446&s=e1d4ab69d70f25d2614001c28039fb45',
            'https://static.zara.net/photos///rw-center/2020/I/0/1/p/7969/227/800/8/w/1839/7969227800_2_1_1.jpg?ts=1605713894346',
            'https://static.zara.net/photos///2020/I/0/1/p/7969/224/800/2/w/913/7969224800_2_1_1.jpg?ts=1605705252652',
            'https://static.zara.net/photos///2020/I/0/1/p/7969/224/800/2/w/914/7969224800_1_1_1.jpg?ts=1605705244985',
            'https://static.zara.net/photos///2020/I/0/1/p/3666/184/800/3/w/913/3666184800_2_1_1.jpg?ts=1605705914635',
            'https://static.zara.net/photos///2020/I/0/1/p/0858/054/753/4/w/1841/0858054753_9_20_1.jpg?ts=1605800021018',
            'https://static.zara.net/photos///rw-center/2021/V/0/1/p/5320/712/806/3/w/1841/5320712806_1_1_1.jpg?ts=1605613271445',
            'https://media.boohoo.com/i/boohoo/fzz02006_black_xl?$product_image_category_page_horizontal_filters_desktop$&fmt=webp',
            'https://media.boohoo.com/i/boohoo/fzz51340_stone_xl?$product_image_category_page_horizontal_filters_desktop$&fmt=webp',
            'https://media.boohoo.com/i/boohoo/pzz62023_grey_xl?$product_image_category_page_horizontal_filters_desktop$&fmt=webp',
            'https://media.boohoo.com/i/boohoo/pzz58815_grey_xl?$product_image_category_page_horizontal_filters_desktop$&fmt=webp',
            'https://cdn.clothingshoponline.com/Images/Style/403_fm.jpg',
            'https://cdn.clothingshoponline.com/Images/Style/2769_fm.jpg',
            'https://cdn.clothingshoponline.com/Images/Style/3644_fm.jpg',
            'https://cdn.clothingshoponline.com/Images/Style/394_fm.jpg',
            'https://www.clothingshoponline.com/p/boxercraft/t66_women%E2%80%99s-preppy-patch-slub-long-sleeve-t-shirt',
            'https://matalan-content.imgix.net/uploads/asset_file/asset_file/288895/1600414320.9883795-S2790526_C323_Alt1.jpg?ixlib=rails-2.1.4&auto=format%2Ccompress&cs=tinysrgb&w=446&s=91192fd658d083c822115e1e168b5700',
            'https://matalan-content.imgix.net/uploads/asset_file/asset_file/292086/1602227016.5904317-S2798784_C526_Alt1.jpg?ixlib=rails-2.1.4&auto=format%2Ccompress&cs=tinysrgb&w=446&s=7ef7ce6d82567b83973b2b0cb12092f8',
            'https://matalan-content.imgix.net/uploads/asset_file/asset_file/288907/1603787515.3169305-S2798789_C47Q_Alt1.jpg?ixlib=rails-2.1.4&auto=format%2Ccompress&cs=tinysrgb&w=446&s=299f5e17694b0fbce29900605ed44710',
            'https://matalan-content.imgix.net/uploads/asset_file/asset_file/288908/1604492533.2555664-S2798792_C333_Alt1.jpg?ixlib=rails-2.1.4&auto=format%2Ccompress&cs=tinysrgb&w=446&s=860e9bb3341086e822161fcbf3fcb5f3',
            'https://matalan-content.imgix.net/uploads/asset_file/asset_file/288910/1601624721.2960753-S2798899_C101_Alt1.jpg?ixlib=rails-2.1.4&auto=format%2Ccompress&cs=tinysrgb&w=446&s=c9b6f5b435adf24cd1d945062ef03c56',
            'https://matalan-content.imgix.net/uploads/asset_file/asset_file/292186/1603787515.7513235-S2798903_C333_Alt1.jpg?ixlib=rails-2.1.4&auto=format%2Ccompress&cs=tinysrgb&w=446&s=842b8f44b0f548c453c0050b62b51003',
        ],
        'Food': [
            'https://www.onamangepourvous.tn/wp-content/uploads/2017/12/90.jpg',
            'https://www.onamangepourvous.tn/wp-content/uploads/2017/12/92.jpg',
            'https://www.onamangepourvous.tn/wp-content/uploads/2017/12/95.jpg',
            'https://i.fatafeat.com/storage/recipes/03-MSA_S01_SH02_PAN-FRIED-LAMB-GARLIC-AND-ROSEMARY_IMGL1766_221371_medium.jpg',
            'https://i.fatafeat.com/storage/recipes/MSA_S01_SH03_CHOCOLATE-BOWL-WITH-FRUITS_IMGL1936_882581_medium.jpg',
            'https://i.fatafeat.com/storage/recipes/130_Aysh_El_Saraya_2_18-46-31-08_983153_medium.png',
            'https://i.fatafeat.com/storage/recipes/140226100243638~Fish%20lettuce%20wrap.jpg',
            'https://i.fatafeat.com/storage/attachments/1/temp_14743915801803308427448998448_595210_medium.jpg',
            'https://i.fatafeat.com/storage/recipes/YYYYYYYY_YYYYYYYYY_639917_medium.jpg',
            'https://i.fatafeat.com/storage/recipes/MSA_S01_SH04_01-SAMOSA-ROLLS-MUSAKHAN-CHEESE_IMGL1993_885487_medium.jpg',
            'https://i.fatafeat.com/storage/recipes/02_MAA_S04_SH27_MEATBALLS_WITH_YOGHURT_AND_HERBS_IMGL1273_473003_medium.jpg',
        ],
        'Computers': [
            'https://www.wiki.tn/54636-home_default_mobi/pc-portable-hp-pavilion-gaming-15-ec0006nk-amd-8go-1to128go-gtx-3go.jpg',
            'https://www.wiki.tn/52149-home_default_mobi/pc-portable-gamer-lenovo-l340-i5-9e-gen-8go-2to-noir-.jpg',
            'https://www.wiki.tn/53841-home_default_mobi/pc-portable-asus-f571lh-i5-10e-8go-512-go-ssd-4g-win10-noir.jpg',
            'https://www.wiki.tn/52252-home_default_mobi/pc-portable-gamer-lenovo-l340-i7-9e-gen-8go-2to-gtx1050-noir.jpg',
            'https://www.wiki.tn/54494-home_default_mobi/pc-portable-acer-nitro-5-an515-54-i5-9e-gen-16go-1to128go-ssd.jpg',
            'https://www.wiki.tn/55286-home_default_mobi/pc-portable-gamer-msi-gf63-thin-10scxr-i5-10e-gen-32go-512go-gtx1650.jpg',
            'https://www.wiki.tn/43304-home_default_mobi/pc-portable-lenovo-legion-y540-i5-9e-gen-8go-1to128go-ssd.jpg',
            'https://www.wiki.tn/53275-home_default_mobi/pc-portable-gamer-asus-tuf-506ii-bq243t-amd-8go-512go-ssd-4go-win10.jpg',
            'https://www.wiki.tn/52605-home_default_mobi/pc-portable-gamer-lenovo-l340-i7-9e-gen-16go-2to256ssd-1650gtx.jpg',
            'https://www.wiki.tn/53619-home_default_mobi/pc-portable-asus-tuf-a15-amd-ryzen-r7-8go-512go-gtx1660ti-gris.jpg',
            'https://www.wiki.tn/55797-home_default_mobi/pc-portable-gamer-lenovo-legion5-ryzen-7-16go-1to-128go-4-go.jpg',
            'https://www.wiki.tn/55740-home_default_mobi/pc-portable-gamer-asus-rog-strix-g512li-i7-10e-gen-8go-512-go-win10.jpg',
            'https://www.wiki.tn/54083-home_default_mobi/pc-portable-gamer-asus-rog-strix-g15-i7-10e-gen-8go-512-go-ssd.jpg'
        ],
        'SmartPhone': [
            'https://www.wiki.tn/49750-home_default_mobi/smartphone-honor-8a-pro-bleu-.jpg',
            'https://www.wiki.tn/52619-home_default_mobi/smartphone-infinix-hot-8-4g-noir.jpg',
            'https://www.wiki.tn/52620-home_default_mobi/smartphone-infinix-hot-8-4g-purple.jpg',
            'https://www.wiki.tn/52622-home_default_mobi/smartphone-infinix-hot-8-4g-gris.jpg',
            'https://www.wiki.tn/55123-home_default_mobi/honor-8a-bleu-.jpg',
            'https://www.wiki.tn/55120-home_default_mobi/honor-8a-rouge.jpg',
            'https://www.wiki.tn/40680-home_default_mobi/samsung-galaxy-s10.jpg',
            'https://images.ctfassets.net/wcfotm6rrl7u/2Obq6PBk4Itttstt47qoG4/0caca27b1e3ff118f9580420650a57b6/nokia_5_3-front_back-Cyan.png?w=230&h=230&fit=pad&bg=rgb:fff',
            'https://images.ctfassets.net/wcfotm6rrl7u/21STLirH16JPA0KmAq2blL/c688e4d3f50e50c57ffd62e3ee214e32/nokia_6_2-front_back-ice.png?w=230&h=230&fit=pad&bg=rgb:fff',
            'https://images.ctfassets.net/wcfotm6rrl7u/2dz1S5fKh1TJUYQF16XrZZ/66c1ada26a46bf3050cccbf4d549314e/nokia_4_2-front_back-Pink.png?w=230&h=230&fit=pad&bg=rgb:fff',
            'https://images.ctfassets.net/wcfotm6rrl7u/2sO5H02uVGptb7Y68jrii7/ce5058dab120782b49f1801a9c9f6bd9/nokia_3_4-front_back-Fjord.png?w=230&h=230&fit=pad&bg=rgb:fff',
            'https://images.ctfassets.net/wcfotm6rrl7u/6MHf3EPng9LoIMTIUlj8sk/12c24603b5fc273c573ba00426589a97/nokia_C3-front_back-Nordic_Blue.png?w=230&h=230&fit=pad&bg=rgb:fff',
            'https://images.ctfassets.net/wcfotm6rrl7u/6960cFaQX8pOTsuT5DML7D/cafcf36fea35cda0a87e14a179d6028b/nokia_2_3-front_n_back-cyan_green.png?w=230&h=230&fit=pad&bg=rgb:fff',
        ],
        'Camera': [
            'https://www.wiki.tn/53210-home_default_mobi/appareil-photo-reflex-numerique-canon-eos-80d-wifi-obj-18-55-is-stm.jpg',
            'https://www.wiki.tn/30027-home_default_mobi/appareil-photo-nikon-d7200-objectif-18-140.jpg',
            'https://www.wiki.tn/53202-home_default_mobi/appareil-reflex-numerique-canon-eos-5d-mark-iv-body.jpg',
            'https://www.wiki.tn/53216-home_default_mobi/appareil-photo-reflex-numerique-canon-eos-80d-objectif-ef-s-18-135mm-s.jpg',
            'https://www.e-infin.com/image/300/estorethumb/3999.jpg',
            'https://www.e-infin.com/image/300/estorethumb/3556.jpg',
            'https://www.e-infin.com/image/300/estorethumb/4072.jpg',
            'https://www.e-infin.com/image/300/estorethumb/4165.jpg',
            'https://www.e-infin.com/image/300/estorethumb/4178.jpg',
            'https://www.e-infin.com/image/300/estorethumb/4179.jpg',
            'https://www.e-infin.com/image/300/estorethumb/4177.jpg',
            'https://www.e-infin.com/image/300/estorethumb/4176.jpg',
            'https://www.e-infin.com/image/300/estorethumb/4175.jpg',
        ],
        'Beauty': [
            'https://beautystore.tn/4335-home_default/revolution-palette-fard-a-joues-ultra-blush-hot-spice.jpg',
            'https://beautystore.tn/6284-home_default/catrice-vernis-a-ongles-ico-nails.jpg',
            'https://beautystore.tn/3569-home_default/i-revolution-palette-chocolate-rose-gold.jpg',
            'https://beautystore.tn/4670-home_default/revolution-palette-fard-a-paupiere-reloaded-iconic-fever.jpg',
            'https://beautystore.tn/3649-home_default/revolution-spray-fixateur-sport-fix.jpg',
            'https://beautystore.tn/6514-home_default/catrice-rouge-a-levres-demi-matt-lipstick-.jpg',
            'https://beautystore.tn/4074-home_default/artdeco-fond-de-teint-liquid-camouflage.jpg',
            'https://beautystore.tn/2500-home_default/essence-mascara-lash-and-brow-gel.jpg',
            'https://beautystore.tn/850-home_default/essence-eyeliner-liquid-ink-wp.jpg',
        ],
        'Travel': [
            'https://www.travelstore.tn/blogs/38-aya-sofia-istanbul.jpg',
            'https://www.travelstore.tn/blogs/34-tanzani-park.jpg',
            'https://www.travelstore.tn/blogs/7-iran.jpg',
            'https://www.travelstore.tn/blogs/8-Dubai-new.jpg',
            'https://www.travelstore.tn/pays/63-Gammarth.png',
            'https://www.travelstore.tn/pays/19-Mahdia.png',
            'https://www.travelstore.tn/voyages/65-Ocean-Haven-Pool1.jpg',

        ],
        'Jobs': ['https://www.tanitjobs.com/templates/Tanitjobsv7/assets/images/img-centre-appel.jpg'],
        'Painting': [
            'https://www.mab.com.tn/img/p/4/1/6/1/4161-large_default.jpg',
            'https://www.mab.com.tn/img/p/3/3/3/1/3331-large_default.jpg',
            'https://www.mab.com.tn/img/p/4/4/0/5/4405-thickbox_default.jpg',
            'https://www.mab.com.tn/img/p/4/4/1/5/4415-thickbox_default.jpg',
        ],
    }
    arr = []

    for c in mock_data:
        get_child_category(arr=arr, data=c, parent=None)

    for category in arr:
        for k in range(30, 100):
            product = Product(
                category=category,
                characteristics={
                    'Processor': 'i' + str(2 * random.randint(1, 4) + 1) + '-' + str(
                        random.randint(2000, 11986)) + 'H',
                    'Graphic card': 'NVIDIA GeForce ' + (
                        'GTX' if random.randint(0, 1) % 2 == 1 else 'RTX') + ' ' + str(
                        random.randint(1000, 3200)) + ' (4 Go GDDR5)',
                    'Screen': ['17.3"', '15.6"', '14"', '13.3"', '12"'][random.randint(0, 4)] + (
                        '' if random.randint(0, 1) % 2 == 1 else 'Full') + ' HD',
                    'RAM': str(random.randint(2, 128)) + ' Go DDR4',
                    'OS': ['FreeDos', 'Ubuntu', 'Windows'][random.randint(0, 2)],
                    'color': ['black', 'red', 'blue', 'pink'][random.randint(0, 3)]
                },
                name='best computer ever ' + get_random_string(),
                image_url=images[category.name][random.randint(0, len(images[category.name]) - 1)],
                popularity=random.randint(15, 100),
                ref=get_random_string()
            )
            product.save()

            for j in range(random.randint(1, 3)):
                stat = [
                    ProductVendorDetails.InventoryState.IN_STOCK,
                    ProductVendorDetails.InventoryState.IN_TRANSIT,
                    ProductVendorDetails.InventoryState.ON_COMMAND,
                    ProductVendorDetails.InventoryState.OUT_OF_STOCK,
                ]
                min_registered_prices = []
                date = datetime(2019, 3, 5)
                for i in range(0, 15):
                    length = len(min_registered_prices)
                    price = 0 if length == 0 else min_registered_prices[length - 1]
                    min_registered_prices.append(
                            price if length > 0 and random.randint(0, 1) == 0 else random.randint(1000, 7000)
                    )
                    date += timedelta(7)
                product_details = ProductVendorDetails(
                    discount_available=random.randint(0, 1) % 2 == 1,
                    inventory_state=stat[random.randint(0, 3)],
                    product=product,
                    unit_price=min_registered_prices[len(min_registered_prices) - 1],
                    url='https://www.wiki.tn/pc-portables-gamer/pc-portable-gamer-asus-zenbook-pro-duo-i9-10e-gen-32go-1to-ssd-32231.html',
                    vendor=vendors[random.randint(0, 4)],
                    warranty=['1 ans', '2 ans', '3 ans', '4 ans', '5 ans'][random.randint(0, 4)],
                    min_registered_prices={'data': min_registered_prices},
                )
                product_details.save()


def get_child_category(arr, data, parent):
    category = Category(name=data['name'], icon=data['icon'], active=data['active'], parent=parent)
    category.save()
    if 'children' in data:
        for d in data['children']:
            get_child_category(arr, d, category)
    else:
        arr.append(category)


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        _populate(self)
        self.stdout.write("okay")
