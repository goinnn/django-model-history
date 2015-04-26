from django.db import models
from django.db.models import signals
from django.forms import model_to_dict
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


from model_history.utils import (get_history_model,
                                 create_history_model_class,
                                 get_list_of_parentlinks)

STATUS = (('insert', _('Insert')),
          ('update', _('Update')),
          ('delete', _('Delete')))


@python_2_unicode_compatible
class BaseModelHistory(models.Model):
    '''Base model class to the hictory instances'''

    history_timestamp = models.DateTimeField(verbose_name=_('Timestamp'),
                                             auto_now_add=True,
                                             editable=True)
    history_status = models.CharField(verbose_name=_('Status'),
                                      max_length=6, choices=STATUS,
                                      default='update')

    class Meta:
        abstract = True

    def __str__(self):
        return self.history_status


class ModelHistoryProviderMeta(models.base.ModelBase):
    '''ModelHistoryProviderMeta creates the current class and another class (MyClassHistory)'''

    def __new__(cls, name, bases, attrs):
        new_class = super(ModelHistoryProviderMeta, cls).__new__(cls, name, bases, attrs)
        if name != 'ModelHistoryProvider' and not new_class._meta.abstract:
            create_history_model_class(new_class, (BaseModelHistory,))
        return new_class


class ModelHistoryProvider(six.with_metaclass(ModelHistoryProviderMeta, models.Model)):
    '''This class provides the model history feature to every class inheriting from it'''

    class Meta:
        abstract = True


# Signals #


def create_history_instance(modelhistory, status, instance):
    '''Creates a change history instance from a instance object'''
    exclude_fields = get_list_of_parentlinks(instance._meta.fields) + [modelhistory._meta.pk.name]
    data = model_to_dict(instance, exclude=exclude_fields)
    data['history_status'] = status
    data['history_id'] = instance.pk

    modelhistory.objects.create(**data)


def model_history_save(sender, instance, created, **kwargs):
    '''Creates a change history instance when a instance is saved: insert or update'''
    modelhistory = get_history_model(instance)
    if modelhistory and issubclass(modelhistory, BaseModelHistory):
        if created:
            status = 'insert'
        else:
            status = 'update'
        create_history_instance(modelhistory, status, instance)
signals.post_save.connect(model_history_save)


def model_history_delete(sender, instance, **kwargs):
    '''Create an change history instance when a instance is deleted'''
    modelhistory = get_history_model(instance)
    if modelhistory and issubclass(modelhistory, BaseModelHistory):
        create_history_instance(modelhistory, 'delete', instance)
signals.post_delete.connect(model_history_delete)