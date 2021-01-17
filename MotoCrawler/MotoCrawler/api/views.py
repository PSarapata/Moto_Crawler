from rest_framework import generics, status, filters, viewsets
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_list_or_404, get_object_or_404

from .models import Offer, Photo, OfferPhoto, UserFavouriteOffer
from .serializers import OfferSerializer, PhotoSerializer, OfferPhotoSerializer, FavouriteOfferSerializer


class ManageFavouriteOfferPermission(BasePermission):
    """
    Custom Permission limiting object modifications on an object
    to its' legitimate owner user only.
    Returns true if the User Primary Key passed along with the request matches
    the User Foreign Key of UserFavouriteOffer instance.
    User has to be authenticated.

    :param: request: HTTP request
    :type request: request: HTTP request
    :param: view: Used on :class: 'UserFavouriteOfferViewSet' ModelViewSet.
    :type view: class: 'UserFavouriteOfferViewSet'
    :param: obj: Authorized User database object (model)
    :obj type: object: 'MotoCrawlerUser'
    :return: Boolean
    """
    message = 'Viewing favourite offers is only allowed for their owner.'

    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user


class OfferList(generics.ListAPIView):
    """
    Simple list view for Offer objects.
    IsAuthenticated project permission applies.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class OfferDetail(generics.RetrieveDestroyAPIView):
    """
    Allows to view and delete Offer instances.
    IsAuthenticated project permission applies.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class PhotoList(generics.ListAPIView):
    """
    Simple list view for Photo objects.
    IsAuthenticated project permission applies.
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class PhotoDetail(generics.RetrieveDestroyAPIView):
    """
    Allows to view and delete Photo instances.
    IsAuthenticated project permission applies.
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class OfferPhotosList(generics.ListAPIView):
    """
    Custom list View for related Offer-Photo instances.
    View feeds on Primary Key of an Offer instance and returns
    serialized list of related Offer-Photo objects.
    IsAuthenticated project permission applies.
    """
    serializer_class = OfferPhotoSerializer
    queryset = OfferPhoto.objects.all()

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = OfferPhoto.objects.filter(offer_id=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BlacklistTokenView(APIView):
    """
    View is used to blacklist expired JWT refresh tokens
    and issue the user a fresh one.
    If everything went as expected = returns HTTP_205_RESET_CONTENT
    Else = returns HTTP_400_BAD_REQUEST
    View is accessible by anyone.
    :return: HTTP_205_RESET_CONTENT on success || HTTP_400_BAD_REQUEST on failure
    """
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
    """
    Search by brand or model view. Filter backend tries to find a match between input string
    and values taken from database, given how they begin.
    Example:
    You want to find model '3000 GT'. I recommend to use search phrase '3000', as it should yield all related
    results, such as '3000-GT' or '3000GT' alongside the queried '3000 GT'.
    IsAuthenticated project permission applies.
    """

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^brand', '^model']


class UserFavouriteOfferViewSet(viewsets.ModelViewSet):
    """Custom Viewset to manage User-FavouriteOffers relation.
    ManageFavouriteOfferPermission applies:
    User has to be authenticated and a holder of a matching User Foreign Key
    to be able to use this view."""
    permission_classes = [ManageFavouriteOfferPermission]
    serializer_class = FavouriteOfferSerializer

    #  Retrieve/Update/Destroy, get a single item based on related object's ID.
    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(UserFavouriteOffer, pk=item)

    # List only Offers related to authenticated User.
    def get_queryset(self):
        return get_list_or_404(UserFavouriteOffer, user=self.request.user)
