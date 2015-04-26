import sys

from copy import copy
from importlib import import_module

from django.apps.registry import apps
from django.db import models
from django.db.models.fields.related import ReverseSingleRelatedObjectDescriptor
from django.core.exceptions import AppRegistryNotReady
from django.utils.translation import ugettext as _


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
            verbose_name = _('%s change history') % model._meta.verbose_name
            verbose_name_plural = _('%s change histories') % model._meta.verbose_name

        attrs = {}
        attrs["Meta"] = Meta
        attrs["__module__"] = model.__module__
        return type(str(name), bases, attrs)


def get_history_model(instance):
    '''Returns the change history model or None if it does not exists'''
    name_model = name_history_model(instance.__class__.__name__)
    return getattr(import_module(instance.__class__.__module__, None),
                   name_model, None)


def get_list_of_parentlinks(fields):
    '''Returns a parentlink fields from fields param'''
    return [f.name for f in fields
            if getattr(f, 'rel', None) and f.rel.parent_link]


def remove_parentlink_fields(fields):
    '''Returns a new field list without the parentlink fields'''
    return [f for f in fields
            if not getattr(f, 'rel', None) or not f.rel.parent_link]


def create_history_model_class(model_class, bases):
    '''
    Returns the change history model class of the model_class.
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
    fk.related_fields[0] = (fk.related_fields[0][0], model_class._meta.get_field(model_class._meta.pk.name))

    setattr(model_class_history, 'history', ReverseSingleRelatedObjectDescriptor(fk))

    # Assign the fields to the new class (model_class_history)
    model_class_history._meta.fields = model_class_history._meta.fields + copy(model_class._meta.fields)[1:] + (fk,)
    model_class_history._meta.local_many_to_many = model_class_history._meta.local_many_to_many + copy(model_class._meta.local_many_to_many)

    # Remove parent fields
    model_class_history._meta.fields = remove_parentlink_fields(model_class_history._meta.fields)
    model_class_history._meta.local_many_to_many = remove_parentlink_fields(model_class_history._meta.local_many_to_many)
    model_class_history._meta.local_concrete_fields = copy(model_class_history._meta.fields)
    model_class_history._meta.local_fields = copy(model_class_history._meta.fields)

    forward_fields_map = copy(model_class._meta._forward_fields_map)
    if model_class._meta.pk:
        field_id = forward_fields_map[model_class._meta.pk.name]
        if getattr(field_id, 'rel', None) and field_id.rel.parent_link:
            del forward_fields_map['%s_id' % field_id.name]
        del forward_fields_map[model_class._meta.pk.name]
        if 'id' in forward_fields_map:
            del forward_fields_map['id']
    model_class_history._meta._forward_fields_map.update(forward_fields_map)
    model_class_history._meta._forward_fields_map.update({'history': fk})

    # Add class to the right path
    setattr(sys.modules[model_class_history.__module__], model_class_history.__name__, model_class_history)
    return model_class_history