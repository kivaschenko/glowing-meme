from decimal import Decimal
import requests
from django.conf import settings
from django.contrib.gis.geos import fromstr

from .models import Offer


def create_new_offer(user_id: int = None, category_id: int = None, type_offer: str = "", price: Decimal = None, currency: str = "",
                     amount: Decimal = None, terms_delivery: str = "", latitude: Decimal = None, longitude: Decimal = None, details: str = ""):
    # TODO: Add logging here
    obj = Offer(author_id=user_id, category_id=category_id, type_offer=type_offer, price=price, currency=currency, amount=amount, terms_delivery=terms_delivery,
                latitude=latitude, longitude=longitude, details=details, geometry_point=fromstr(f'POINT({longitude} {latitude})', srid=4326))
    obj.save()
    print(f'Created a new Offer: {obj}')


def get_address_info_by_coords(endpoint: str = 'mapbox.places', longitude: Decimal = None, latitude: Decimal = None,
                               access_token: str = settings.MAPBOX_ACCESS_TOKEN):
    url = f"https://api.mapbox.com/geocoding/v5/{endpoint}/{longitude},{latitude}.json?access_token={access_token}"