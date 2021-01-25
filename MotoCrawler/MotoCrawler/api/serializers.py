from rest_framework import serializers

from .models import Offer, Photo, OfferPhoto, UserFavouriteOffer


class PhotoSerializer(serializers.ModelSerializer):
    """Serializer for Photo database objects."""
    class Meta:
        fields = ('id', 'url')
        model = Photo


class OfferPhotoSerializer(serializers.ModelSerializer):
    """Serializer for Offer-Photo database objects.
    Serializer displays following data:
    id = OfferPhoto instance Unique Identifier
    offer = Related Offer instance Unique Identifier
    photo = Related Photo instance Unique Identifier
    photo_url = URL of Related Photo instance"""
    photo_url = serializers.ReadOnlyField(source='photo.url')

    class Meta:
        fields = ('id', 'offer', 'photo', 'photo_url')
        model = OfferPhoto


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for Offer database objects.
    Besides displaying all relevant Offer object attributes,
    it also displays all related Photo instances
    using photo_urls StringRelatedField in read-only mode,
    'many=True' flag is used to display the entire set."""
    photo_urls = serializers.StringRelatedField(many=True, source="offerphoto_set.all", read_only=True)

    class Meta:
        fields = ('id', 'url', 'brand', 'model', 'title', 'price', 'description', 'photo_urls')
        model = Offer


class FavouriteOfferSerializer(serializers.ModelSerializer):
    """Serializer displays Unique Identifier and timestamp
    of related UserFavouriteOffer instance and all attributes
    of related Offer instance.
    'depth=1' flag was used to achieve this."""
    def create(self, validated_data):
        print("Hello from create method of FavouriteOfferSerializer.")
        return UserFavouriteOffer.objects.create(**validated_data)
    photo_urls = serializers.StringRelatedField(many=True, source="offer.offerphoto_set.all")

    class Meta:
        exclude = ('user',)
        model = UserFavouriteOffer
        depth = 1
