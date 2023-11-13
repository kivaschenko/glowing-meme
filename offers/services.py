from decimal import Decimal
import logging

import requests
from django.conf import settings
from django.contrib.gis.geos import fromstr

from .models import Offer


logger = logging.Logger(__name__)


def create_new_offer(user_id: int = None, category_id: int = None, type_offer: str = "", price: Decimal = None, currency: str = "",
                     amount: Decimal = None, terms_delivery: str = "", latitude: Decimal = None, longitude: Decimal = None, details: str = ""):
    # TODO: Add logging here
    obj = Offer(author_id=user_id, category_id=category_id, type_offer=type_offer, price=price, currency=currency, amount=amount, terms_delivery=terms_delivery,
                latitude=latitude, longitude=longitude, details=details, geometry_point=fromstr(f'POINT({longitude} {latitude})', srid=4326))
    obj.save()
    logger.info(f'Created a new Offer: {obj}')


def get_address_info_by_coords(longitude: Decimal, latitude: Decimal, endpoint: str = 'mapbox.places',
                               access_token: str = settings.MAPBOX_ACCESS_TOKEN):
    url = f"https://api.mapbox.com/geocoding/v5/{endpoint}/{longitude},{latitude}.json"
    params = {"access_token": access_token}
    r = requests.get(url, params=params)
    if r.status_code == 200:
        response = r.json()
        logger.info(f"Got response: {response}")
        return response
    else:
        logger.error(f"Failed request: {r.content}")
        return None
