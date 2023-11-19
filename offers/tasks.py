import logging
from decimal import Decimal

from celery import shared_task

from django.conf import settings


logger = logging.Logger(__name__)

@shared_task()
def add(x=2, y=3):
    z = x + y
    print(f"z={z}")


# TODO: Add task to grab curse dollar/hryvnya and recount prices for offers where only one price from 2


@shared_task()
def get_address_from_coordinates(longitude: Decimal, latitude: Decimal, offer_id: int):
    from .services import get_address_info_by_coords
    from .models import Offer
    try:
        logger.info(f"Start getting address for Offer id={offer_id}.")
        offer = Offer.objects.get(id=offer_id)
        response = get_address_info_by_coords(longitude, latitude)
        offer.address = response['features'][0]['place_name']
        offer.country = response['features'][-1]['text']
        offer.save()
        logger.info(f'Offers address updated successfully: {offer}.')
    except Exception as e:
        logger.exception(f'Occurred error during updating address: {e}.')


@shared_task()
def get_mini_map_image_from_coordinates(longitude: Decimal, latitude: Decimal, offer_id: int):
    from .services import get_static_map_image_by_coords
    from .models import Offer
    from django.core.files.base import File, ContentFile
    try:
        logger.info(f'Start getting mini map image for Offer id={offer_id}')
        offer = Offer.objects.get(id=offer_id)
        filename = 'minimap_{}.png'.format(offer_id)
        response_content = get_static_map_image_by_coords(longitude=longitude, latitude=latitude)
        cf = ContentFile(response_content)
        offer.mini_map_img.save(name=filename, content=File(cf))
        offer.save()
        logger.info('Offers mini map updated successfully: %', offer.id)
    except Exception as e:
        logger.exception(f'Occurred error during updating mini map: {e}')
