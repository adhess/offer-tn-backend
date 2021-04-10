import json
import re

file_path = 'conf.json'

settings_file = open(file_path)
settings = json.loads(settings_file.read())

jumia_pc = """
Type systéme d'exploitation : FreeDOS
Type processeur : Intel Core i3-7020U
Mémoire cache : 3 Mo
Couleur : Noir
Garantie 1 an
Fréquence horloge :2.3 Ghz
Processeur : Intel Core i3
Type mémoire : DDR4
Mémoire installée : 4 Go
Capacité : 1 To
Connectique :SATA
Vitesse : 5400 tours/min
Type lecteur optique
Graveur DVD/RW
Type lecteur de supports numériques
Lecteur 4-en-1
LAN
Gigabit Ethernet
Wi-Fi
Bluetooth
Taille écran :15.6
Type écran  : HD TN
Résolution :1920x1080
"""

string_jumia_2 = """
TYPE :   Ordinateur Portable
Systéme d’expolitation : Windows 10 Home
PROCESSEUR     Intel Celeron-Dual Core N4205 Dual 1.8 GHz Cache 2Mo
MEMOIRE: 8gb DDR4 2666mhz
DISQUE: 1Tb (1000GB)
type dd: HDD seagate st1000lm035
Ecran  HD LED 15.6 Pouces 1366 x 768
CARTE GRAPHIQUE        Graphique Intégrée
CONNECTIVITE SANS-FIL              Wi-Fi
Type Carte Graphique             Intel HD Graphics
Connecteurs 2 ports USB 3.1 de 1re génération, 1 port USB 2.0, 1 port HDMI 1.4b, 1 port RJ45, 1 prise jack audio microphone et casque
Couleur Noir
Graveur DVD oui
GARANTIE 1 an
SKU: DE014CL1EZJMONAFAMZ
Couleur: noir
Modèle: Inspiron 15
Gamme de produits: Laptop
Poids (kg): 2.25
"""

string_mytek = """
Référence 81N300LWFG Ecran 15.6" HD LED - Processeur: Dual-Core AMD A6-9225 (2.6 GHz up to 3.0 GHz, Dual-Core) - FreeDos - Mémoire RAM: 4 Go DDR4 - Disque Dur: 1 To - Carte Graphique: Intel HD Graphics avec  Wifi - Couleur: Noir - Garantie: 1 an
"""

string_Mytek_2 = """
GAMER Non SYSTEME D'EXPLOITATION MacOS PROCESSEUR Intel Core i7 Type Processeur Quad-Core Frequence Processeur 2.6 GHz Mémoire Cache 6 Mo Capacité de Batterie jus
qu'à 10 heures d'autonomie Type de Batterie Lithium-Polymère MEMOIRE 16 Go Vitesse Memoire 1600 MHz Type Memoire DDR3 Lecteur de Carte Mémoire carte SD, carte SDHC
, carte SDXC TAILLE DE L'ECRAN 15.4 Pouces Ecran LED HD Résolution Ecran 2880 x 1800 pixels ECRAN TACTILE Non DISQUE DUR 256 Go SSD CARTE GRAPHIQUE AMD Radeon Type
 Disque Dur SSD CONNECTIVITE SANS-FIL Wi-Fi Type Carte Graphique AMD Radeon Pro 450 Audio HP intégrés Connecteurs 4 ports USB 3.1 Type C / Thunderbolt 3 avec prise
 en charge du signal DisplayPort Formats 35,89 x 24,71 x 1,8 cm Bluetooth Bluetooth 4.2 GARANTIE 1 an
  """

