from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import pytest
from conftest import api_client


class OfferTest(APITestCase):

    def test_project_permissions(self):
        """Ensure only authenticated users can view offer list."""
        url = reverse('listview')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


@pytest.mark.django_db
def test_authentication(api_client=api_client):
    """Check that authenticated user is able to see offers."""

    url = reverse('hello_world')
    response = api_client.get(url)
    data = response.data
    assert response.status_code == status.HTTP_200_OK
    assert data == "world"
