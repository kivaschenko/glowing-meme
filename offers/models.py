import logging
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.contrib.gis.db import models

logger = logging.Logger(__name__)


class Category(models.Model):
    # TODO: Add slug field
    category_name = models.CharField(max_length=120, unique=True, help_text="max 120 characters")
    name_ua = models.CharField(max_length=120, null=True)
    group = models.CharField(max_length=60, null=True)

    class Meta:
        db_table = 'categories'
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
    # TODO add slug field
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
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    details = models.CharField(max_length=255, null=True, blank=True)
    # geometry location
    geometry_point = models.PointField(verbose_name="Location", srid=4326)
    address = models.TextField(max_length=500, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    # images
    mini_map_img = models.FileField(upload_to='offer_static_maps', null=True, blank=True)

    objects = models.Manager()
    actual = ActualOffers()  # offers where expired datetime less or equal now

    # mapbox popup
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'offers'
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.category}"

    def __repr__(self):
        return f"<Offer(id={self.id} title={self.category}...)>"

    def get_popup_description_for_map(self, *args, **kwargs):
        html_source = (f"<h6>{self.type_offer.upper()} {self.category.category_name}</h6>"
                       f"<p>Price: {self.price} {self.currency}</p>"
                       f"<p>Amount: {self.amount} metric tonn</p>"
                       f"<p>Terms Delivery: {self.terms_delivery}</p>")
        return html_source

    def save(self, *args, **kwargs):
        self.expired_at = datetime.now() + timedelta(days=30)
        self.description = self.get_popup_description_for_map()
        super().save(*args, **kwargs)


class ActualCountry(models.Model):
    name = models.CharField(max_length=255, unique=True)
    offers_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']
        db_table = 'actual_countries'

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"<ActualCountry(name={self.name}, offers_count={self.offers_count})>"
