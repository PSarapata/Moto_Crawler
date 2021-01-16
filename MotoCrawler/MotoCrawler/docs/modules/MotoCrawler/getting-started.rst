Getting Started
===============

This section will give you an overview on how to communicate with MotoCrawler API and hopefully will allow you to
consume it with ease.

Let's get to it, shall we?

First thing you need to know before we start, is that MotoCrawler has a project-wide IsAuthenticated permission class
. That means you need a JWT token to access most resources.

Let's suppose you are trying to access the

Base URL
--------

This is the main resource of MotoCrawler, the list of scraped car offers:

.. code-block::

    http://localhost:8000/api/

If you make a request to this URL, the standard response you should get would be as follows:

.. code-block:: json

    {
        "detail": "Authentication credentials were not provided."
    }

As mentioned above, you first need to log in and pass a JWT token with your request.
Simply follow the steps in next subsection and your screen should then show something like that:

.. code-block:: json

    {
        "count": 98,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "url": "https://www.autoscout24.pl/oferta/mitsubishi-eclipse-benzyna-niebieski-33d3c696-a88f-4126-8efe-e3a7f74b8486",
                "brand": "Mitsubishi",
                "model": "Eclipse",
                "title": "Mitsubishi Eclipse",
                "price": "€ 2.800,-",
                "description": null,
                "photo_urls": [
                    "https://prod.pictures.autoscout24.net/listing-images/33d3c696-a88f-4126-8efe-e3a7f74b8486_42dd3f43-3b48-43ea-89cc-282153a9d289.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/33d3c696-a88f-4126-8efe-e3a7f74b8486_abdc7d16-32d2-4fcc-920d-b8212d08bb11.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/33d3c696-a88f-4126-8efe-e3a7f74b8486_96b2e5f9-a9f2-406d-b8e8-55db0d7d1020.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/33d3c696-a88f-4126-8efe-e3a7f74b8486_029fdc1d-f101-4081-bc0b-9f1e62737653.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/33d3c696-a88f-4126-8efe-e3a7f74b8486_dd2b8476-bd43-4659-bae8-833957084ea3.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/33d3c696-a88f-4126-8efe-e3a7f74b8486_a2e12a22-4b15-4f3c-86a0-524f70b1ce3e.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/33d3c696-a88f-4126-8efe-e3a7f74b8486_e76f73f9-bce7-4465-b9d9-fe8dbb80ae6a.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/33d3c696-a88f-4126-8efe-e3a7f74b8486_a42c5909-636c-4b72-bd31-dac4136c3a68.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/33d3c696-a88f-4126-8efe-e3a7f74b8486_0402cfb4-5e5a-413a-aec6-b439b7e312e8.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/33d3c696-a88f-4126-8efe-e3a7f74b8486_73e010d9-d094-4d01-beac-144e4d1de4d3.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/33d3c696-a88f-4126-8efe-e3a7f74b8486_3a0d3451-939c-4d7e-9c6f-e9aeb7c1d38f.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/33d3c696-a88f-4126-8efe-e3a7f74b8486_a5f6619d-a30f-4ef6-85ed-6a36e2e72226.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/33d3c696-a88f-4126-8efe-e3a7f74b8486_68edd99a-3200-46ec-b48f-4f16bc049be3.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/33d3c696-a88f-4126-8efe-e3a7f74b8486_aa8b4af7-be1a-46fa-a426-0cc83d516121.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/33d3c696-a88f-4126-8efe-e3a7f74b8486_5673d746-8ebf-438d-933f-1dadbd8018bf.jpg/640x480.jpg"
                ]
            },
            {
                "id": 2,
                "url": "https://www.autoscout24.pl/oferta/mitsubishi-eclipse-2000-gs-16v-benzyna-niebieski-326ad816-5975-4bbe-9317-274cf162820b",
                "brand": "Mitsubishi",
                "model": "Eclipse",
                "title": "Mitsubishi Eclipse 2000 GS-16V",
                "price": "€ 1.399,-",
                "description": null,
                "photo_urls": [
                    "https://prod.pictures.autoscout24.net/listing-images/326ad816-5975-4bbe-9317-274cf162820b_27cab634-618a-4f6c-9e34-874e0bcbb60e.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/326ad816-5975-4bbe-9317-274cf162820b_2eae84a3-245a-4f61-aa9a-a3addd6c987d.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/326ad816-5975-4bbe-9317-274cf162820b_d49dab4a-ea82-4e18-92cb-55986764fe95.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/326ad816-5975-4bbe-9317-274cf162820b_0bd38273-7216-4fed-8ecf-eea5a155cc54.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/326ad816-5975-4bbe-9317-274cf162820b_4cf6792a-27c7-4deb-984b-384e08da0cf7.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/326ad816-5975-4bbe-9317-274cf162820b_92039bff-e8e8-493a-9c45-c278a1672065.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/326ad816-5975-4bbe-9317-274cf162820b_044436eb-8940-4214-b305-ffe18630007a.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/326ad816-5975-4bbe-9317-274cf162820b_8b9b9370-861c-4a0e-b2e8-d19efa7ff41e.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/326ad816-5975-4bbe-9317-274cf162820b_62824abd-8258-4a2b-a522-389eb84a6b43.jpg/640x480.jpg"
                ]
            },
            {
                "id": 3,
                "url": "https://www.autoscout24.pl/oferta/mitsubishi-3000-gt-3-0-stealth-benzyna-czerwony-fe27bab2-2153-9575-e053-0100007f08c6",
                "brand": "Mitsubishi",
                "model": "3000-GT",
                "title": "Mitsubishi 3000 GT 3.0 stealth",
                "price": "€ 4.986,-",
                "description": null,
                "photo_urls": [
                    "https://prod.pictures.autoscout24.net/listing-images/fe27bab2-2153-9575-e053-0100007f08c6_b7879235-0263-4455-b129-36451d8afae8.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/fe27bab2-2153-9575-e053-0100007f08c6_f3d9dd3d-5176-4d11-a3b7-b5a5f4470b79.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/fe27bab2-2153-9575-e053-0100007f08c6_8ce96704-3ca9-4846-ac85-d76e45051f18.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/fe27bab2-2153-9575-e053-0100007f08c6_a84ad4ae-2b62-4182-8a00-aa9511a78c23.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/fe27bab2-2153-9575-e053-0100007f08c6_516d810e-7083-4974-bc63-c868d4e3b4d1.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/fe27bab2-2153-9575-e053-0100007f08c6_5e840e43-897d-4864-8e95-0ec82f56a040.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/fe27bab2-2153-9575-e053-0100007f08c6_e9afa7de-eec5-4cb0-aef7-33855d4ef997.jpg/640x480.jpg",
                    "https://prod.pictures.autoscout24.net/listing-images/fe27bab2-2153-9575-e053-0100007f08c6_034ce903-60c9-4b3a-9e1a-6508506d4afa.jpg/640x480.jpg"
                ]
            },
            {...}
    }

