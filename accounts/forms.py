from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from accounts.models import Profile
from offers.models import Category, Offer


class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(widget=forms.widgets.EmailInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        field_classes = {"username": UsernameField}

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and self._meta.model.objects.filter(email__iexact=email).exists():
            self._update_errors(
                ValidationError({"email": self.instance.unique_error_message(self._meta.model, ["email"])}))
        else:
            return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'company', 'phone', 'avatar', 'website', 'description']
        widgets = {'user': forms.HiddenInput()}


class AddressForm(forms.Form):
    address_name = forms.CharField(max_length=150,
                                   help_text='Enter your address name, for example "My wholesale warehouse')
    latitude = forms.CharField(max_length=20)
    longitude = forms.CharField(max_length=20)


class SearchByAddressAndRadius(forms.Form):
    type_offer = forms.ChoiceField(choices=(("buy", "BUY (Куплю)"), ("sell", "SELL (Продам)")),
                                   widget=forms.widgets.RadioSelect(), initial="buy")
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    min_amount = forms.DecimalField(max_digits=8, decimal_places=2, required=False,
                                    help_text="minimum amount in metric tons")
    max_amount = forms.DecimalField(max_digits=8, decimal_places=2, required=False,
                                    help_text="maximum amount in metric tons")
    min_price = forms.DecimalField(max_digits=8, decimal_places=2, required=False,
                                   help_text="minimum price per 1 metric ton")
    max_price = forms.DecimalField(max_digits=8, decimal_places=2, required=False,
                                   help_text="maximum price per 1 metric ton")
    currency = forms.ChoiceField(choices=(("USD", "USD"), ("UAH", "UAH")), widget=forms.widgets.RadioSelect(),
                                 initial="UAH")
    radius = forms.ChoiceField(
        choices=(("161000", "161 km (100 miles)"), ("322000", "322 km (200 miles"), ("483000", "483 km (300 miles)")),
        widget=forms.widgets.RadioSelect(),
        initial="161000",
        help_text='radius in km from the address',
    )
