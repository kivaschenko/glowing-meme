from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.auth.models import User

from PIL import Image

from offers.models import Category


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    full_name = models.CharField(max_length=150, blank=True, null=True, default='Full name')
    company = models.CharField(max_length=120, blank=True, null=True, default='Company name')
    phone = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='profile_avatars/', default='profile_avatars/default-avatar.jpg',
                               blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(max_length=600, blank=True, null=True)

    class Meta:
        db_table = 'profiles'
        ordering = ('user',)

    def __str__(self):
        return "Profile for {}".format(self.user.username)

    def __repr__(self):
        return f"<Profile(user_id={self.user_id} company={self.company}...)>"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('profile', kwargs={'user_id': self.user_id})

    # TODO: add Celery task to handle avatar image from mediafiles
    # def save(self, *args, **kwargs):
    #     super().save()
    #
    #     img = Image.open(self.image.path)  # Open image
    #
    #     # resize image
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)  # Resize image
    #         img.save(self.image.path)  # Save it again and override the larger image


class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interests')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='interests')

    class Meta:
        db_table = 'interests'
        ordering = ('category',)

    def __str__(self):
        return "Interest for {0}: {1}".format(self.user, self.category)

    def __repr__(self):
        return f"<Interest(user={self.user}, category={self.category})>"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_name = models.CharField(max_length=150, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    region = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    mini_map = models.FileField(upload_to='address_static_maps/', null=True)

    # geometry location
    geometry_point = gis_models.PointField(verbose_name="Location", srid=4326)

    class Meta:
        db_table = 'addresses'
        ordering = ['country', 'region']

    def __str__(self):
        return f"Address for {self.user}: {self.address_name} at {self.address}"

    def __repr__(self):
        return f"<Address(user={self.user} name={self.name}, latitude={self.latitude} longitude={self.longitude})>"
