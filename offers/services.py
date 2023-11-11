from decimal import Decimal
from .models import Offer


def create_new_offer(
    category_id: int = None,
    type_offer: str = "",
    price: Decimal = None,
    currency: str = "",
    amount: Decimal = None,
    terms_delivery: str = "",
    latitude: Decimal = None,
    longitude: Decimal = None,
    details: str = ""
):
    # TODO: Add logging here
    obj = Offer(
        category_id=category_id,
        price=price,
        currency=currency,
        amount=amount,
        terms_delivery=terms_delivery,
        latitude=latitude,
        longitude=longitude,
        details=details
    )
    obj.save()
    print(f'Created a new Offer: {obj}')