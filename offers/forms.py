from django.forms import (
    Form,
    CharField,
    DecimalField,
    ModelChoiceField,
    widgets,
    ChoiceField,
    EmailField,
)
from django.core import validators
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Category


class CustomSignupForm(UserCreationForm):
    email = EmailField(widget=widgets.EmailInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        field_classes = {"username": UsernameField}

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and self._meta.model.objects.filter(email__iexact=email).exists():
            self._update_errors(ValidationError({"email": self.instance.unique_error_message(self._meta.model, ["email"])}))
        else:
            return email


class OfferForm(Form):
    type_offer = ChoiceField(choices=(("buy", "BUY (Куплю)"), ("sell", "SELL (Продам)")), widget=widgets.RadioSelect())
    category = ModelChoiceField(queryset=Category.objects.all())
    amount = DecimalField(max_digits=8, decimal_places=2, help_text="amount in metric tons")
    price = DecimalField(max_digits=8, decimal_places=2, help_text="price per 1 metric ton")
    currency = ChoiceField(choices=(("USD", "USD"), ("UAH", "UAH")), widget=widgets.RadioSelect())
    terms_delivery = ChoiceField(choices=(("EXW", "EXW - Ex Works (Франко-завод)"),
                                          ("FCA", "FCA - Free Carrier (Франко-перевізник)"),
                                          ("CPT", "CPT - Carriage Paid To (Перевезення оплачено до)"),
                                          ("CIP", "CIP - Carriage and Insurance Paid To (Перевезення та страхування оплачено до)"),
                                          ("DAP", "DAP - Delivered At Place (Поставка в місці)"),
                                          ("DPU", "DPU - Delivered At Place Unloaded (Поставка в місці з розвантаженням)"),
                                          ("DDP", "DDP - Delivered Duty Paid (Поставка з оплатою мита)"),
                                          ("FAS", "FAS - Free Alongside Ship (Франко вздовж борту судна)"),
                                          ("FOB", "FOB - Free On Board (Франко-борт)"),
                                          ("CFR", "CFR - Cost and Feight (Вартість і фрахт)"),
                                          ("CIF", "CIF - Cost Insurance and Freight (Вартість, страхування і фрахт)")
                                          ))
    details = CharField(max_length=255, min_length=4, required=False,
                        widget=widgets.Textarea(attrs={"cols": 40, "rows": 5}),
                        help_text="offers widely describe until 255 characters, allowed letters, digits and symbols ().-%,",
                        validators=([validators.RegexValidator(regex=r"\w+[(). -%,]")]))
    latitude = CharField(max_length=20,
                         # widget=widgets.TextInput(attrs={"readonly": True})
                         )
    longitude = CharField(max_length=20,
                          # widget=widgets.TextInput(attrs={"readonly": True})
                          )
