from django.contrib import admin
from .models import Category, Offer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    pass
