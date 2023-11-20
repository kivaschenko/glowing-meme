import logging
from decimal import Decimal

from celery import shared_task

from django.conf import settings


logger = logging.Logger(__name__)


@shared_task()
def add(x=2, y=3):
    z = x + y
    print(f"z={z}")


# TODO: Add task to grab curse dollar/hryvnia and recount prices for offers where only one price from 2


@shared_task()
def get_address_from_coordinates(longitude: Decimal, latitude: Decimal, offer_id: int):
    from .services import get_address_info_by_coords
    get_address_info_by_coords(longitude, latitude, offer_id)


@shared_task()
def get_mini_map_image_from_coordinates(longitude: Decimal, latitude: Decimal, offer_id: int):
    from offers.services import get_static_map_image_by_coords
    get_static_map_image_by_coords(longitude, latitude, offer_id)
