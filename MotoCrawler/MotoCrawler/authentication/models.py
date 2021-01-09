from django.db import models
from django.contrib.auth.models import AbstractUser


# MotoCrawlerUser extends from base Django user. I used it for authentication, following this tutorial:
# "https://hackernoon.com/110percent-complete-jwt-authentication-with-django-and-react-2020-iejq34ta"
# I then had an idea to create a relation so a user can store/watch his favourite offers, hence the relation:
class MotoCrawlerUser(AbstractUser):
    favourite_offers = models.ManyToManyField("api.Offer", through="api.UserFavouriteOffer")
