from rest_framework import routers
from django.urls import path

from .api import CategoryListView, OfferViewSet


router = routers.DefaultRouter()
router.register(r"offers", OfferViewSet, basename="offers")
urlpatterns = router.urls

app_name = "offers"

urlpatterns += [
    path("categories/", CategoryListView.as_view(), name="categories"),
]
