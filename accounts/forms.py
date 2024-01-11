from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from accounts.models import Profile


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
