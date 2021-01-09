from django.urls import path
from .views import OfferList, OfferDetail, PhotoList, PhotoDetail, OfferPhotosList, BlacklistTokenView, OfferSearch, UserFavouriteOffers

urlpatterns = [
    path('<int:pk>/', OfferDetail.as_view(), name='detailview'),
    path('', OfferList.as_view(), name='listview'),
    path('photos/', PhotoList.as_view(), name='photolistview'),
    path('photos/<int:pk>/', PhotoDetail.as_view(), name='photodetailview'),
    path('offerphotos/<int:pk>/', OfferPhotosList.as_view(), name='offerphotos'),
    path('user/favourites/<int:pk>/', UserFavouriteOffers.as_view(), name='favourites'),
    path('user/logout/blacklist/', BlacklistTokenView.as_view(), name='blacklist'),
    path('search/', OfferSearch.as_view(), name='offersearch'),
]
