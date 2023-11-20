from decimal import Decimal
import logging

import requests
from django.conf import settings
from django.core.files.base import File, ContentFile
from django.contrib.gis.geos import fromstr

from .models import Offer

logger = logging.Logger(__name__)


# ---------------
# Offers services
def create_new_offer(user_id: int = None, category_id: int = None, type_offer: str = "", price: Decimal = None, currency: str = "",
                     amount: Decimal = None, terms_delivery: str = "", latitude: Decimal = None, longitude: Decimal = None, details: str = ""):
    # TODO: Add logging here
    obj = Offer(author_id=user_id, category_id=category_id, type_offer=type_offer, price=price, currency=currency, amount=amount, terms_delivery=terms_delivery,
                latitude=latitude, longitude=longitude, details=details, geometry_point=fromstr(f'POINT({longitude} {latitude})', srid=4326))
    obj.save()
    logger.info(f'Created a new Offer: {obj}')
    return obj


# ---------------
# Mapbox services
def get_address_info_by_coords(longitude: Decimal, latitude: Decimal, offer_id: int, endpoint: str = 'mapbox.places',
                               access_token: str = settings.MAPBOX_ACCESS_TOKEN):
    """Get address from coordinates https://docs.mapbox.com/api/search/geocoding/"""
    logger.info(f'Start getting address by coords: {longitude}, {latitude}')
    url = f"https://api.mapbox.com/geocoding/v5/{endpoint}/{longitude},{latitude}.json"
    params = {"access_token": access_token}
    r = requests.get(url, params=params)
    if r.status_code == 200:
        response = r.json()
        logger.info(f"Got response: {response}")
    else:
        logger.error(f"Failed request: {r.content}")
        return
    try:
        logger.info(f"Start getting address for Offer id={offer_id}.")
        offer = Offer.objects.get(id=offer_id)
        offer.address = response['features'][0]['place_name']
        offer.country = response['features'][-1]['text']
        offer.save()
        logger.info(f'Offers address updated successfully: {offer}.')
    except Exception as e:
        logger.exception(f'Occurred error during updating address: {e}.')


def get_static_map_image_by_coords(longitude: Decimal, latitude: Decimal, offer_id: int,
                                   style_id: str = 'light-v11',
                                   overlay: str = None,
                                   zoom: Decimal = Decimal(5.5),
                                   bearing: int = 0,
                                   pitch: int = 20,
                                   width: int = 360,
                                   height: int = 360,
                                   access_token: str = settings.MAPBOX_ACCESS_TOKEN,
                                   ):
    """Get static map from coordinates https://docs.mapbox.com/api/maps/static-images/ """
    if overlay is None:
        overlay = f'pin-s+555555({longitude},{latitude})'  # type and style for marker

    url = f"https://api.mapbox.com/styles/v1/mapbox/{style_id}/static/{overlay}/{longitude},{latitude},{zoom},{bearing},{pitch}/{width}x{height}"

    params = {"access_token": access_token}
    r = requests.get(url, params=params)
    if r.status_code == 200:
        logger.info(f"Got response: {r.content}")
    else:
        logger.error(f"Failed request: {r.content}")
        return
    try:
        logger.info(f'Start getting mini map image for Offer id={offer_id}')
        offer = Offer.objects.get(id=offer_id)
        filename = 'minimap_{}.png'.format(offer_id)
        cf = ContentFile(r.content)
        offer.mini_map_img.save(name=filename, content=File(cf))
        offer.save()
        logger.info('Offers mini map updated successfully: %', offer.id)
    except Exception as e:
        logger.exception(f'Occurred error during updating mini map: {e}')
        return
