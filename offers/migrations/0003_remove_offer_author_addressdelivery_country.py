# Generated by Django 4.2.4 on 2023-11-07 05:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("offers", "0002_delete_tag"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="offer",
            name="author",
        ),
        migrations.AddField(
            model_name="addressdelivery",
            name="country",
            field=models.CharField(max_length=255, null=True),
        ),
    ]