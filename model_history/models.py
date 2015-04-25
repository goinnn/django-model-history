import datetime

from importlib import import_module

from django.db import models
from django.db.models import signals
from django.forms import model_to_dict
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


from model_history.utils import name_history_model, create_history_model_class

STATUS = (('insert', _('Insert')),
          ('update', _('Update')),
          ('delete', _('Delete')))


@python_2_unicode_compatible
class BaseModelHistory(models.Model):
    '''Base model class to the hictoric instances'''

    timestamp = models.DateTimeField(default=datetime.datetime.now)
    status = models.CharField(verbose_name=_(u'Status'),
                              max_length=6, choices=STATUS,
                              default='update')

    class Meta:
        abstract = True

    def __str__(self):
        return self.status


class ModelHistoryProviderMeta(models.base.ModelBase):
    '''ModelHistoryProviderMeta creates the current class and another class (MyClassHistory)'''

    def __new__(cls, name, bases, attrs):
        new_class = super(ModelHistoryProviderMeta, cls).__new__(cls, name, bases, attrs)
        if name != 'ModelHistoryProvider':
            create_history_model_class(new_class, (BaseModelHistory,))
        return new_class


class ModelHistoryProvider(models.Model):
    '''This class provides the model history feature to every class inheriting from it'''

    __metaclass__ = ModelHistoryProviderMeta

    class Meta:
        abstract = True


# Signals #


def create_history_instance(status, instance):
    '''Create an historic instance from a instance object'''
    data = model_to_dict(instance, exclude=(instance._meta.pk.name,))
    data['status'] = status
    data['history_id'] = instance.pk
    name_model = name_history_model(instance.__class__.__name__)

    modelhistory = getattr(import_module(instance.__class__.__module__, None),
                           name_model)
    modelhistory.objects.create(**data)


def model_history_save(sender, instance, created, **kwargs):
    '''Create an historic instance when a instance is saved: insert or update'''
    if isinstance(instance, ModelHistoryProvider):
        if created:
            status = 'insert'
        else:
            status = 'update'
        create_history_instance(status, instance)
signals.post_save.connect(model_history_save)


def model_history_delete(sender, instance, **kwargs):
    '''Create an historic instance when a instance is deleted'''
    if isinstance(instance, ModelHistoryProvider):
        status = 'delete'
        create_history_instance(status, instance)
signals.post_delete.connect(model_history_delete)