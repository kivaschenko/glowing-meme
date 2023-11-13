from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase, Client
from django.contrib.auth.models import User

from .models import Offer, Category


def mock_address_reposne_from_mapbox(*kwargs):
    fake_response = {'type': 'FeatureCollection', 'query': [32.049741352051115, 49.43173280170663], 'features': [{'id': 'address.2094753486894238', 'type': 'Feature', 'place_type': ['address'], 'relevance': 1, 'properties': {'accuracy': 'street'}, 'text': 'Провулок Яцька Остряниці', 'place_name': 'Провулок Яцька Остряниці, Черкаси, Ukraine, 180', 'center': [32.0496019, 49.4318573], 'geometry': {'type': 'Point', 'coordinates': [32.0496019, 49.4318573]}, 'context': [{'id': 'postcode.1822441', 'mapbox_id': 'dXJuOm1ieHBsYzpHODdw', 'text': '180'}, {'id': 'place.229976297', 'mapbox_id': 'dXJuOm1ieHBsYzpEYlVvNlE', 'wikidata': 'Q157055', 'text': 'Черкаси'}, {'id': 'region.9449', 'mapbox_id': 'dXJuOm1ieHBsYzpKT2s', 'wikidata': 'Q161808', 'short_code': 'UA-71', 'text': 'Cherkasy Oblast'}, {'id': 'country.8937', 'mapbox_id': 'dXJuOm1ieHBsYzpJdWs', 'wikidata': 'Q212', 'short_code': 'ua', 'text': 'Ukraine'}]}, {'id': 'postcode.1822441', 'type': 'Feature', 'place_type': ['postcode'], 'relevance': 1, 'properties': {'mapbox_id': 'dXJuOm1ieHBsYzpHODdw'}, 'text': '180', 'place_name': '180, Черкаси, Cherkasy Oblast, Ukraine', 'bbox': [31.946251, 49.349863, 32.151058, 49.494097], 'center': [32.05878, 49.444789], 'geometry': {'type': 'Point', 'coordinates': [32.05878, 49.444789]}, 'context': [{'id': 'place.229976297', 'mapbox_id': 'dXJuOm1ieHBsYzpEYlVvNlE', 'wikidata': 'Q157055', 'text': 'Черкаси'}, {'id': 'region.9449', 'mapbox_id': 'dXJuOm1ieHBsYzpKT2s', 'wikidata': 'Q161808', 'short_code': 'UA-71', 'text': 'Cherkasy Oblast'}, {'id': 'country.8937', 'mapbox_id': 'dXJuOm1ieHBsYzpJdWs', 'wikidata': 'Q212', 'short_code': 'ua', 'text': 'Ukraine'}]}, {'id': 'place.229976297', 'type': 'Feature', 'place_type': ['place'], 'relevance': 1, 'properties': {'mapbox_id': 'dXJuOm1ieHBsYzpEYlVvNlE', 'wikidata': 'Q157055'}, 'text': 'Черкаси', 'place_name': 'Черкаси, Cherkasy Oblast, Ukraine', 'bbox': [31.9584686, 49.364981, 32.125147, 49.4976578], 'center': [32.0588, 49.4448], 'geometry': {'type': 'Point', 'coordinates': [32.0588, 49.4448]}, 'context': [{'id': 'region.9449', 'mapbox_id': 'dXJuOm1ieHBsYzpKT2s', 'wikidata': 'Q161808', 'short_code': 'UA-71', 'text': 'Cherkasy Oblast'}, {'id': 'country.8937', 'mapbox_id': 'dXJuOm1ieHBsYzpJdWs', 'wikidata': 'Q212', 'short_code': 'ua', 'text': 'Ukraine'}]}, {'id': 'region.9449', 'type': 'Feature', 'place_type': ['region'], 'relevance': 1, 'properties': {'mapbox_id': 'dXJuOm1ieHBsYzpKT2s', 'wikidata': 'Q161808', 'short_code': 'UA-71'}, 'text': 'Cherkasy Oblast', 'place_name': 'Cherkasy Oblast, Ukraine', 'bbox': [29.611994, 48.463392, 32.887905, 50.223179], 'center': [32.0587805, 49.4447888], 'geometry': {'type': 'Point', 'coordinates': [32.0587805, 49.4447888]}, 'context': [{'id': 'country.8937', 'mapbox_id': 'dXJuOm1ieHBsYzpJdWs', 'wikidata': 'Q212', 'short_code': 'ua', 'text': 'Ukraine'}]}, {'id': 'country.8937', 'type': 'Feature', 'place_type': ['country'], 'relevance': 1, 'properties': {'mapbox_id': 'dXJuOm1ieHBsYzpJdWs', 'wikidata': 'Q212', 'short_code': 'ua'}, 'text': 'Ukraine', 'place_name': 'Ukraine', 'bbox': [22.136964, 44.3163136, 40.22559, 52.379352], 'center': [31.3202829593814, 49.3227937844972], 'geometry': {'type': 'Point', 'coordinates': [31.3202829593814, 49.3227937844972]}}], 'attribution': 'NOTICE: © 2023 Mapbox and its suppliers. All rights reserved. Use of this data is subject to the Mapbox Terms of Service (https://www.mapbox.com/about/maps/). This response and the information it contains may not be retained. POI(s) provided by Foursquare.'}
    return fake_response


class OfferTest(TestCase):
    fixtures = [
        'offers/fixtures/categories.json',
        'offers/fixtures/users.json',
    ]

    def setUp(self):
        client = Client()
        test_user = User.objects.get(id=1)

    @patch('offers.services.get_address_info_by_coords', mock_address_reposne_from_mapbox)
    def test_create_offer_success(self):
        # create offer
        form_data = dict(
            category=26,
            type_offer='buy',
            price=Decimal('123.58'),
            currency='USD',
            amount=Decimal('1123.58'),
            terms_delivery='FCA',
            latitude=Decimal('49.43173280170663'),
            longitude=Decimal('32.049741352051115'),
            details='protein - 33.25%, garbage - 1.2%'
        )
        # log in
        self.client.login(username='dev', password='235813')
        res = self.client.post("/create-offer/", data=form_data)
        self.assertEqual(res.status_code, 302)
        new_offer = Offer.objects.last()
        self.assertEqual(new_offer.amount, Decimal('1123.58'))
        # need Celery work
        self.assertEqual(new_offer.address, 'Провулок Яцька Остряниці, Черкаси, Ukraine, 180')
        self.assertEqual(new_offer.country, 'Ukraine')

    def test_offer_not_created_without_logged_user(self):
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

        self.assertEqual(res.status_code, 302)
        new_offer = Offer.objects.last()
        self.assertIsNone(new_offer)