string_wiki = """
, Marque, , MSI, , Garantie, , 2 ans, , Processeur , , Intel Core i5, , Fréquence processuer, , 2.5 GHz - 4.5GHz, , Référence Processeur, , Intel Core i5-10300H,
, Mémoire cache, , 8 Mo, , Mémoire Ram, , 16 Go, , Connecteurs, , 1 x Type-C USB 3.2 gen.1 - 3 x Type-A USB 3.2 gen. -1 x RJ45 -1 x HDMI -1 x Entrée micro +1 x Sor
tie casque, , Carte graphique, , NVIDIA GeForce GTX1650 (Max-Q), , Webcam, , oui, , Bluetooth, , Oui, , Connectivité sans fil, , Wifi, , Batterie, , 3 cellules, ,
Type de Batterie, , Li-Polymère / 51 Wh, , Ecran Tactile, , Non, , Type Ecran, , FULL HD, , Poids, , 1.86Kg, , Capacité du disque dur, , 512 Go, , Chipset grap
hique, , NVIDIA GeForce GTX1650 (Max-Q), , Résolution Max, , 1920 x 1080 pixels, , Taux de rafraîchissement , , 144Hz, , Taille d\'écran en pouces, , 15.6", , Type
 de système d\'exploitation, , FreeDos, , Marque, , MSI, , Garantie, , 2 ans, , Processeur , , Intel Core i5, , Fréquence processuer, , 2.5 GHz - 4.5GHz, , Référen
ce Processeur, , Intel Core i5-10300H, , Mémoire cache, , 8 Mo, , Mémoire Ram, , 16 Go, , Connecteurs, , 1 x Type-C USB 3.2 gen.1 - 3 x Type-A USB 3.2 gen. -1 x RJ
45 -1 x HDMI -1 x Entrée micro +1 x Sortie casque, , Carte graphique, , NVIDIA GeForce GTX1650 (Max-Q), , Webcam, , oui, , Bluetooth, , Oui, , Connectivité sans fi
l, , Wifi, , Batterie, , 3 cellules, , Type de Batterie, , Li-Polymère / 51 Wh, , Ecran Tactile, , Non, , Type Ecran, , FULL HD, , Poids, , 1.86Kg, , Capacité du d
isque dur, , 512 Go , , Chipset graphique, , NVIDIA GeForce GTX1650 (Max-Q), , Résolution Max, , 1920 x 1080 pixels, , Taux de rafraîchissement , , 144Hz, , Tai
lle d\'écran en pouces, , 15.6", , Type de système d\'exploitation, , FreeDos"""

wiki2 = """
', Marque, , ASUS, , Garantie, , 1 an, , Processeur , , Intel Core i5, , Type processeur, , Quad core, , Fréquence processuer, , 2.5 GHz up to 4.5 GHz, , Référence
 Processeur, , i5-10300H 10éme Génération, , Mémoire cache, , 8 Mo, , Mémoire Ram, , 16 Go, , Connecteurs, , 1x HDMI 2.0b -1x USB 2.0 Type-A -2x USB 3.2 Gen 1 Type
-A -1x USB 3.2 Gen 2 Type-C -1x prise audio combo 3,5 mm, , Carte graphique, , NVIDIA GeForce GTX 1650Ti 4Go, , Webcam, , oui, , WIFI, , Oui, , Ecran Tactile, , No
n, , Type Ecran, , FULL HD, , Capacité du disque dur, , 512 Go SSD, , Résolution Max, , 1920 x 1080 pixels, , Taille d\'écran en pouces, , 15.6", , Type de système
 d\'exploitation, , Windows, , Marque, , ASUS, , Garantie, , 1 an, , Processeur , , Intel Core i5, , Type processeur, , Quad core, , Fréquence processuer, , 2.5 GH
z up to 4.5 GHz, , Référence Processeur, , i5-10300H 10éme Génération, , Mémoire cache, , 8 Mo, , Mémoire Ram, , 16 Go, , Connecteurs, , 1x HDMI 2.0b -1x USB 2.0 T
ype-A -2x USB 3.2 Gen 1 Type-A -1x USB 3.2 Gen 2 Type-C -1x prise audio combo 3,5 mm, , Carte graphique, , NVIDIA GeForce GTX 1650Ti 4Go, , Webcam, , oui, , WIFI,
, Oui, , Ecran Tactile, , Non, , Type Ecran, , FULL HD, , Capacité du disque dur, , 512 Go SSD, , Résolution Max, , 1920 x 1080 pixels, , Taille d\'écran en pouces
, , 15.6", , Type de système d\'exploitation, , Windows'
"""

wiki3= """
, Marque, , LENOVO, , Garantie, , 1 an, , Processeur , , AMD Ryzen 3, , Type processeur, , Quad core, , Référence Processeur, , AMD Ryzen 3 3200U, , Mémoire cache
, , 4 Mo, , Mémoire Ram, , 4 Go, , Connecteurs, , 2x USB 3.1 Gen 1 -1x HDMI 1.4b - 1x card reader - 1x headphone / microphone combo jack - 1x power connector, , Ca
rte graphique, , AMD Readon, , Ecran Tactile, , oui, , Type Ecran, , FULL HD, , Capacité du disque dur, , 1 Tera, , Type de mémoire, , DDR4, , Chipset graphiqu
e, , AMD Radeon Vega 3, , Résolution Max, , 1920 x 1080 pixels, , Taille d\'écran en pouces, , 14", , Type de système d\'exploitation, , Windows, , Marque, , LENOV
O, , Garantie, , 1 an, , Processeur , , AMD Ryzen 3, , Type processeur, , Quad core, , Référence Processeur, , AMD Ryzen 3 3200U, , Mémoire cache, , 4 Mo, , Mémoir
e Ram, , 4 Go, , Connecteurs, , 2x USB 3.1 Gen 1 -1x HDMI 1.4b - 1x card reader - 1x headphone / microphone combo jack - 1x power connector, , Carte graphique, , A
MD Readon, , Ecran Tactile, , oui, , Type Ecran, , FULL HD, , Capacité du disque dur, , 256 Go SSD, , Type de mémoire, , DDR4, , Chipset graphique, , AMD Radeon Ve
ga 3, , Résolution Max, , 1920 x 1080 pixels, , Taille d\'écran en pouces, , 14", , Type de système d\'exploitation, , Windows"""

