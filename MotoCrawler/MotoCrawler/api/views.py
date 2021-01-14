from rest_framework import generics, status, filters, viewsets
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_list_or_404, get_object_or_404

from .models import Offer, Photo, OfferPhoto, UserFavouriteOffer
from .serializers import OfferSerializer, PhotoSerializer, OfferPhotoSerializer, FavouriteOfferSerializer


class ManageFavouriteOfferPermission(BasePermission):
    message = 'Viewing favourite offers is only allowed for their owner.'

    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user


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
    """Search by brand or model view. Filter backend tries to find a match between input string
    and values taken from database, given how they begin.
    Example:
    You want to find model '3000 GT'. I recommend to use search phrase '3000', as it should yield all related
    results, such as '3000-GT' or '3000GT' alongside the queried '3000 GT'."""

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^brand', '^model']


class UserFavouriteOfferViewSet(viewsets.ModelViewSet):
    """Testing viewset approach whether it's gonna be easier to get into UserFavourites."""
    permission_classes = [ManageFavouriteOfferPermission]
    serializer_class = FavouriteOfferSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(UserFavouriteOffer, pk=item)

    # List only Offers related to logged in User
    def get_queryset(self):
        return get_list_or_404(UserFavouriteOffer, user=self.request.user)
