from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import CategorySerializer, OfferSerializer
from .models import Category, Offer


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    queryset = Category.objects.all()


class OfferViewSet(ModelViewSet):
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]
    queryset = Offer.objects.all()
