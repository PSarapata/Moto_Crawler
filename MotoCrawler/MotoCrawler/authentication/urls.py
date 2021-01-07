from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from authentication.views import MotoCrawlerUserCreate, HelloWorldView

urlpatterns = [
    path('user/create/', MotoCrawlerUserCreate.as_view(), name='create_user'),
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', HelloWorldView.as_view(), name='hello_world')
]