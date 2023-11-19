from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.files.storage import storages, default_storage

from .tasks import get_address_from_coordinates, get_mini_map_image_from_coordinates


def select_storages():
    if settings.DEBUG:
        return default_storage
    else:
        return storages.get('digital_ocean')


class Category(models.Model):
    # TODO: Add slug field
    category_name = models.CharField(max_length=120, unique=True, help_text="max 120 characters")
    name_ua = models.CharField(max_length=120, null=True)
    group = models.CharField(max_length=60, null=True)

    class Meta:
        ordering = ["group", "category_name"]

    def __str__(self):
        return f"{self.category_name} ({self.name_ua})"


class ActualOffers(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(is_active=True)
            .filter(expired_at__gte=datetime.now())
        )


class Offer(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="offers")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="offers"
    )
    type_offer = models.CharField(
        max_length=5, choices=(("buy", "buy"), ("sell", "sell"))
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    terms_delivery = models.CharField(max_length=3, help_text="for example, FCA", null=True)
    created_at = models.DateField(auto_now=True)
    expired_at = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    latitude = models.DecimalField(max_digits=18, decimal_places=16, null=True, blank=True)
    longitude = models.DecimalField(max_digits=18, decimal_places=16, null=True, blank=True)
    details = models.CharField(max_length=255, null=True, blank=True)
    # geometry location
    geometry_point = models.PointField(verbose_name="Location", srid=4326)
    address = models.TextField(max_length=500, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    # images
    mini_map_img = models.FileField(upload_to='offer_static_maps', storage=select_storages, null=True)

    objects = models.Manager()
    actual = ActualOffers()  # offers where expired datetime less or equal now

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.category}"

    def __repr__(self):
        return f"<Offer(id={self.id} title={self.category}...)>"

    def save(self, *args, **kwargs):
        self.expired_at = datetime.now() + timedelta(days=30)
        super().save(*args, **kwargs)


@receiver(post_save, sender=Offer, dispatch_uid="update_address_minimap_from_mapbox")
def add_address_and_mini_map(sender, instance, **kwargs):
    if not instance.address:
        get_address_from_coordinates.delay(instance.longitude, instance.latitude, instance.id)
    if not instance.mini_map_img.name:
        get_mini_map_image_from_coordinates.delay(instance.longitude, instance.latitude, instance.id)
