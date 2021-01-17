Authentication
==============

Authentication is MotoCrawler's submodule. It defines a custom MotoCrawlerUser model and hosts rest framework's
simple JWT access and refresh token related endpoints.

If you are struggling to authenticate yourself, take a step back to :ref:`getting_started` section.

Models
------

MotoCrawlerUser
^^^^^^^^^^^^^^^

This is the authorized user model for MotoCrawler project, as defined in Django's settings file:

.. code-block:: python

    # Custom user model for authentication:
    AUTH_USER_MODEL = "authentication.MotoCrawlerUser"


**Attributes**

Besides all the standard inherited fields from the generic Django AbstractUser, it defines a Many-To-Many relation
with API's Offer resource:

.. code-block:: python

        # MotoCrawlerUser extends from base Django user. I used it for authentication, following this tutorial:
    # "https://hackernoon.com/110percent-complete-jwt-authentication-with-django-and-react-2020-iejq34ta"
    # I then had an idea to create a relation so a user can store/watch his favourite offers:
    class MotoCrawlerUser(AbstractUser):
        favourite_offers = models.ManyToManyField("api.Offer", through="api.UserFavouriteOffer")

Views
^^^^^

As mentioned, authentication hosts majority of token-related endpoints, but also a very simple "Hello-World" View,
built with testing in mind.

**Endpoints**

    * *api/ user/create/* --> register (create) a new MotoCrawlerUser
    * *api/ token/obtain/* --> get a pair of **access** and **refresh** tokens
    * *api/ token/refresh/* --> get a new **access** token (access tokens expire after 5 minutes!)
    * *api/ user/logout/blacklist/* --> blacklist User's tokens.
    * *api/ hello/* --> test "hello world" view

**Permissions**
    * *api/ user/create/ == AllowAny*
    * *api/ token/obtain/ == Allows POST requests with a dictionary of "username" and "password" key/value pairs*
    * *api/ token/refresh/ == Allows POST requests with a dictionary of "refresh" token key/value, returns fresh tokens*
    * *api/ user/logout/blacklist/ == AllowAny, allows POST request with "refresh_token" key/value, returns
      RESET_CONTENT_205 response on success*
    * *api / hello/ == IsAuthenticated*

**HelloWorld**

.. code-block:: python

    class HelloWorldView(APIView):
        """
        Simple Test View, displaying a pseudo-dictionary key-value pair 'hello: world'.
        Comes in handy when testing authentication-related issues. Sits under 'hello/' endpoint.
        :return: pseudo-dict{"hello":"world"} & HTTP_200_OK response
        """
        def get(self, request):
            return Response(data={"hello": "world"}, status=status.HTTP_200_OK)
