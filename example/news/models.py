from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_history.models import ModelHistoryProvider

from django.utils.encoding import python_2_unicode_compatible


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


class Event(BaseNews):
    start_date = models.DateTimeField(verbose_name=_('Start date'))
    end_date = models.DateTimeField(verbose_name=_('End date'))
