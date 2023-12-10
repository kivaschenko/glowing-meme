from rest_framework.serializers import ModelSerializer

from .models import Category, Offer


class OfferSerializer(ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"


class CategorySerializer(ModelSerializer):
    offers = OfferSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["category_name", "offers"]
