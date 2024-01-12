from django.contrib.auth import get_user_model

from accounts.models import Profile
from offers.models import Offer, Category


user_samples = [
    ('testuser1', 'Te$testuser1@example.com', '$0meSeecretP4$$word1'),
    ('testuser2', 'Te$testuser2@example.com', '$0meSeecretP4$$word2'),
    ('testuser3', 'Te$testuser3@example.com', '$0meSeecretP4$$word3'),
]

profile_samples = [
    ('Petro Gerashchenko', 'Test Grain Company LLC', '+380441235813', 'http://www.test-grain-company.com.ua'),
    ('Mykola Petrenko', 'Test GrainFuelTrade LLC', '+380951235813', 'http://www.test-grain-fuel-trade.com.ua'),
    ('Sergiy Ivahnenko', 'Test Farmer Grain LLC', '+380671235813', 'http://www.test-farmer-grain.com.ua'),
]

coordinates_samples = [

]

def create_fake_user(username,  email, password):
    user = get_user_model()
    u = user.objects.create_user(username=username, email=email, password=password)
    return u


def update_profile(user_id, full_name, company, phone, website):
    profile = Profile.objects.get(pk=user_id)
    profile.full_name = full_name
    profile.company = company
    profile.phone = phone
    profile.website = website
    profile.save()
    return profile


def create_pool_offers(user_id):
