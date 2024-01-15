"""
URL configuration for refactored_graintrade project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers, serializers, viewsets

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# monolith urls
from offers.views import (
    HomeView,
    OffersListView,
    CreateOfferView,
    OfferDetailView,
    CategoryListView,
    CategoryDetailView,
    SearchResultsView,
)
from accounts.views import (
    RegistrationView,
    ProfileUpdateView,
    ProfileDetailView,
)
from offers.urls import urlpatterns as offer_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", HomeView.as_view(), name="home"),
    path("accounts/signup/", RegistrationView.as_view(), name='signup'),
    path("accounts/update-profile/<int:pk>/", ProfileUpdateView.as_view(), name='update-profile'),
    path("accounts/profile/<int:user_id>/", ProfileDetailView.as_view(), name='profile'),
    # offers
    path("offers-list/", OffersListView.as_view(), name="offers-list"),
    path("create-offer/", CreateOfferView.as_view(), name="create-offer"),
    path("offer-details/<int:pk>/", OfferDetailView.as_view(), name="offer-details"),
    path("search-results/", SearchResultsView.as_view(), name="search"),
    # categories
    path("categories-list/", CategoryListView.as_view(), name="categories-list"),
    path("category-detail/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("accounts/", include("django.contrib.auth.urls")),
    # built-in path's:
    # accounts/login/ [name='login']
    # accounts/logout/ [name='logout']
    # accounts/password_change/ [name='password_change']
    # accounts/password_change/done/ [name='password_change_done']
    # accounts/password_reset/ [name='password_reset']
    # accounts/password_reset/done/ [name='password_reset_done']
    # accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # accounts/reset/done/ [name='password_reset_complete']
]

urlpatterns += [
    # YOUR PATTERNS
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "apidoc/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    path("api/v1/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

# Offers API
urlpatterns += offer_urlpatterns



urlpatterns += [
    path("accounts/signup/", RegistrationView.as_view(), name='signup'),
    path("accounts/update-profile/<int:pk>/", ProfileUpdateView.as_view(), name='update-profile'),
    path("accounts/profile/<int:user_id>/", ProfileDetailView.as_view(), name='profile'),
    # offers
    path("offers-list/", OffersListView.as_view(), name="offers-list"),
    path("create-offer/", CreateOfferView.as_view(), name="create-offer"),
    path("offer-details/<int:pk>/", OfferDetailView.as_view(), name="offer-details"),
    # categories
    path("categories-list/", CategoryListView.as_view(), name="categories-list"),
    path("category-detail/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
