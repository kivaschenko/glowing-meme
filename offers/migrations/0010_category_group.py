# Generated by Django 4.2.4 on 2023-11-11 17:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("offers", "0009_remove_category_description_category_name_ua"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="group",
            field=models.CharField(max_length=60, null=True),
        ),
    ]
