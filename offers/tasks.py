from celery import shared_task


@shared_task()
def add(x=2, y=3):
    z = x + y
    print(f"z={z}")


# TODO: Add task to grab curse dollar/hryvnya and recount prices for offers where only one price from 2