wiki4 = """, Marque, , DELL, , Couleur, , Gris, , Garantie, , 1 an, , Processeur , , Intel Core i5, , Fréquence processuer, , jusqu‘à 4,2 GHz, , Référence Processeur, , Inte
l® Core™ i5-1135G7, , Mémoire cache, , 8 Mo, , Mémoire Ram, , 8 Go, , Connecteurs, , Port USB 3.2 Gen 1 Type A - Prise jack combinée pour microphone/casque -Port H
DMI 1.4b -Port USB 3.2 Gen 1 Type A - Port USB 3.2 Gen 1 Type-C, , Carte graphique, , Intel Iris Graphics, , Webcam, , oui, , Ecran Tactile, , oui, , Type Ecran, ,
 FULL HD, , Capacité du disque dur, , 256 Go SSD, , Chipset graphique, , Intel® Iris® Xᵉ, , Résolution Max, , 1920 x 1080 pixels, , Taille d\'écran en pouces, , 14
", , Type de système d\'exploitation, , Windows, , Marque, , DELL, , Couleur, , Gris, , Garantie, , 1 an, , Processeur , , Intel Core i5, , Fréquence processuer, ,
 jusqu‘à 4,2 GHz, , Référence Processeur, , Intel® Core™ i5-1135G7, , Mémoire cache, , 8 Mo, , Mémoire Ram, , 8 Go, , Connecteurs, , Port USB 3.2 Gen 1 Type A - Pr
ise jack combinée pour microphone/casque -Port HDMI 1.4b -Port USB 3.2 Gen 1 Type A - Port USB 3.2 Gen 1 Type-C, , Carte graphique, , Intel Iris Graphics, , Webcam
, , oui, , Ecran Tactile, , oui, , Type Ecran, , FULL HD, , Capacité du disque dur, , 256 Go SSD, , Chipset graphique, , Intel® Iris® Xᵉ, , Résolution Max, , 1920
x 1080 pixels, , Taille d\'écran en pouces, , 14", , Type de système d\'exploitation, , Windows"""

wiki5 = """, Marque, , ASUS, , Couleur, , Gris, , Garantie, , 1 an, , Processeur , , Intel Celeron, , Fréquence processuer, , 1.10 GHz Up to 2.80 GHz, , Référence Processeur
, , Intel Celeron N4020, , Mémoire cache, , 4 Mo, , Mémoire Ram, , 8 Go, , Connecteurs, , 1 port USB Type-C® SuperSpeed, 2 ports USB Type-A SuperSpeed, 1 port HDMI
 1.4b, 1 port RJ-45, 1 prise secteur Smart Pin, 1 prise combinée casque/microphone, , Carte graphique, , Graphique Intégrée, , Bluetooth, , Oui, , Connectivité san
s fil, , Wifi, , Batterie, , 2 cellules, , Ecran Tactile, , Non, , Type Ecran, , HD, , Capacité du disque dur, , 1 Téra, , Chipset graphique, , Intel HD Graphics,
, Résolution Max, , 1366 x 768 pixels, , Taille d\'écran en pouces, , 15.6", , Type de système d\'exploitation, , FreeDos, , Marque, , ASUS, , Couleur, , Gris, , G
arantie, , 1 an, , Processeur , , Intel Celeron, , Fréquence processuer, , 1.10 GHz Up to 2.80 GHz, , Référence Processeur, , Intel Celeron N4020, , Mémoire cache,
 , 4 Mo, , Mémoire Ram, , 8 Go, , Connecteurs, , 1 port USB Type-C® SuperSpeed, 2 ports USB Type-A SuperSpeed, 1 port HDMI 1.4b, 1 port RJ-45, 1 prise secteur Smar
t Pin, 1 prise combinée casque/microphone, , Carte graphique, , Graphique Intégrée, , Bluetooth, , Oui, , Connectivité sans fil, , Wifi, , Batterie, , 2 cellules,
, Ecran Tactile, , Non, , Type Ecran, , HD, , Capacité du disque dur, , 1 Téra, , Chipset graphique, , Intel HD Graphics, , Résolution Max, , 1366 x 768 pixels, ,
Taille d\'écran en pouces, , 15.6", , Type de système d\'exploitation, , FreeDos"""


