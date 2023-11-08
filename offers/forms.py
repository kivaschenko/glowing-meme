from django.forms import (
    Form,
    CharField,
    DecimalField,
    ModelChoiceField,
    widgets,
    ChoiceField,
)
from django.core import validators

from .models import Category


class OfferForm(Form):
    type_offer = ChoiceField(choices=(("buy", "BUY"), ("sell", "SELL")))
    category = ModelChoiceField(queryset=Category.objects.all())
    title = CharField(
        max_length=255,
        min_length=10,
        help_text="offers widely describe until 255 characters, allowed letters, digits and symbols (). -%,",
        validators=[validators.RegexValidator(regex=r"\w+[(). -%,]")],
    )
    amount = DecimalField(
        max_digits=8, decimal_places=2, help_text="amount in metric tons"
    )
    price = DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="price per 1 metric ton",
    )
    currency = ChoiceField(
        choices=(
            ("USD", "USD"),
            ("EUR", "EUR"),
            ("UAH", "UAH"),
        )
    )
    terms_delivery = ChoiceField(
        choices=(
            ("EXW", "EXW"),
            ("FCA", "FCA"),
            ("CPT", "CPT"),
            ("CIP", "CIP"),
            ("DAP", "DAP"),
            ("DPU", "DPU"),
            ("DDP", "DDP"),
            ("FAS", "FAS"),
            ("FOB", "FOB"),
            ("CFR", "CFR"),
            ("CIF", "CIF"),
        ),
    )
    latitude = CharField(max_length=20)
    longitude = CharField(max_length=20)
