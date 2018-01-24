Get Yr Beta
=====================

:License: GPLv3


Get Yr Beta is a web application to facilitate, automate, and coordinate
planning logistics for outdoor adventures. The idea stemmed from
weekly group meetings with the Boeing Alpine Club, Boealps, where groups
went through the trip planning process weekly. Collecting numbers for
the local sheriff's office, organizing carpools, and assigning group gear
was always clunky and usually took longer than anyone wanted. Get Yr Beta
was born as a tool to streamline this process and get everyone out to
9lb Hammer sooner than later.


Primary information included in Get Yr Beta:
---------------------------------------------
* Trip members

* Starting point

* Objectives

* Group gear

* Emergency contacts - both personal and external (i.e. Sheriff's office)

* Vehicle information

* Carpools


Typical flow for user to organize a new trip
----------------------
#) Sign up for an account

#) Fill out user profile (User info, Emergency contact, Vehicle info)

#) Make a new trip

#) Add members

#) Check emergency info *- future functionality*

#) Check vehicle info *- future functionality*

#) Assign gear *- future functionality*

#) Check trip plan *- future functionality*


Settings
--------
Moved to:

  * config/settings/base.py

  * config/settings/local.py

  * config/settings/test.py

  * config/settings/production.py


base.py is inherited by all other files. Developers should run the app using
local.py. Testing uses test.py. The app is deployed using production.py. The
settings files are setup this way to ensure all development is done with the
same settings. All local and base settings are checked into version control.
The production settings make use of environmental variables stored in .env,
which is not checked into version control. To see an example of what is in
.env, check out env.example.


Basic Commands
--------------

Setting Up Users
^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the
  form. Once you submit it, an email confirmation will be emailed with a link
  to verify the email address. This step is currently optional, but will become
  mandatory in a future version. The email along with verification link
  will be printed in the console.

* To create a **superuser account**, use this command::

    $ python manage.py createsuperuser


Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Note that testing is currently limited to functional tests. Integration tests
will coming soon!


Installation for development
----------------------------
see `installation <docs/install.rst>`_


Deployment
----------
see `deployment <docs/deploy.rst>`_


General layout
--------------
Project layout is based on Cookie Cutter Django
https://github.com/pydanny/cookiecutter-django
