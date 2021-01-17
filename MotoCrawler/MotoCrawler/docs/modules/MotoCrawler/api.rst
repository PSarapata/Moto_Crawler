API
======

If core is the heart of MotoCrawler, API is its' brain. This is where the magic happens, and majority of
most seeked-after resources sit in API's views.

If you are having trouble viewing API's resources, familiarise yourself with :ref:`getting_started` section.


Models
------

API defines 4 django class models:

Offer
^^^^^
Offer resource is a single instance of a car advert scraped from one of the source car selling websites.

**Endpoints**
    * /api/ --> API's main view, list of all offers from the database
    * /api/:id/ --> detailed single offer view
    * /api/ search/ --> Offer search view, searching must "start_with" your phrase and scans offers for matching
      **brand** or **model**

**Attributes**

    * *pk* : int - Unique Identifier
    * *url* : string - URL of the offer
    * *brand* : string - brand of the car being the offer's subject
    * *model* : string - model of the car being the subject of the offer
    * *title* : string - offer's title
    * *price* : string - price in a format specified by the car website. It may differ between offers!
    * *description* : string - offer's textual description, usually providing detailed information about the
      advertised car.

**Permissions**
    *IsAuthenticated*

If you are interested in how to authenticate your requests within MotoCrawler, please read the :ref:`getting_started`
section.

**Search Fields**

    * **brand**
    * **model**

**Relations**
    * **Offer -- Photo**
    * **Offer -- MotoCrawlerUser**

Photos
^^^^^^

Photo resource is a single photograph, tied to the offer by a foreign key.

**Endpoints**
    * api/ photos/  --> Lists all available Photo resources
    * api/ photos/:pk/ --> Access a single Photo resource view

**Attributes**

    * *pk* : int - Primary Key of a Photo resource
    * *offer* : int - Foreign Key of the Offer
    * *url* : string - URL of a Photo resource

**Permissions**
    *IsAuthenticated*

**Relations**
    * **Photo -- Offer**

OfferPhoto
^^^^^^^^^^

OfferPhoto is an auxiliary resource, its' purpose it to link Offer and Photo instances.

**Endpoints**
    * api/ offerphotos/:pk>/ --> Lists all photos related to a particular Offer resource. **The PK sent to this
      endpoint is one of the Offer!**

**Attributes**

    * *pk* : int -- Primary Key of OfferPhoto resource
    * *offer* : int -- Foreign Key to the Offer instance
    * *photo* : int -- Foreign Key to the Photo instance

**Permissions**
    *IsAuthenticated*

UserFavouriteOffer
^^^^^^^^^^^^^^^^^^

This one is a blast. It links your Authenticated User with his/hers favourite offers. Views are based on
django_rest_framework's custom ModelViewSets, and since it might be a bit tricky to figure it out, the code for this
is included below.

**Endpoints**
    * ^favourites/$ --> Lists User's favourite offers.
    * ^favourites/(?P<pk>[^/.]+)/$ --> Details of a single related (favourite) offer.

**Attributes**

    * *pk* : int -- Primary Key of FavouriteUserOffer resource
    * *offer* : int -- Foreign Key of the Offer instance
    * *user* : int -- Foreign Key of the MotoCrawlerUser instance
    * *timestamp* : datetime -- "Created at" field, gives an indication on when the offer was added as favourites.

**Code**

.. code-block:: python

        class UserFavouriteOfferViewSet(viewsets.ModelViewSet):
            """Custom Viewset to manage User-FavouriteOffers relation.
            ManageFavouriteOfferPermission applies:
            User has to be authenticated and a holder of a matching User Foreign Key
            to be able to use this view."""
            permission_classes = [ManageFavouriteOfferPermission]
            serializer_class = FavouriteOfferSerializer

            #  Retrieve/Update/Destroy, get a single item based on related object's ID.
            def get_object(self, queryset=None, **kwargs):
                item = self.kwargs.get('pk')
                return get_object_or_404(UserFavouriteOffer, pk=item)

            # List only Offers related to authenticated User.
            def get_queryset(self):
                return get_list_or_404(UserFavouriteOffer, user=self.request.user)

**Permissions**
    *ManageFavouriteOfferPermission*

The custom permission applies to this view. Have a look through its' code below:

.. code-block:: python

    class ManageFavouriteOfferPermission(BasePermission):
        """
        Custom Permission limiting object modifications on an object
        to its' legitimate owner user only.
        Returns true if the User Primary Key passed along with the request matches
        the User Foreign Key of UserFavouriteOffer instance.
        User has to be authenticated.

        :param: request: HTTP request
        :type request: request: HTTP request
        :param: view: Used on :class: 'UserFavouriteOfferViewSet' ModelViewSet.
        :type view: class: 'UserFavouriteOfferViewSet'
        :param: obj: Authorized User database object (model)
        :obj type: object: 'MotoCrawlerUser'
        :return: Boolean
        """
        message = 'Viewing favourite offers is only allowed for their owner.'

        def has_object_permission(self, request, view, obj):
            return obj.pk == request.user


**Relations**
    * **MotoCrawlerUser -- Offer**