from django.forms import (
    Form,
    CharField,
    DecimalField,
    ModelChoiceField,
    widgets,
    ChoiceField,
)

from .models import Category


class OfferForm(Form):
    category = ModelChoiceField(queryset=Category.objects.all())
    title = CharField(max_length=255, min_length=10, help_text="offers widely describe")
    type_offer = ChoiceField(choices=(("buy", "buy"), ("sell", "sell")))
    price_dollar = DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="price in dollars USA per 1 metric tonn",
    )
    amount = DecimalField(
        max_digits=6, decimal_places=3, help_text="amount in metric tons"
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
