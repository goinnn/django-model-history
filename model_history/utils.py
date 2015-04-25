import sys

from copy import copy

from django.apps.registry import apps
from django.db import models
from django.core.exceptions import AppRegistryNotReady
from django.db.models.fields.related import ReverseSingleRelatedObjectDescriptor


def name_history_model(name):
    '''
    Returns the name of the history model class from a name
    '''
    return "%sHistory" % name


def create_empty_class(model, bases):
    '''
    Returns an empty class with the right metadata
    '''
    name = name_history_model(model.__name__)

    try:
        return apps.get_model(model._meta.app_label, name)

    except AppRegistryNotReady:

        class Meta:
            app_label = model._meta.app_label
            abstract = False

        attrs = {}
        attrs["Meta"] = Meta
        attrs["__module__"] = model.__module__
        return type(str(name), bases, attrs)


def create_history_model_class(model_class, bases):
    '''
    Returns the history model class of the model_class.
    This class will have the same attributes that model_class, so it will be
    able to save the data. Also it will have timestamp field and status field,
    these fields are from bases class
    '''
    model_class_history = create_empty_class(model_class, bases)

    # Create history foreignkey
    fk = models.ForeignKey(model_class, name='history',
                           null=True, on_delete=models.SET_NULL)
    fk.model = model_class_history
    fk.attname = 'history_id'
    fk.concrete = True
    fk.column = 'history_id'
    fk.opts = model_class_history._meta
    setattr(model_class_history, 'history', ReverseSingleRelatedObjectDescriptor(fk))

    # Assign the fields to the new class (model_class_history)
    model_class_history._meta.fields = model_class._meta.fields + model_class_history._meta.fields[1:] + (fk,)
    model_class_history._meta.local_many_to_many = model_class._meta.local_many_to_many + model_class_history._meta.local_many_to_many
    model_class_history._meta.local_concrete_fields = model_class._meta.local_concrete_fields + model_class_history._meta.local_concrete_fields[1:] + (fk,)
    model_class_history._meta.local_fields = model_class._meta.local_fields + model_class_history._meta.local_fields[1:] + [fk]

    forward_fields_map = copy(model_class._meta._forward_fields_map)
    del forward_fields_map['id']
    model_class_history._meta._forward_fields_map.update(forward_fields_map)
    model_class_history._meta._forward_fields_map.update({'history': fk})

    setattr(sys.modules[model_class_history.__module__], model_class_history.__name__, model_class_history)
    return model_class_history