from decimal import Decimal
from datetime import datetime
from typing import Tuple, List
import logging

import requests
from django.conf import settings
from django.db import connection
from django.core.files.base import File, ContentFile
from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import Distance
from django.core.serializers import serialize

from offers.models import Offer, ActualCountry
from accounts.models import Address

logger = logging.Logger(__name__)


# ---------------
# Offers services
def create_new_offer(user_id: int = None, category_id: int = None, type_offer: str = "", price: Decimal = None,
                     currency: str = "", amount: Decimal = None, terms_delivery: str = "", latitude: Decimal = None,
                     longitude: Decimal = None, details: str = ""):
    # TODO: Add logging here
    obj = Offer(author_id=user_id, category_id=category_id, type_offer=type_offer, price=price, currency=currency,
                amount=amount, terms_delivery=terms_delivery,
                latitude=latitude, longitude=longitude, details=details,
                geometry_point=fromstr(f"POINT({longitude} {latitude})", srid=4326))
    obj.save()
    logger.info(f'Created a new Offer: {obj}')
    return obj


def get_offers_by_category_id(category_id: int):
    queryset = Offer.actual.filter(category_id=category_id)
    return queryset


def get_offers_by_type_offer_and_category_id(type_offer: str, category_id: int):
    queryset = Offer.actual.filter(type_offer=type_offer, category_id=category_id, is_active=True)
    return queryset


def get_offers_by_author_id(author_id: int):
    queryset = Offer.objects.filter(author_id=author_id)
    return queryset


def get_offer_by_id(offer_id: int):
    queryset = Offer.objects.get(id=offer_id)
    return queryset


def get_count_offers_by_country_name(country_name: str):
    count = Offer.actual.filter(country=country_name).count()
    return count


def update_actual_country_record(country_name: str, count: int):
    actual_country, _ = ActualCountry.objects.get_or_create(name=country_name)
    actual_country.offers_count = count
    actual_country.save()
    print(f"Updated country {actual_country}")
    logger.info(f'Updated country record for {actual_country}')


def collect_all_unique_country_from_actual_offers():
    records = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT country, COUNT(country) FROM offers GROUP BY country")
        records = cursor.fetchall()
    if len(records):
        for record in records:
            actual_country, _ = ActualCountry.objects.get_or_create(name=record[0])
            actual_country.offers_count = record[1]
            actual_country.save()
            print(f'Updated country record for {actual_country}')
            logger.info(f'Updated country record for {actual_country}')


# ---------------
# Mapbox services
def get_address_from_mapbox(longitude: Decimal, latitude: Decimal, endpoint: str = 'mapbox.places',
                            access_token: str = settings.MAPBOX_ACCESS_TOKEN):
    """Get address from coordinates https://docs.mapbox.com/api/search/geocoding/"""
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
        return {}


def get_offer_address_info_by_coords(longitude: Decimal, latitude: Decimal, offer_id: int):
    try:
        response = get_address_from_mapbox(longitude, latitude)
        logger.info(f"Start getting address for Offer id={offer_id}.")
        offer = Offer.objects.get(id=offer_id)
        offer.address = response['features'][0]['place_name']
        offer.region = response['features'][-2]['text']
        offer.country = response['features'][-1]['text']
        offer.save()
        logger.info(f'Offers address updated successfully: {offer}.')
    except Exception as e:
        logger.exception(f'Occurred error during updating address: {e}.')


def get_static_map_image_from_mapbox(longitude: Decimal, latitude: Decimal,
                                     overlay: str = None,
                                     zoom: Decimal = Decimal(9.0),
                                     bearing: int = 0,
                                     pitch: int = 20,
                                     width: int = 400,
                                     height: int = 400,
                                     access_token: str = settings.MAPBOX_ACCESS_TOKEN,
                                     ):
    """Get static map from coordinates https://docs.mapbox.com/api/maps/static-images/ """
    if overlay is None:
        overlay = f'pin-s+555555({longitude},{latitude})'  # type and style for marker

    url = f"https://api.mapbox.com/styles/v1/kivaschenko/ckhc76knv0dh719m3kngv5z2b/static/{overlay}/{longitude},{latitude},{zoom},{bearing},{pitch}/{width}x{height}"

    params = {"access_token": access_token}
    r = requests.get(url, params=params)
    if r.status_code == 200:
        logger.info(f"Got response: {r.content}")
        return r.content
    else:
        logger.error(f"Failed request: {r.content}")
        return None


