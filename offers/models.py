from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.contrib.gis.db import models


class Category(models.Model):
    name = models.CharField(max_length=60, unique=True, help_text='max 60 characters')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)


class ActualOffers(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).filter(expired_at__lt=datetime.now())


class Offer(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="offers")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="offers")
    title = models.CharField(max_length=255, help_text='name of product widely')
    type_offer = models.CharField(max_length=5, choices=(("buy", "buy"), ("sell", "sell")))
    price_dollar = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="price in USD")
    price_uah = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="price in UAH")
    amount = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True, help_text="amount in metric tonn")
    incoterms = models.CharField(max_length=3, default="FCA",
                                 choices=(
                                     ("EXW", "EXW"),
                                     ("FCA", "FCA"),
                                     ("CPT", "CPT"),
                                     ("CIP", "CIP"),
                                     ("DAP", "DAP"),
                                     ("DPU", "DPU"),
                                     ("DDP", "DDP"),
                                     ("FAS", "FAS"),
                                     ("FOB", "FOB"),
                                     ("CFR", "CFR"),
                                     ("CIF", "CIF"),
                                 ))
    created_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    location = models.PointField(verbose_name='Location', srid=4326)

    objects = models.Manager()
    actual = ActualOffers()  # offers where expired datetime less or equal now

    class Meta:
        ordering = ["-created_at", "category"]

    def __str__(self):
        return f'{self.title} {self.amount} ${self.price_dollar} {self.incoterms}'

    def save(self, *args, **kwargs):
        self.expired_at = datetime.now() + timedelta(days=30)
        super().save(*args, **kwargs)
