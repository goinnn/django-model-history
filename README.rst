django-model-history
====================

Enable in any Model class an change history of all inserts, updates and deletes

Installation
============


In your models.py
-----------------

Only you have to update the parent class of your model.

::
    from django.db import models


    class MyModel(models.Model):
        ....



::

    from model_history.models import ModelHistoryProvider


    class MyModel(ModelHistoryProvider):
        ....

    ...




In your settings.py
-------------------

Only you need it, if you want the translation of django-model-history

::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.admin',

        #.....................#

        'model_history',
    )


Development
===========

You can get the last bleeding edge version of django-model-history by doing a clone
of its git repository::

  git clone https://github.com/goinnn/django-model-history


Example project
===============

In the source tree, you will find a directory called  `example <https://github.com/goinnn/django-model-history/tree/0.1.0/example/>`_. It contains
a readily setup project that uses django-model-history. You can run it as usual:

::

    python manage.py makemigrations
    python manage.py syncdb --noinput
    python manage.py runserver


Access in a browser to http://localhost:8000/