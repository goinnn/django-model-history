# -*- coding: utf-8 -*-
# Copyright (c) 2015 by Pablo Martín <goinnn@gmail.com>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from model_history.models import ModelHistoryProvider, BaseModelHistory
from model_history.utils import create_history_model_class


@python_2_unicode_compatible
class Base(ModelHistoryProvider):
    title = models.CharField(verbose_name=_('Title'), max_length=256)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class BaseNews(Base):
    description = models.TextField(verbose_name=_('Description'),
                                   blank=True,
                                   null=True)


class NewsItem(BaseNews):
    publish_date = models.DateTimeField(verbose_name=_('Publish date'))

    class Meta:
        verbose_name = _('News item')
        verbose_name_plural = _('News')


class Event(BaseNews):
    start_date = models.DateTimeField(verbose_name=_('Start date'))
    end_date = models.DateTimeField(verbose_name=_('End date'))

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')


ContentTypeHistory = create_history_model_class(ContentType, (BaseModelHistory,))