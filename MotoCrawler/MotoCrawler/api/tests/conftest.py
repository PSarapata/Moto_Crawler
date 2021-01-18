from authentication.models import MotoCrawlerUser
from api.models import Offer, Photo, OfferPhoto, UserFavouriteOffer
from rest_framework.test import APIClient
import json
import pytest
from faker import Faker, Factory
from faker_vehicle import VehicleProvider

faker = Factory.create()
fakeCar = Faker()
fakeCar.add_provider(VehicleProvider)


@pytest.fixture
def api_client():
    """Returns authenticated MotoCrawlerUser instance for tests"""
    user = MotoCrawlerUser.objects.get_or_create(username='john', email='js@js.com')[0]
    user.set_password(raw_password='js.js')
    user.save()
    client = APIClient()
    response = client.post("http://testserver/api/token/obtain/", {"username": "john", "password": "js.js"})
    response_content = json.loads(response.content.decode('utf-8'))
    token = response_content["access"]
    client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    return client


@pytest.fixture
def make_offer():
    """Create an Offer instance for tests"""

    offer = Offer.objects.create(url=faker.url(), brand=fakeCar.vehicle_make(), model=fakeCar.vehicle_model(),
                                 title=fakeCar.vehicle_year_make_model(),
                                 price=faker.random_number(digits=5, fix_len=True),
                                 description=fakeCar.vehicle_year_make_model_cat())
    return offer


def make_photos():
    """Returns a tuple of Photo instances for testing."""
    photos = []

    def create_sample_photos(count=5):
        for number in range(count):
            photo = Photo.objects.create(url=faker.url())
            photos.append(photo)
        return photos
    return create_sample_photos()


@pytest.fixture
def make_offerphoto_relation(make_offer):
    photos = make_photos()
    offer_photo_objects = []
    for instance in photos:
        offerphoto = OfferPhoto.objects.create(offer=Offer.objects.first(), photo=instance)
        offer_photo_objects.append(offerphoto)
    return offer_photo_objects
