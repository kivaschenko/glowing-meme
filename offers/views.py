from django.views.generic import ListView, DeleteView, DetailView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import OfferForm
from .models import Offer, Category
from .services import create_new_offer, get_offers_by_category_id
from .events import NewOfferCreated
from .bus_messages import handle


# ------
# OFFERS

class OffersListView(ListView):
    model = Offer
    queryset = Offer.actual.all()
    context_object_name = 'offers'
    # paginate_by = 10


@method_decorator(login_required, name='dispatch')
class CreateOfferView(FormView):
    form_class = OfferForm
    success_url = "/offers-list/"
    template_name = "offers/create_offer.html"

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        if self.events:
            for event in self.events:
                handle(event)
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            # create a new offer
            new_offer = create_new_offer(user_id=request.user.id,
                                         category_id=data.get("category").id,
                                         type_offer=data.get("type_offer"),
                                         price=data.get("price"),
                                         currency=data.get("currency"),
                                         amount=data.get("amount"),
                                         terms_delivery=data.get("terms_delivery"),
                                         latitude=data.get("latitude"),
                                         longitude=data.get("longitude"),
                                         details=data.get("details"),
                                         )
            # create a new events
            self.events.append(NewOfferCreated(new_offer.longitude, new_offer.latitude, new_offer.id))
            # self.get(request, *args, **kwargs)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        if hasattr(self, "get") and not hasattr(self, "head"):
            self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs
            # for events
            self.events = []


class OfferDetailView(DetailView):
    model = Offer
    context_object_name = 'offer'


# ----------
# Categories

class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'categories'
    template_name = 'categories/category_list.html'

class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    extra_context = {}
    template_name = 'categories/category_detail.html'
    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = {}
        if self.object:
            context["object"] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
            self.extra_context['offers'] = get_offers_by_category_id(category_id=self.object.id)
        context.update(kwargs)
        return super().get_context_data(**context)