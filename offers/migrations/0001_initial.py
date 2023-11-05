# Generated by Django 4.2.4 on 2023-11-05 08:08

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AddressDelivery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address_name", models.CharField(max_length=255, null=True)),
                ("address", models.TextField(max_length=500, null=True)),
                (
                    "lat",
                    models.DecimalField(decimal_places=10, max_digits=12, null=True),
                ),
                (
                    "lng",
                    models.DecimalField(decimal_places=10, max_digits=12, null=True),
                ),
                (
                    "geometry_point",
                    django.contrib.gis.db.models.fields.PointField(
                        srid=4326, verbose_name="Location"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Addresses Delivery",
                "db_table": "addresses",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "category_name",
                    models.CharField(
                        help_text="max 120 characters", max_length=120, unique=True
                    ),
                ),
                ("description", models.TextField(max_length=500)),
            ],
            options={
                "ordering": ["category_name"],
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tag_name", models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name="Offer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="name of product widely", max_length=255
                    ),
                ),
                (
                    "type_offer",
                    models.CharField(
                        choices=[("buy", "buy"), ("sell", "sell")], max_length=5
                    ),
                ),
                (
                    "price",
                    models.DecimalField(decimal_places=2, max_digits=8, null=True),
                ),
                ("currency", models.CharField(max_length=3)),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, max_digits=8, null=True),
                ),
                ("measurement", models.CharField(max_length=12)),
                (
                    "terms_delivery",
                    models.CharField(
                        help_text="for example, FCA", max_length=3, null=True
                    ),
                ),
                ("created_at", models.DateField(auto_now=True)),
                ("expired_at", models.DateField(null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "address",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="offers.addressdelivery",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="offers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="offers",
                        to="offers.category",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
