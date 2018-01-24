Install
=========

Source code is located here:
https://github.com/djcroissant/getyrbeta

Follow these steps to setup a local copy of Get Yr Beta:
#) Clone the repo onto local machine: https://github.com/djcroissant/getyrbeta.git

#) Make a virtual environment and install dependencies from requirements/local.txt

    * Note, WeasyPrint has additional dependencies that must be installed separately.
    More info here: https://github.com/djcroissant/getyrbeta/blob/master/docs/install.rst

    * Installation relies on homebrew. Run the following command:

    brew install cairo pango gdk-pixbuf libffi

#) Create PostgreSQL database.

    * Excellent tutorial here: https://www.codementor.io/devops/tutorial/getting-started-postgresql-server-mac-osx

#) Create .env file in base directory. It will follow the format in env.example.

#) Using the log in credentials for your PostgreSQL database, assign the DATABASE_URL environmental variable in the .env file

#) Assign the DJANGO_SECRET_KEY environmental variable in the .env file.

#) Migrate database: $ python manage.py migrate

#) Create superuser

#) Run local tasks with settings/local.py:
  * $ python manage.py shell --settings=config.settings.local
  * $ python manage.py runserver --settings=config.settings.local

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