wiki6 = """
, Marque, , MSI, , Garantie, , 2 ans, , Processeur , , Intel Core i7, , Type processeur, , Hexa core, , Fréquence processuer, , 2.6GHz up to 5 GHz, , Référence Pr
ocesseur, , Intel i7-10750H, , Mémoire cache, , 12Mo, , Mémoire Ram, , 32 Go, , Connecteurs, , 1 X USB 3.0 Type C - 3 X USB 3.0 - 1 X RJ45, , Carte graphique, , Nvidia GeForce RTX3060 max-q, , Webcam, , oui, , Bluetooth, , Oui, , Connectivité sans fil, , Wifi, , Ecran Tactile, , Non, , Type Ecran, , FULL HD, , Capacité du disque d
ur, , 1 Téra, , Résolution Max, , 1920 x 1080 pixels, , Taux de rafraîchissement , , 144Hz, , Taille d\'écran en pou
ces, , 17.3", , Type de système d\'exploitation, , FreeDos, , Marque, , MSI, , Garantie, , 2 ans, , Processeur , , Intel Core i7, , Type processeur, , Hexa core, ,
 Fréquence processuer, , 2.6GHz up to 5 GHz, , Référence Processeur, , Intel i7-10750H, , Mémoire cache, , 12Mo, , Mémoire Ram, , 32 Go, , Connecteurs, , 1 X USB 3
.0 Type C - 3 X USB 3.0 - 1 X RJ45, , Carte graphique, , Webcam, , oui, , Bluetooth, , Oui, , Connectivité sans fil, , Wifi, , Ecran Tact
ile, , Non, , Type Ecran, , FULL HD, , Capacité du disque dur, , 1 Téra, , Chipset graphique, , Résolution Max, , 1920 x 1080 pixels, , T
aux de rafraîchissement , , 144Hz, , Taille d\'écran en pouces, , 17.3", , Type de système d\'exploitation, , FreeDos
"""

wiki7 = """
, Marque, , LENOVO, , Garantie, , 1 an, , Processeur , , AMD, , Fréquence processuer, , 1,2 / 2,6 GHz, , Référence Processeur, , AMD 3020e, , Mémoire cache, , 4 M
o, , Mémoire Ram, , 4 Go, , Connecteurs, , 1 port USB 2.0 -2 ports USB 3.1 -1 x HDMI -1x lecteur de carte -1x prise combo casque / microphone –1x connecteur d\'ali
mentation, , Carte graphique, , AMD Readon, , Webcam, , oui, , Bluetooth, , v 4.2, , Connectivité sans fil, , Wifi, , Ecran Tactile, , Non, , Type Ecran, , HD, , C
apacité du disque dur, , 1 Téra, , Chipset graphique, , AMD Radeon Intégréé, , Résolution Max, , 1366 x 768 pixels, , Taille d\'écran en pouces, , 15.6", , Type de
 système d\'exploitation, , FreeDos, , Marque, , LENOVO, , Garantie, , 1 an, , Processeur , , AMD, , Fréquence processuer, , 1,2 / 2,6 GHz, , Référence Processeur,
 , AMD 3020e, , Mémoire cache, , 4 Mo, , Mémoire Ram, , 4 Go, , Connecteurs, , 1 port USB 2.0 -2 ports USB 3.1 -1 x HDMI -1x lecteur de carte -1x prise combo casqu
e / microphone –1x connecteur d\'alimentation, , Carte graphique, , AMD Readon, , Webcam, , oui, , Bluetooth, , v 4.2, , Connectivité sans fil, , Wifi, , Ecran Tac
tile, , Non, , Type Ecran, , HD, , Capacité du disque dur, , 1 Téra, , Chipset graphique, , AMD Radeon Intégréé, , Résolution Max, , 1366 x 768 pixels, , Taille d\
'écran en pouces, , 15.6", , Type de système d\'exploitation, , FreeDos"""

for element, element_format in settings['LaptopItem'].items():
    out = f"{element}: "
    for i, pattern in enumerate(element_format['patterns']):
        cp = re.compile(pattern, re.IGNORECASE)
        curr_match = cp.search(wiki7)
        if curr_match:
            out += element_format['formats'][i].format(*(curr_match.groups()))
            break
    print(out)