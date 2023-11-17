from django.views.generic import ListView, DeleteView, DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import OfferForm, CustomSignupForm
from .models import Offer
from .services import create_new_offer


# -----------------
# BUILT IN ACCOUNTS

class RegistrationView(FormView):
    template_name = 'registration/signup.html'
    form_class = CustomSignupForm
    success_url = '/home/'
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

# ------
# OFFERS

class OffersListView(ListView):
    model = Offer
    queryset = Offer.actual.all()
    context_object_name = 'offers'


@method_decorator(login_required, name='dispatch')
class CreateOfferView(FormView):
    form_class = OfferForm
    success_url = "/offers-list/"
    template_name = "offers/create_offer.html"

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            # create a new offer
            create_new_offer(
                user_id=request.user.id,
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
            # self.get(request, *args, **kwargs)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class OfferDetailView(DetailView):
    model = Offer
    context_object_name = 'offer'
