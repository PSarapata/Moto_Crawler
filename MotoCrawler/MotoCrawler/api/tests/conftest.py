from authentication.models import MotoCrawlerUser
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

import pytest


@pytest.fixture
def api_client():
    user = MotoCrawlerUser.objects.create_user(username='john', email='js@js.com', password='js.sj')
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(AUTHORIZATION=f'JWT {refresh.access_token}')

    return client
