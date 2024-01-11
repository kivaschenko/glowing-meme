from unittest.mock import patch
from django.test import TestCase, Client
from django.contrib.auth.models import User

from accounts.models import Profile


class ProfileTestClass(TestCase):
    def setUp(self):
        client = Client()

    # @patch("django.db.models.signals.ModelSignal.send")
    def test_auto_create_profile_after_registration_successful(self):
        form_data = dict(
            username='test-user-1',
            email='test-user-1@graintrade.info',
            password1='6gB7^)v4;XM#-X!',
            password2='6gB7^)v4;XM#-X!',
        )
        # register
        r = self.client.post('/accounts/signup/', form_data)
        self.assertEqual(r.status_code, 302)
        user = User.objects.last()
        self.assertEqual(user.username, 'test-user-1')
        self.assertEqual(user.email, 'test-user-1@graintrade.info')
        p = Profile.objects.last()
        self.assertEqual(p.user.username, 'test-user-1')
        self.assertEqual(p.full_name, 'Full name')
        self.assertEqual(p.company, 'Company name')
