from rest_framework import serializers

from .models import Offer, Photo, OfferPhoto, UserFavouriteOffer


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


class FavouriteOfferSerializer(serializers.ModelSerializer):
    """Serializer lists id of related UserFavouriteOffer instance and details of related Offer instance"""
    class Meta:
        exclude = ('timestamp', 'user')
        model = UserFavouriteOffer
        depth = 1
