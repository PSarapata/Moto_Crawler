from rest_framework import generics
from rest_framework.response import Response

from .models import Offer, Photo, OfferPhoto
from .serializers import OfferSerializer, PhotoSerializer, OfferPhotoSerializer


class OfferList(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class OfferDetail(generics.RetrieveDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class PhotoList(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class PhotoDetail(generics.RetrieveDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class OfferPhotosList(generics.ListAPIView):
    serializer_class = OfferPhotoSerializer
    queryset = OfferPhoto.objects.all()

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = OfferPhoto.objects.filter(offer_id=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
