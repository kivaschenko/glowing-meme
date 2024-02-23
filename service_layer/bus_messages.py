from typing import Type

from service_layer import events, services, tasks

base_event = Type[events.Event]


def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)


# ---------------
# NewOfferCreated
def update_offer_address(event: events.NewOfferCreated):
    tasks.get_address_from_coordinates_for_new_offer.delay(event.longitude, event.latitude, event.offer_id)


def update_offer_mini_map(event: events.NewOfferCreated):
    tasks.get_mini_map_image_from_coordinates_for_new_offer.delay(event.longitude, event.latitude, event.offer_id)


def update_actual_country_count(event: events.NewOfferCreated):
    tasks.update_actual_country_count_for_new_offer.delay(event.offer_id)


# -----------------
# NewAddressCreated
def update_address_data(event: events.NewAddressCreated):
    services.get_address_data_by_coords(event.longitude, event.latitude, event.address_id)


def update_address_mini_map(event: events.NewAddressCreated):
    tasks.get_mini_map_image_from_coordinates_for_new_address.delay(event.longitude, event.latitude, event.address_id)


def send_notification(event: events.Event):
    pass


HANDLERS = {
    events.NewOfferCreated: [
        update_offer_address,
        update_offer_mini_map,
        update_actual_country_count,
        # send_notification,
    ],
    events.NewAddressCreated: [
        update_address_data,
        update_address_mini_map,
    ]
}
