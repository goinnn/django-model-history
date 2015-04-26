django-model-history
====================

.. image:: https://travis-ci.org/goinnn/django-model-history.png
    :target: https://travis-ci.org/goinnn/django-model-history

.. image:: https://coveralls.io/repos/goinnn/django-model-history/badge.png
    :target: https://coveralls.io/r/goinnn/django-model-history

.. image:: https://badge.fury.io/py/django-model-history.png
    :target: https://badge.fury.io/py/django-model-history

Enable in any Model class an change history of all inserts, updates and deletes

Installation
============

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


Option 1: In your models.py
---------------------------

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

`Option 1 example <https://github.com/goinnn/django-model-history/blob/0.1.0/example/news/models.py#L28>`_.


Option 2: In your models.py
---------------------------

::

    from django.db import models


    from model_history.models import create_history_model_class, BaseModelHistory

    class MyModel(models.Model):
        ....


    MyModelHistory = create_history_model_class(MyModel, (BaseModelHistory,))


`Option 2 example <https://github.com/goinnn/django-model-history/blob/0.1.0/example/news/models.py#L63>`_.


Development
===========

You can get the last bleeding edge version of django-model-history by doing a clone
of its git repository

::

  git clone https://github.com/goinnn/django-model-history


Example project
===============

.. image:: https://raw.githubusercontent.com/goinnn/django-model-history/0.1.0/example/uml.png
   :target: https://github.com/goinnn/django-model-history/tree/0.1.0/example/news/models.py

In the source tree, you will find a directory called  `example <https://github.com/goinnn/django-model-history/tree/0.1.0/example/>`_. It contains
a readily setup project that uses django-model-history. You can run it as usual:

::

    python manage.py makemigrations
    python manage.py syncdb --noinput
    python manage.py runserver


Access in a browser to http://localhost:8000/