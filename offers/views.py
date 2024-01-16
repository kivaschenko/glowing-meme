from decimal import Decimal
from django.db.models import QuerySet
from django.views.generic import ListView, DeleteView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import OfferForm, SearchForm
from .models import Offer, Category
from .services import create_new_offer, get_offers_by_category_id
from .events import NewOfferCreated
from .bus_messages import handle


# ----
# HOME
class HomeView(TemplateView):
    template_name = 'home.html'
    extra_context = {'form': SearchForm()}


# ------
# OFFERS

class OffersListView(ListView):
    model = Offer
    queryset = Offer.actual.all()[:100]
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


# ------
# Search

class SearchResultsView(ListView):
    model = Offer
    queryset = Offer.actual.all()
    ordering = ['country', 'region']
    filter_params = {}
    context_object_name = 'offers'
    template_name = 'offers/search_results.html'
    paginate_by = 10

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        self.filter_params = {}
        super(SearchResultsView, self).setup(request, *args, **kwargs)
        self._get_filter_params(request)

    def _get_filter_params(self, request):
        params = request.GET.copy()
        if type_offer := params.get('type_offer'):
            self.filter_params['type_offer'] = type_offer
        if category_id := params.get('category'):
            self.filter_params['category_id'] = int(category_id)
        if country := params.get('country'):
            self.filter_params['country'] = country
        if min_amount := params.get('min_amount'):
            self.filter_params['amount__gte'] = Decimal(min_amount)
        if max_amount := params.get('max_amount'):
            self.filter_params['amount__lte'] = Decimal(max_amount)
        if min_price := params.get('min_price'):
            self.filter_params['price__gte'] = Decimal(min_price)
        if max_price := params.get('max_price'):
            self.filter_params['price__lte'] = Decimal(max_price)
        if currency := params.get('currency'):
            self.filter_params['currency'] = currency
        if terms_delivery := params.get('terms_delivery'):
            self.filter_params['terms_delivery'] = terms_delivery

    def get_queryset(self):
        """
        Return the list of items for this view.
        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                # update queryset according GET params filtering:
                queryset = queryset.filter(**self.filter_params)
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset
