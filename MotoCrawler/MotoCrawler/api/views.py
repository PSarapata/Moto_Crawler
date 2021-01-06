from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Offer, Photo, OfferPhoto
from .serializers import OfferSerializer, PhotoSerializer, OfferPhotoSerializer, UserSerializer


class OfferList(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class OfferDetail(generics.RetrieveDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]


class PhotoList(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]


class PhotoDetail(generics.RetrieveDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class OfferPhotosList(generics.ListAPIView):
    serializer_class = OfferPhotoSerializer
    queryset = OfferPhoto.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = OfferPhoto.objects.filter(offer_id=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class BlacklistTokenView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TestView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Well, hello there!'}
        return Response(content)
