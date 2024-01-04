from decimal import Decimal
from unittest.mock import patch
from pathlib import Path

from django.conf import settings
from django.test import TestCase, Client
from django.contrib.auth.models import User

from .models import Offer
from .services import get_address_info_by_coords, get_static_map_image_by_coords
from .mocks import *


class OfferTest(TestCase):
    fixtures = [
        'offers/fixtures/categories.json',
        'offers/fixtures/users.json',
    ]

    def setUp(self):
        client = Client()
        test_user = User.objects.get(id=1)

    def tearDown(self):
        # remove minimap images
        minimaps_dir = settings.MEDIA_ROOT / 'offer_static_maps/'
        [f.unlink() for f in minimaps_dir.glob('*.png') if f.is_file()]

    @patch('offers.services.get_address_from_mapbox', mock_address_response_from_mapbox)
    @patch('offers.services.get_static_map_image_from_mapbox', mock_fake_minimap_image)
    def test_create_offer_success(self):
        # create offer
        form_data = dict(
            category=51,
            type_offer='sell',
            price=Decimal('345.90'),
            currency='USD',
            amount=Decimal('1000.00'),
            terms_delivery='FCA',
            latitude=Decimal("53.403045"),
            longitude=Decimal("10.016860"),
            details='protein - 33.25%, garbage - 1.2%'
        )
        # log in
        self.client.login(username='dev', password='235813')

        res = self.client.post("/create-offer/", data=form_data)
        self.assertEqual(res.status_code, 302)
        new_offer = Offer.objects.last()
        self.assertEqual(new_offer.type_offer, 'sell')
        self.assertEqual(new_offer.amount, Decimal('1000.00'))
        self.assertEqual(new_offer.details, 'protein - 33.25%, garbage - 1.2%')

        get_address_info_by_coords(new_offer.longitude, new_offer.latitude, new_offer.id)

        updated_offer = Offer.objects.get(id=new_offer.id)
        self.assertEqual("Germany", updated_offer.country)
        self.assertEqual("Lohe 9, 21217 Seevetal, Germany", updated_offer.address)

        get_static_map_image_by_coords(new_offer.longitude, new_offer.latitude, new_offer.id)

        updated_offer = Offer.objects.get(id=new_offer.id)
        self.assertIn('offer_static_maps/minimap_', updated_offer.mini_map_img.name)

    def test_offer_not_created_without_logged_user(self):
        # create offer
        form_data = dict(
            category=13,
            type_offer='buy',
            price=Decimal('123.58'),
            currency='USD',
            amount=Decimal('1123.58'),
            terms_delivery='FCA',
            latitude=Decimal('49.326304'),
            longitude=Decimal('32.218506'),
            details='protein - 33.25% '
        )
        res = self.client.post("/create-offer/", data=form_data)

        self.assertEqual(res.status_code, 302)
        new_offer = Offer.objects.last()
        self.assertIsNone(new_offer)
