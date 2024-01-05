from rest_framework.serializers import ModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Category, Offer


class OfferSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"
        geo_field = "geometry_point"


class CategorySerializer(ModelSerializer):
    offers = OfferSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["category_name", "offers"]
