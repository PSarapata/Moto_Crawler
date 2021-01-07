from django.db import models
from django.contrib.auth.models import AbstractUser


# For now this is just a test to fix authentication issue I ran up to, I am following a tutorial from Hackernoon:
# "https://hackernoon.com/110percent-complete-jwt-authentication-with-django-and-react-2020-iejq34ta"
# I might change this field to create an actual favourite offer relation at some point in the future.
class MotoCrawlerUser(AbstractUser):
    favourite_offer = models.CharField(blank=True, max_length=120)
