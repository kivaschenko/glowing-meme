from typing import Type

from offers import events, tasks, services

base_event = Type[events.Event]


def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)


# ---------------
# NewOfferCreated
def update_address(event: events.NewOfferCreated):
    # tasks.get_address_from_coordinates.delay(event.longitude, event.latitude, event.offer_id)
    services.get_address_info_by_coords(event.longitude, event.latitude, event.offer_id)


def update_mini_map(event: events.NewOfferCreated):
    tasks.get_mini_map_image_from_coordinates.delay(event.longitude, event.latitude, event.offer_id)
    # services.get_static_map_image_by_coords(event.longitude, event.latitude, event.offer_id)


def update_actual_country_count(event: events.NewOfferCreated):
    print(f"Received event: {event}")
    tasks.update_actual_country_count_for_new_offer.delay(event.offer_id)


def send_notification(event: events.Event):
    pass


HANDLERS = {
    events.NewOfferCreated: [
        update_address,
        update_mini_map,
        update_actual_country_count,
        send_notification,
    ],
}
