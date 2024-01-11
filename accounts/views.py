from django.http import HttpResponseForbidden
from django.views.generic import DetailView, UpdateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login

from .models import Profile
from .forms import CustomSignupForm
from offers.services import get_offers_by_author_id


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

