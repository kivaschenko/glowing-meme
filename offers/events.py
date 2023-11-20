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
