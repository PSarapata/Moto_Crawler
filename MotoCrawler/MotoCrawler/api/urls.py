from django.urls import path
from .views import OfferList, OfferDetail, PhotoList, PhotoDetail, OfferPhotosList, BlacklistTokenView, OfferSearch


urlpatterns = [
    path('<int:pk>/', OfferDetail.as_view(), name='detailview'),
    path('', OfferList.as_view(), name='listview'),
    path('photos/', PhotoList.as_view(), name='photolistview'),
    path('photos/<int:pk>/', PhotoDetail.as_view(), name='photodetailview'),
    path('offerphotos/<int:pk>/', OfferPhotosList.as_view(), name='offerphotos'),
    path('user/logout/blacklist/', BlacklistTokenView.as_view(), name='blacklist'),
    path('search/', OfferSearch.as_view(), name='offersearch'),
]