from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.contrib.gis.db import models


class Category(models.Model):
    # TODO: Add slug field
    category_name = models.CharField(
        max_length=120, unique=True, help_text="max 120 characters"
    )
    description = models.TextField(max_length=500)

    class Meta:
        ordering = ["category_name"]

    def __str__(self):
        return f"{self.category_name}"


class AddressDelivery(models.Model):
    address = models.TextField(max_length=500, null=True)
    country = models.CharField(max_length=255, null=True)
    geometry_point = models.PointField(verbose_name="Location", srid=4326)

    def __repr__(self):
        return f"<AddressDelivery(id={self.id} address={self.address} lat={self.lat} lng={self.lng} geometry_point={self.geometry_point})>"

    def __str__(self):
        return f"{self.address}"

    class Meta:
        db_table = "addresses"
        verbose_name_plural = "Addresses Delivery"


class ActualOffers(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(is_active=True)
            .filter(expired_at__lt=datetime.now())
        )


class Offer(models.Model):
    # author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="offers")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="offers"
    )
    title = models.CharField(max_length=255, help_text="name of product widely")
    type_offer = models.CharField(
        max_length=5, choices=(("buy", "buy"), ("sell", "sell"))
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    terms_delivery = models.CharField(
        max_length=3, help_text="for example, FCA", null=True
    )
    created_at = models.DateField(auto_now=True)
    expired_at = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    latitude = models.DecimalField(max_digits=18, decimal_places=16, null=True)
    longitude = models.DecimalField(max_digits=18, decimal_places=16, null=True)
    address = models.ForeignKey("AddressDelivery", on_delete=models.SET_NULL, null=True)

    objects = models.Manager()
    actual = ActualOffers()  # offers where expired datetime less or equal now

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"<Offer(id={self.id} title={self.title}...)>"

    def save(self, *args, **kwargs):
        self.expired_at = datetime.now() + timedelta(days=30)
        super().save(*args, **kwargs)
