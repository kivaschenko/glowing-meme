from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from accounts.models import Profile

user_model = get_user_model()


@receiver(post_save, sender=user_model, dispatch_uid="auto_create_profile")
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=user_model, dispatch_uid="auto_save_profile")
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
