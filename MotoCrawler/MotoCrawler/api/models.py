from django.db import models
from authentication.models import MotoCrawlerUser


class Offer(models.Model):
    url = models.URLField()
    brand = models.TextField(max_length=128)
    model = models.TextField(max_length=128)
    title = models.TextField(max_length=1024)
    price = models.TextField(max_length=24)
    description = models.TextField(max_length=2048, null=True)

    def __str__(self):
        return self.title


class Photo(models.Model):
    offer = models.ManyToManyField(Offer, through="OfferPhoto")
    url = models.URLField()

    def __str__(self):
        return self.url


class OfferPhoto(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.photo.url


class UserFavouriteOffer(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    user = models.ForeignKey(MotoCrawlerUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
