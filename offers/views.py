from django.views.generic import ListView

from .models import Offer, Category


class OffersListView(ListView):
    model = Offer
    queryset = Offer.actual.all()
    paginate_by = 10