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

for element, element_format in settings.items():
    for i, pattern in enumerate(element_format['patterns']):
        cp = re.compile(pattern)
        curr_match = cp.search(string_Mytek_2)
        if curr_match:
            result = element_format['formats'][i].format(*(curr_match.groups()))
            print(element + ' : ' + result)
            break
