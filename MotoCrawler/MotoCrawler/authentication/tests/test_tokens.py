"""Testing tokens"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import json
import pytest

from authentication.models import MotoCrawlerUser


@pytest.fixture
def authenticated_client():
    """Create authenticated user for testing."""
    user = MotoCrawlerUser.objects.get_or_create(username='john_doe', email='john@doe.com')[0]
    user.set_password(raw_password='john.doe')
    user.save()
    client = APIClient()
    client.cache = {}
    url = reverse('token_create')
    response = client.post(url, {"username": "john_doe", "password": "john.doe"})
    data = json.loads(response.content.decode('utf-8'))
    token = data['access']
    client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    client.cache['access'] = data['access']
    client.cache['refresh'] = data['refresh']
    return client


@pytest.mark.django_db
def test_token_create():
    """Test that token pair create view issues user with a pair of access & refresh tokens."""
    user = MotoCrawlerUser.objects.get_or_create(username='johndoe', email='john.doe@johndoe.com')[0]
    user.set_password('johndoepassword')
    user.save()
    client = APIClient()
    url = reverse('token_create')
    response = client.post(url, {'username': 'johndoe', 'password': 'johndoepassword'})
    data = json.loads(response.content.decode())
    assert response.status_code == status.HTTP_200_OK
    assert "access" in data
    assert "refresh" in data


@pytest.mark.django_db
def test_token_refresh(authenticated_client):
    """Ensure that POSTing a refresh token issues user with a fresh Access token."""
    refresh_view = reverse('token_refresh')
    response = authenticated_client.post(refresh_view, {'refresh': authenticated_client.cache["refresh"]})
    access_token = authenticated_client.cache['access']
    print(access_token)
    data = json.loads(response.content.decode())
    assert response.status_code == status.HTTP_200_OK
    assert data['access'] != access_token


@pytest.mark.django_db
def test_blacklist_view(authenticated_client):
    """Ensure that user logout is handled correctly.
    Please note that refresh token is being blacklisted, and access is granted by the 5 minute-lifespan access token."""
    blacklist_url = reverse('blacklist')
    response = authenticated_client.post(blacklist_url, {"refresh_token": authenticated_client.cache["refresh"]})
    assert response.status_code == status.HTTP_205_RESET_CONTENT

    #  Ensure that after successful logout, user will not be able to access protected views.
    hello_view = reverse('hello_world')
    #  Clear authorization headers
    authenticated_client.credentials()
    response = authenticated_client.get(hello_view)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
