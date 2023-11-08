from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import OfferForm
from .models import Offer
from .services import create_new_offer


class OffersListView(ListView, FormView):
    model = Offer
    queryset = Offer.actual.all()
    paginate_by = 10
    form_class = OfferForm


def create_offer(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = OfferForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            # create a new offer
            create_new_offer(
                category_id=data.get('category').id,
                title=data.get('title'),
                type_offer=data.get('type_offer'),
                price=data.get('price'),
                currency=data.get('currency'),
                amount=data.get('amount'),
                terms_delivery=data.get('terms_delivery'),
                latitude=data.get('latitude'),
                longitude=data.get('longitude')
            )
            # redirect to a new URL:
            return HttpResponseRedirect("/offers-list/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = OfferForm()

    return render(request, "offers/create_offer.html", {"form": form})
