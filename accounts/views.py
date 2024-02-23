from decimal import Decimal

from celery.bin.control import status
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView, UpdateView, TemplateView
from django.views.generic.edit import FormView, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login

from .models import Profile, Address
from .forms import CustomSignupForm, AddressForm, SearchByAddressAndRadius
from service_layer.services import (
    get_offers_by_author_id,
    create_new_address,
    find_offers_within_radius,
    get_geojson_features_within_radius,
)
from service_layer.events import NewAddressCreated
from service_layer.bus_messages import handle


# -----------------
# BUILT IN ACCOUNTS

class RegistrationView(FormView):
    template_name = 'registration/signup.html'
    form_class = CustomSignupForm
    success_url = reverse_lazy('home')
    extra_context = {}

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            user = form.save()
            self.extra_context.update({'messages': 'You have registered successfully!'})
            login(request, user)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# -------
# Profile

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['full_name', 'company', 'phone', 'avatar', 'website', 'description']
    template_name = 'profile/profile_form.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseForbidden("You do not have permission to edit this profile")
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            data = form.cleaned_data
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profile/profile_detail.html'
    pk_url_kwarg = 'user_id'
    extra_context = {'offers': []}

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        if hasattr(self, "get") and not hasattr(self, "head"):
            self.head = self.get
        self.request = request
        self.args = args
        self.kwargs = kwargs
        # add offers list for current profile
        author_id = self.kwargs.get(self.pk_url_kwarg)
        offers = get_offers_by_author_id(author_id)
        self.extra_context['offers'] = offers


# -------
# Address

class CreateAddressView(LoginRequiredMixin, FormView):
    form_class = AddressForm
    template_name = 'profile/address_form.html'

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        success_url = 'accounts/profile/{}/'.format(self.request.user.id)
        return success_url

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
            # create a new address
            new_address = create_new_address(user_id=request.user.id, **data)
            new_address.save()
            # create new events
            self.events.append(NewAddressCreated(new_address.longitude, new_address.latitude, new_address.id))
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


class AddressDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Address
    template_name = 'profile/address_detail.html'
    form_class = SearchByAddressAndRadius
    extra_context = {}
    context_object_name = 'address'

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = {}
        if self.object:
            context["object"] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        return super().get_context_data(**context)


def search_results_map(request, pk):
    # template_name = 'profile/search_map_by_address.html'
    template_name = 'offers/map_listing.html'
    context = {}
    data = request.GET
    address_obj = Address.objects.get(pk=pk)
    # add center map coords to context
    context.update({'center_lng': float(address_obj.longitude), 'center_lat': float(address_obj.latitude)})
    filter_params = dict(
        longitude=address_obj.longitude,
        latitude=address_obj.latitude,
        radius_in_meters=data.get("radius"),
        category_id=data.get("category"),
        type_offer=data.get("type_offer"),
    )
    if min_price := data.get("min_price"):
        filter_params.update({'min_price': min_price})
    if max_price := data.get("max_price"):
        filter_params.update({'max_price': max_price})
    if min_amount := data.get("min_amount"):
        filter_params.update({'min_amount': min_amount})
    if max_amount := data.get("max_amount"):
        filter_params.update({'max_amount': max_amount})
    json_data = get_geojson_features_within_radius(**filter_params)
    context.update({'places': json_data})
    # return JsonResponse(context, status=200)
    return render(request, template_name, context, status=200)
