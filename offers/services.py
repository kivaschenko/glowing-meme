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
    logger.info(f'Start getting address by coords: {longitude}, {latitude}')
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


def get_static_map_image_by_coords(username: str = 'mapbox',
                                   style_id: str = 'light-v11',
                                   overlay: str = None,
                                   longitude: Decimal = None,
                                   latitude: Decimal = None,
                                   zoom: Decimal = Decimal(5.5),
                                   bearing: int = 0,
                                   pitch: int = 20,
                                   width: int = 360,
                                   height: int = 360,
                                   access_token: str = settings.MAPBOX_ACCESS_TOKEN,
                                   ):
    if overlay is None:
        overlay = f'pin-s+555555({longitude},{latitude})'

    url = f"https://api.mapbox.com/styles/v1/{username}/{style_id}/static/{overlay}/{longitude},{latitude},{zoom},{bearing},{pitch}/{width}x{height}"

    params = {"access_token": access_token}
    r = requests.get(url, params=params)
    if r.status_code == 200:
        logger.info(f"Got response: {r.content}")
        return r.content
    else:
        logger.error(f"Failed request: {r.content}")
        return None
