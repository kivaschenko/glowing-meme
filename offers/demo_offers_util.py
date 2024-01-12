from copy import copy
from decimal import Decimal

from django.contrib.auth.models import User

from accounts.models import Profile
from offers.models import Offer


user_data = {
    'username': 'testuser{}',
    'email': 'Te$testuser{}@example.com',
    'password': '$0meSeecretP4$$word{}',
}


def create_pool_offers(user, all_offers):
    print('Creating pool offers')
    for offer in all_offers:
        new_offer = copy(offer)
        new_offer.id = None
        new_offer.author = user
        if offer.type_offer == 'buy':
            new_offer.type_offer = 'sell'
            new_offer.price *= Decimal('1.05')
            new_offer.amount *= Decimal('1.10')
        else:
            new_offer.type_offer = 'buy'
            new_offer.price *= Decimal('0.95')
            new_offer.amount *= Decimal('0.90')
        new_offer.latitude -= Decimal('0.000001')
        new_offer.longitude += Decimal('0.000001')
        new_offer.save()
        print(new_offer)


def main(counter=3):
    all_offers = Offer.objects.all()
    new_users = []
    # create users with profiles
    for c in range(1, counter + 1, 1):
        last_user = User.objects.last()
        next_user_id = last_user.id + 1
        u_data = {k:v.format(next_user_id) for k, v in user_data.items()}
        new_user = User.objects.create_user(**u_data)
        print(new_user)
        new_users.append(new_user)
    # create offers
    for i in range(len(new_users)):
        create_pool_offers(user=new_users[i], all_offers=all_offers)


if __name__ == '__main__':
    main()