Authentication
--------------
Authentication in MotoCrawler is utilizing simple JWT tokens. First, register yourself, by POSTing your user data to

.. code-block::

    http://localhost:8000/api/user/create

Simply, pass the data in a dictionary:

.. code-block:: json

    {
        "username": "user"
        "email": "email@email.com"
        "password": "password"
    }

Once you've registered your account, go to:

.. code-block::

    http://localhost:8000/api/token/obtain

passing your user credentials (username and password in a dictionary format) along with the request.

You should be issued with a pair of tokens:

.. code-block:: json

    {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
                eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjA0NTYxMCwianRpIjoiOGI3ZDcwZDdjZTMwNGU2Y2EyNDZiMTRlOTE1MTE5NWMiLC
                J1c2VyX2lkIjozfQ.1gcSDjW0CPDlZ2ogiYcB-XcWOxyFoe24TIkOr6ot7i4",
    "access":  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
                eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjEwODM2MzEwLCJqdGkiOiI0YWJlZGQ3NWYyY2M0NDU0OTQxZjYxZjM1ZGU2ZDAyZiIsIn
                VzZXJfaWQiOjN9.vfzvpE-VZdiLYlZEFCMylDsSccp9H0bDizCMqs7OlGw"
    }

Now, all you need to do is to pass a token along with each request you make. To do that, grab your **ACCESS** token
and stick it into your Request's **HEADERS**. It has to be passed as **Authorization** key, with a value of **JWT
{access_token}** Notice the whitespace between the two, it is extremely important! You should also specify
**Content-Type** as **application/json**.

.. code-block::

    Headers:

        "Content-Type": "application/json"
        "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXN{...}"

Now you should be able to access protected views. If you are still struggling, please contact customer service
(except... There isn't one ;D).

It is worth to mention that the /favourites endpoint is only accessible by you. Noone else can view your stored offers.
Happy days!