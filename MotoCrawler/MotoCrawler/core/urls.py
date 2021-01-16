"""
MotoCrawler Endpoints:

    admin/
    api/ <int:pk>/ [name='detailview']
    api/ [name='listview']
    api/ photos/ [name='photolistview']
    api/ photos/<int:pk>/ [name='photodetailview']
    api/ offerphotos/<int:pk>/ [name='offerphotos']
    api/ user/logout/blacklist/ [name='blacklist']
    api/ search/ [name='offersearch']
    api/ user/create/ [name='create_user']
    api/ token/obtain/ [name='token_create']
    api/ token/refresh/ [name='token_refresh']
    api/ hello/ [name='hello_world']
    ^favourites/$ [name='favourite_offers-list']
    ^favourites\.(?P<format>[a-z0-9]+)/?$ [name='favourite_offers-list']
    ^favourites/(?P<pk>[^/.]+)/$ [name='favourite_offers-detail']
    ^favourites/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='favourite_offers-detail']
    ^$ [name='api-root']
    ^\.(?P<format>[a-z0-9]+)/?$ [name='api-root']

"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserFavouriteOfferViewSet

router = DefaultRouter()
router.register('favourites', UserFavouriteOfferViewSet, basename='favourite_offers')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/', include('authentication.urls')),
    path('', include(router.urls)),
]
