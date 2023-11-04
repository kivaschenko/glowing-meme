from rest_framework.serializers import ModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Category, Offer

class OfferSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'
        geo_field = 'location'

class CategorySerializer(ModelSerializer):
    # offers = OfferSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['name', 'offers']

