from rest_framework import generics, status, filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Offer, Photo, OfferPhoto
from authentication.models import MotoCrawlerUser
from .serializers import OfferSerializer, PhotoSerializer, OfferPhotoSerializer, FavouriteUserOffersSerializer


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


class BlacklistTokenView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OfferSearch(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^brand', '^model']


class UserFavouriteOffers(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    queryset = MotoCrawlerUser.objects.all()
    serializer_class = FavouriteUserOffersSerializer
