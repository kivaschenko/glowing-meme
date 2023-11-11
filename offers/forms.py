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
    type_offer = ChoiceField(
        choices=(("buy", "BUY (Куплю)"), ("sell", "SELL (Продам)")), widget=widgets.RadioSelect()
    )
    category = ModelChoiceField(queryset=Category.objects.all())
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
            ("UAH", "UAH"),
        ),
        widget=widgets.RadioSelect(),
    )
    terms_delivery = ChoiceField(
        choices=(
            ("EXW", "EXW - Ex Works (Франко-завод)"),
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
        ),
    )
    details = CharField(
        max_length=255,
        required=False,
        widget=widgets.Textarea(attrs={"cols": 40, "rows": 5}),
        help_text="offers widely describe until 255 characters, allowed letters, digits and symbols ().-%,",
        validators=([validators.RegexValidator(regex=r"\w+[(). -%,]")]),
    )
    latitude = CharField(max_length=20)
    longitude = CharField(max_length=20)
