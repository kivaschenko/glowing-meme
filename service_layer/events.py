from decimal import Decimal
from typing import List
from dataclasses import dataclass


@dataclass
class Event:
    pass


@dataclass
class NewOfferCreated(Event):
    longitude: Decimal
    latitude: Decimal
    offer_id: int


@dataclass
class NewAddressCreated(Event):
    longitude: Decimal
    latitude: Decimal
    address_id: int
