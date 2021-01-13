from rest_framework import serializers

from .models import Offer, Photo, OfferPhoto
from authentication.models import MotoCrawlerUser


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'url')
        model = Photo


class OfferPhotoSerializer(serializers.ModelSerializer):
    photo_url = serializers.ReadOnlyField(source='photo.url')

    class Meta:
        fields = ('id', 'offer', 'photo', 'photo_url')
        model = OfferPhoto


class OfferSerializer(serializers.ModelSerializer):
    photo_urls = serializers.StringRelatedField(many=True, source="offerphoto_set.all", read_only=True)

    class Meta:
        fields = ('id', 'url', 'brand', 'model', 'title', 'price', 'description', 'photo_urls')
        model = Offer


class FavouriteUserOffersSerializer(serializers.ModelSerializer):
    """Depth attribute allows to get into favourite_offers of the user whose PK was sent with the URI"""

    class Meta:
        fields = ('username', 'favourite_offers')
        model = MotoCrawlerUser
        depth = 1
