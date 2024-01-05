from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from accounts.models import Profile, Interest, Address

admin.site.register(Profile)
admin.site.register(Interest)


@admin.register(Address)
class AddressAdmin(OSMGeoAdmin):
    default_lat = 6350000
    default_lon = 3570000
    default_zoom = 6
    # ...