def get_offer_static_map_image_by_coords(longitude: Decimal, latitude: Decimal, offer_id: int):
    try:
        r_content = get_static_map_image_from_mapbox(longitude, latitude)
        logger.info(f'Start getting mini map image for Offer id={offer_id}')
        offer = Offer.objects.get(id=offer_id)
        filename = 'minimap_{}.png'.format(offer_id)
        cf = ContentFile(r_content)
        offer.mini_map_img.save(name=filename, content=File(cf))
        offer.save()
        logger.info('Offers mini map updated successfully: %', offer.id)
    except Exception as e:
        logger.exception(f'Occurred error during updating mini map: {e}')
        return


# PostGis

def find_offers_within_radius(longitude: Decimal = None, latitude: Decimal = None, radius_in_meters: int = None,
                              category_id: int = None, type_offer: str = 'sell', min_price: Decimal = Decimal('0.00'),
                              max_price: Decimal = Decimal('1000000.00'), currency: str = 'USD',
                              expired_at: str = None) -> List[Tuple[Decimal, Decimal,]]:
    """example return value:
        [(11, 'sell', Decimal('5300.00'), 'UAH', Decimal('120.00'), 'EXW', 'Ukraine', 'Corn', 'Кукурудза'),
        (12, 'sell', Decimal('4900.00'), 'UAH', Decimal('280.00'), 'EXW', 'Ukraine', 'Corn', 'Кукурудза')]
    """
    if expired_at is None:
        expired_at = datetime.today().strftime('%Y-%m-%d')
    stmt = """
       SELECT offers.id, offers.type_offer, offers.price, offers.currency, offers.amount, 
        offers.terms_delivery, offers.country, offers.longitude, offers.latitude,
        categories.category_name, categories.name_ua
    FROM offers
    LEFT JOIN categories ON offers.category_id=categories.id
    WHERE ST_DWithin(geometry_point, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s)
        AND offers.category_id=%s AND type_offer=%s AND price>=%s AND price<=%s AND currency=%s 
        AND is_active=true AND expired_at >=%s"""
    with connection.cursor() as cursor:
        cursor.execute(stmt, [longitude, latitude, radius_in_meters, category_id, type_offer, min_price, max_price,
                              currency, expired_at])
        records = cursor.fetchall()
    return records


def get_geojson_features_within_radius(longitude, latitude, radius_in_meters: int, category_id: int = None,
                                       type_offer='sell', min_price=Decimal('0.00'), max_price=Decimal('999999.99'),
                                       min_amount=Decimal('0.00'), max_amount=Decimal('999999.99'), currency='USD',
                                       expired_at: str = None):
    if expired_at is None:
        expired_at = datetime.today().strftime('%Y-%m-%d')
    geom = fromstr(f"POINT({longitude} {latitude})", srid=4326)
    queryset = Offer.objects.filter(
        geometry_point__distance_lte=(geom, Distance(m=radius_in_meters))
    ).filter(category_id=category_id, type_offer=type_offer
             ).filter(expired_at__gte=expired_at, currency=currency
                      ).filter(price__gte=min_price, price__lte=max_price
                               ).filter(amount__gte=min_amount, amount__lte=max_amount)
    json_data = serialize("geojson", queryset, geometry_field="geometry_point",
                                   fields=['id', 'type_offer', 'category', 'price', 'currency',
                                           'amount', 'description'])
    return json_data

# -----------------
# Accounts services

def create_new_address(user_id: int = None, address_name: str = None, latitude: Decimal = None,
                       longitude: Decimal = None):
    obj = Address(user_id=user_id, address_name=address_name, latitude=latitude, longitude=longitude,
                  geometry_point=fromstr(f"POINT({longitude} {latitude})", srid=4326))
    obj.save()
    logger.info(f'New Address created with id: {obj.id}')
    return obj


def get_address_data_by_coords(longitude, latitude, address_id):
    try:
        response = get_address_from_mapbox(longitude, latitude)
        logger.info(f'Start getting address for Address id: {address_id}')
        address = Address.objects.get(id=address_id)
        address.address = response['features'][0]['place_name']
        address.region = response['features'][-2]['text']
        address.country = response['features'][-1]['text']
        address.save()
        logger.info(f'Offers address updated successfully: {address}.')
    except Exception as e:
        logger.exception(f'Occurred error during updating address: {e}.')


def get_address_static_map_image_by_coords(longitude: Decimal, latitude: Decimal, address_id: int):
    try:
        r_content = get_static_map_image_from_mapbox(longitude, latitude)
        logger.info(f'Start getting mini map image for Offer id={address_id}')
        address = Address.objects.get(id=address_id)
        filename = 'minimap_{}.png'.format(address_id)
        cf = ContentFile(r_content)
        address.mini_map.save(name=filename, content=File(cf))
        address.save()
        logger.info('Address mini map updated successfully: %', address.id)
    except Exception as e:
        logger.exception(f'Occurred error during updating mini map: {e}')
        return
