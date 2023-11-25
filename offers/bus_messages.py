from typing import Type

from offers import events, tasks

base_event = Type[events.Event]


def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)


# ---------------
# NewOfferCreated
def update_address(event: events.NewOfferCreated):
    tasks.get_address_from_coordinates.delay(event.longitude, event.latitude, event.offer_id)


def update_mini_map(event: events.NewOfferCreated):
    tasks.get_mini_map_image_from_coordinates.delay(event.longitude, event.latitude, event.offer_id)


def send_notification(event: events.Event):
    pass


HANDLERS = {
    events.NewOfferCreated: [
        update_address,
        update_mini_map,
        send_notification,
    ],
}
