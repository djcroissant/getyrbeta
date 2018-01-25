=========
Install
=========

Source code is located here:
https://github.com/djcroissant/getyrbeta

Follow these steps to setup a local copy of Get Yr Beta:

Clone the repo onto local machine
+++++++++++++++++++++++++++++++++

.. code::

  git clone https://github.com/djcroissant/getyrbeta.git

Setup your environment
++++++++++++++++++++++

Mac OSX:
--------

Make a virtual environment and install dependencies.  

Note: This project uses WeasyPrint which requires additional dependencies.  You must have brew installed and the bundle command will install packages into your *host environment*!  
  
.. code::

  pip3 -r requirements/local.txt
  brew bundle

Postgres
--------

Create PostgreSQL database using your favourite method, this `excellent tutorial <https://github.com/djcroissant/getyrbeta.git>`_ or use the docker method below.  Please refer to the `docker resources <https://docs.docker.com/docker-for-mac/install/>`_ for installing and using docker like on OSX.

.. code::

  CONTAINER_NAME=getyrbeta_db_1
  DATABASE_NAME=getyrbeta
  docker-compose
  CONTAINER_IP=$(docker-machine inspect --format='{{.Driver.IPAddress}}')
  DATABASE_URL=postgres://postgres:password@$CONTAINER_IP:5432
  docker exec -it getyrbeta_db_1 psql $DATABASE_URL -c "CREATE DATABASE $DATABASE_NAME"
  echo -e "\n---\nPostgres is now ready at: $DATABASE_URL/$DATABASE_NAME\n---"

Use the output URL for the next section to configure your DATABASE_URL.

Django
------

Copy `env.example <env.example>`_ to .env and edit the .env file with your development data.  Use the comments within the file for help.

DATABASE_URL
  Defines where to find the database using the postgres format (see env.example)

DJANGO_SECRET_KEY
  This is your own unique key for this project and can be generated online or locally.

Leave other variables empty unless you plan to use the mapping or mail features.

Now django can be setup for first time use:

.. code::

  python manage.py migrate
  python manage.py createsuperuser
  python manage.py shell --settings=config.settings.local

To start the server now (and in the future):

.. code::

  python manage.py runserver --settings=config.settings.local


Facebook
---------------
Get Yr Beta allows a user to log in using a facebook account. Create a
developer account at https://developers.facebook.com/. Then complete the
following steps:

* At developers.facebook.com

  #) Ensure app domains are added to the section: "App Domains."

  #) Ensure the website url is added

  #) Grap the App ID and App Secret

* Log in to GetYrBeta admin as a super user to complete the following:

  #) Sites: add the domain name: 127.0.0.1:8000

    * Note that the index of site must match what is set in the settings variable SITE_ID


  #) SOCIAL ACCOUNTS -> Social applications: Create Facebook and add:

    * Client id: (From Facebook account)

    * Secret key: (From Facebook account)

    * Sites: add 127.0.0.1:8000

Google Maps
-----------
Get Yr Beta uses Google maps API for trip locations. Get an API key from
https://developers.google.com/places/javascript/. Assign this key to the
GOOGLE_MAPS_API environmental variable in the .env file.

Mailgun
-------
Mailgun credentials are not required for development. All emails will be
snubbed and displayed in the terminal. Mailgun setup is described for
production in docs/deploy.rst.

Easy PDF
--------
Currently using development version v0.2.0-dev1. It uses the WeasyPrint backend,
which makes rendering templates to pdfs simple.
