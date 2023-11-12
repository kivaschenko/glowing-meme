from decimal import Decimal

from django.test import TestCase, Client
from django.contrib.auth.models import User

from .models import Offer, Category


class OfferTest(TestCase):
    fixtures = [
        'offers/fixtures/categories.json',
        'offers/fixtures/users.json',
    ]

    def setUp(self):
        client = Client()
        test_user = User.objects.get(id=1)

    def test_create_offer_success(self):
        # create offer
        form_data = dict(
            category=26,
            type_offer='buy',
            price=Decimal('123.58'),
            currency='USD',
            amount=Decimal('1123.58'),
            terms_delivery='FCA',
            latitude=Decimal('49.32630492910923'),
            longitude=Decimal('32.218506548413444'),
            details='protein - 33.25%, garbage - 1.2%'
        )
        # log in
        self.client.login(username='dev', password='235813')
        res = self.client.post("/create-offer/", data=form_data)
        self.assertEqual(res.status_code, 302)
        new_offer = Offer.objects.last()
        self.assertEqual(new_offer.amount, Decimal('1123.58'))

    def test_offer_wasnt_created_without_logged_user(self):
        category = Category.objects.first()
        # create offer
        form_data = dict(
            category=13,
            type_offer='buy',
            price=Decimal('123.58'),
            currency='USD',
            amount=Decimal('1123.58'),
            terms_delivery='FCA',
            latitude=Decimal('49.32630492910923'),
            longitude=Decimal('32.218506548413444'),
            details='protein - 33.25%, garbage - 1.2%'
        )
        res = self.client.post("/create-offer/", data=form_data)

        self.assertEqual(res.status_code, 200)
        new_offer = Offer.objects.last()
        self.assertIsNone(new_offer)
