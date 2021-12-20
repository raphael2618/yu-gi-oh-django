import os
import random
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yugioh_django_proj.settings')
django.setup()

# After setup()
from trading_cards.models import Card

# url = 'https://db.ygoprodeck.com/api/v7/randomcard.php'
url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
response = requests.get(url)
cards = response.json()['data']

i = 0
for card in cards:
    card = Card.objects.create(
        yugioh_id=card['id'],
        name=card['name'],
        img_small=card['card_images'][0]['image_url_small'],
        img=card['card_images'][0]['image_url'],
        desc=card['desc'],
    )
    print(card)
    i += 1
    if i == 200:
        break

# for card in cards:
#     print(card['name'])
#     i += 1
#     if i == 10:
#         break
# todo: add a new model for atk def level ONLY FOR MOSTERS if revelent (YES OR NO?)
