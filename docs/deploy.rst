Deploy
========
Tripplan (Get Yr Beta) is deployed on Heroku.
Heroku git repo: https://git.heroku.com/getyrbeta.git
To deploy: $ git push heroku master


Heroku
-----------------------------
* Dependencies. Heroku requires a 'requirements.txt' file in the root directory that lists
  all the dependencies. To meet the Heroku requirement and maintain the
  preferred file structure, the ROOT/requirements.txt is just a pointer
  to requirements/production.txt.

* Heroku requires Procfile to exist and be in the ROOT directory

* Secrets. Add all environmental variables to Heroku before attempting to run
  commands. This is currently done manually through the Heroku dashboard.
  env.example shows a list of the variables that must be defined.

* Database. A postgres database was created as a Heroku resource. Heroku
  automatically creates a database url and saves it to a config variable.
  The database url must be copied to the config var: DATABASE_URL.

* The deployed url must be added to ALLOWED_HOSTS in config/settings/production.py

* Create a super user to enable access to the admin

* SSL certificate. Handled by Heroku. Enabled by: $ heroku certs:auto:enable

Facebook
---------------
Get Yr Beta allows a user to log in using a facebook account. After deploying
on Heroku, the following steps are required to setup Facebook:

* developers.facebook.com

  #) Ensure app domains are added to the section: "App Domains."

  #) Ensure the website url is added

  #) Grap the App ID and App Secret

* getyrbeta.com/admin

  #) Sites: add the domain name

  #) SOCIAL ACCOUNTS -> Social applications: Create Facebook and add relevant
     info from developers.facebook.com

Google Maps
-----------
Get Yr Beta uses Google maps API for trip locations. The API key must be
entered as a Heroku config variable.

Mailgun
-------
Get Yr Beta uses django-anymail to keep the code mail-server-agnostic. The
specific mailserver settings are entered as environmental variables,
specifically DJANGO_MAILGUN_API_KEY.
