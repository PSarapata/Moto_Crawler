from rest_framework import serializers
from .models import Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'url', 'brand', 'model', 'title', 'price', 'description')
        model = Offer
