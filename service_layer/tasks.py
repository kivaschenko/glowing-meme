import logging
from decimal import Decimal

from celery import shared_task

logger = logging.Logger(__name__)


@shared_task()
def add(x=2, y=3):
    z = x + y
    print(f"z={z}")


# TODO: Add task to grab curse dollar/hryvnia and recount prices for offers where only one price from 2


@shared_task()
def get_address_from_coordinates_for_new_offer(longitude: Decimal, latitude: Decimal, offer_id: int):
    from service_layer.services import get_offer_address_info_by_coords
    get_offer_address_info_by_coords(longitude, latitude, offer_id)


@shared_task()
def get_mini_map_image_from_coordinates_for_new_offer(longitude: Decimal, latitude: Decimal, offer_id: int):
    from service_layer.services import get_offer_static_map_image_by_coords
    get_offer_static_map_image_by_coords(longitude, latitude, offer_id)


@shared_task()
def update_actual_country_count_for_new_offer(offer_id: int):
    from service_layer import services
    country_name = services.get_offer_by_id(offer_id).country
    count = services.get_count_offers_by_country_name(country_name)
    services.update_actual_country_record(country_name, count)


@shared_task()
def update_actual_country_for_all_offers():
    from service_layer.services import collect_all_unique_country_from_actual_offers
    collect_all_unique_country_from_actual_offers()


@shared_task()
def get_address_info_by_coords_for_new_address(longitude: Decimal, latitude: Decimal, address_id: int):
    from service_layer.services import get_address_data_by_coords
    get_address_data_by_coords(longitude, latitude, address_id)


@shared_task()
def get_mini_map_image_from_coordinates_for_new_address(longitude: Decimal, latitude: Decimal, address_id: int):
    from service_layer.services import get_address_static_map_image_by_coords
    get_address_static_map_image_by_coords(longitude, latitude, address_id)
