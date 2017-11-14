Install
=========

Source code is located here:
https://github.com/djcroissant/getyrbeta

Follow these steps to setup a local copy of Get Yr Beta:
#) Clone the repo onto local machine:
   https://github.com/djcroissant/getyrbeta.git
#) Make a virtual environment and install dependencies from
   requirements/local.txt
#) Create postgresql database. Database url in settings/base.py:
    postgres://tripplan:optoutside!@127.0.0.1:5432/tripplandb
#) Migrate database: $ python manage.py migrate
#) Create superuser
#) Run local tasks with settings/local.py:
  * $ python manage.py shell --settings=config.settings.local
  * $ python manage.py runserver --settings=config.settings.local
#) Facebook. Log into admin with superuser account to add the following:
  * Sites: add the domain name: 127.0.0.1:8000
  * SOCIAL ACCOUNTS -> Social applications: Create Facebook and add:
    * Client id: 1974308959508610
    * Secret key: 4afd22969c3ecfed032e3b545441fab0
    * Sites: add 127.0.0.1:8000
