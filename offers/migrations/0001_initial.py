# Generated by Django 4.2.4 on 2023-08-22 17:34

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
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='max 60 characters', max_length=60, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='name of product widely', max_length=255)),
                ('type_offer', models.CharField(choices=[('buy', 'buy'), ('sell', 'sell')], max_length=5)),
                ('price_dollar', models.DecimalField(blank=True, decimal_places=2, help_text='price in USD', max_digits=8, null=True)),
                ('price_uah', models.DecimalField(blank=True, decimal_places=2, help_text='price in UAH', max_digits=8, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=3, help_text='amount in metric tonn', max_digits=6, null=True)),
                ('incoterms', models.CharField(choices=[('EXW', 'EXW'), ('FCA', 'FCA'), ('CPT', 'CPT'), ('CIP', 'CIP'), ('DAP', 'DAP'), ('DPU', 'DPU'), ('DDP', 'DDP'), ('FAS', 'FAS'), ('FOB', 'FOB'), ('CFR', 'CFR'), ('CIF', 'CIF')], default='FCA', max_length=3)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('expired_at', models.DateTimeField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Location')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='offers', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='offers.category')),
            ],
            options={
                'ordering': ['-created_at', 'category'],
            },
        ),
    ]
