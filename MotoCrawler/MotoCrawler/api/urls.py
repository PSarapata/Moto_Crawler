from django.urls import path
from .views import OfferList, OfferDetail

urlpatterns = [
    path('<int:pk>/', OfferDetail.as_view(), name='detailview'),
    path('', OfferList.as_view(), name='listview'),
]
