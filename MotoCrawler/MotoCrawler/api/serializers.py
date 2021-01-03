from rest_framework import serializers
from .models import Offer, Photo, OfferPhoto


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'url', 'brand', 'model', 'title', 'price', 'description')
        model = Offer


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'url')
        model = Photo


class OfferPhotoSerializer(serializers.ModelSerializer):
    photo_url = serializers.ReadOnlyField(source='photo.url')

    class Meta:
        fields = ('id', 'offer', 'photo', 'photo_url')
        model = OfferPhoto
