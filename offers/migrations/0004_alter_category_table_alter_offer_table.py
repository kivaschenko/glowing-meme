# Generated by Django 4.2.4 on 2024-01-15 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0003_alter_actualcountry_name'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='category',
            table='categories',
        ),
        migrations.AlterModelTable(
            name='offer',
            table='offers',
        ),
    ]