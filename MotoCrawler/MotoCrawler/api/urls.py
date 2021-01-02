from django.urls import path
from .views import OfferList, OfferDetail, PhotoList, OfferPhotosList

urlpatterns = [
    path('<int:pk>/', OfferDetail.as_view(), name='detailview'),
    path('', OfferList.as_view(), name='listview'),
    path('photos/', PhotoList.as_view(), name='photolistview'),
    path('offerphotos/<int:pk>/', OfferPhotosList.as_view(), name='offerphotos')
]
