from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import pytest
import json


@pytest.mark.django_db
def test_project_permissions():
    """Ensure unauthenticated users cannot view offers."""

    url = reverse('listview')
    client = APIClient()
    response = client.get(url, format='json')
    assert (response.status_code == status.HTTP_401_UNAUTHORIZED)


@pytest.mark.django_db
def testing_fixture(api_client):
    """Testing whether our fixture allows us to enter main API resource."""

    url = reverse('listview')
    response = api_client.get(url)
    assert (response.status_code == status.HTTP_200_OK)


@pytest.mark.django_db
def test_pagination(api_client):
    """Testing if pagination is applied."""

    url = reverse('listview')
    response = api_client.get(url)
    data = json.loads(response.content.decode())
    assert "next" in data
    assert "previous" in data


@pytest.mark.django_db
def test_authentication(api_client):
    """Ensure that authenticated user is able to access protected views and read content."""

    hello = reverse('hello_world')
    url = 'http://testserver%s' % hello
    response = api_client.get(url)
    data = json.loads(response.content.decode())
    assert response.status_code == status.HTTP_200_OK
    assert data["hello"] == "world"


@pytest.mark.django_db
@pytest.mark.usefixtures('make_offer')
def test_offer_content(api_client):
    """Ensure that a user can actually see a list of available offers at /api endpoint and that at least 1 Offer
    object is stored in the database."""

    url = reverse('listview')
    response = api_client.get(url)
    data = json.loads(response.content.decode())
    assert len(data["results"]) >= 1


@pytest.mark.django_db
@pytest.mark.usefixtures('make_offer')
def test_offer_details(api_client):
    """
    Ensure that our user can access offer details page and is able to find all relevant information there.
    Data is a dictionary, hence assertion to see if all expected keys can be found in the response.
    """

    offer_detail_url = reverse('detailview', args=[2])
    response = api_client.get(offer_detail_url)
    data = json.loads(response.content.decode())
    expected_keys = {
        'id',
        'url',
        'brand',
        'model',
        'title',
        'price',
        'description',
        'photo_urls'
    }

    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == 2
    assert all(key in data for key in expected_keys)
