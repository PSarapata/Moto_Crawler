Core
====

Core is the source of Django MotoCrawler project. This is where you will find the all-so-important settings.py file.
You might also be interested with urls.py, which lists all endpoints available in the application, and celery.py,
hosting custom Celery settings.

Django Settings
---------------

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'django_extensions',
        'api',
        'rest_framework',
        'corsheaders',
        'authentication',
        'rest_framework_simplejwt.token_blacklist',
        'django_filters',
    ]

These are all applications added on top of the django's defaults. Note that django_filters are currently not being
used in the project.

Because the project is using Django CorsHeaders, be sure to include this in your MiddleWare:

.. code-block:: python

    MIDDLEWARE = [
        # ...
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        # ...
    ]

Exactly in the position shown above.

Furthemore, you need to allow origin of the FrontEnds that will be consuming the project's API.
As the project is being run locally, that is localhost on port 3000:

.. code-block:: python

    # CorsHeaders
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000"
    ]

MotoCrawler is using SimpleJWT token authentication, hence it is prudent to specify few settings for those tokens to
work as intended:

.. code-block:: python

    # JWT TOKEN SETTINGS (AUTHENTICATION)
    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
        'ROTATE_REFRESH_TOKENS': True,
        'BLACKLIST_AFTER_ROTATION': False,
        'ALGORITHM': 'HS256',
        'SIGNING_KEY': SECRET_KEY,
        'VERIFYING_KEY': None,
        'AUTH_HEADER_TYPES': ('JWT',),
        'USER_ID_FIELD': 'id',
        'USER_ID_CLAIM': 'user_id',
        'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
        'TOKEN_TYPE_CLAIM': 'token_type',
    }

Notice the use of Django's secret key as a signing key. It is important that it does not get compromised, otherwise
User's data would be at risk.

Since MotoCrawler project is based on RESTful API, those settings come in handy. Pagination and project-level
permissions are purely voluntary (You could go for *IsAuthenticatedOrReadOnly* instead), however if we want to run JWT
tokens, *'DEFAULT_AUTHENTICATION_CLASSES'* step should not be ommitted:

.. code-block:: python

    # REST FRAMEWORK SETTINGS
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        # LIMIT RESULTS PER PAGE TO 100 ITEMS
        'PAGE_SIZE': 100,
        # PROJECT-WIDE PERMISSIONS - LIMIT VIEWS TO AUTHENTICATED USERS ONLY. CAN BE OVERRIDDEN ON VIEW LEVEL.
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        # AUTHENTICATION UTILIZES JWT TOKENS
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
    }

Finally, a reminder: don't forget to specify a **database** for your project. MotoCrawler is ran on **PostgreSQL**,
however with some changes, it should be possible to run it with a different SQL engine.

MotoCrawler's URLS
-------------------

Here's a list of all available endpoints:

.. code-block:: python

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

Celery
--------
*Currently unsupported*