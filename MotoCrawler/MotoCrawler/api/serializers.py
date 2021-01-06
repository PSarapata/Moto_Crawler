from rest_framework import serializers
from .models import Offer, Photo, OfferPhoto
from django.contrib.auth.models import User


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
