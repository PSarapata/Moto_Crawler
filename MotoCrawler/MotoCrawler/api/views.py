from rest_framework import generics
from .models import Offer
from .serializers import OfferSerializer


class OfferList(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class OfferDetail(generics.RetrieveDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
