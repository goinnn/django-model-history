from django.db import models

from model_history.models import ModelHistoryProvider

from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class NewsItem(ModelHistoryProvider):
    title = models.CharField(max_length=256,
                             blank=True,
                             null=True)
    description = models.TextField(blank=True,
                                   null=True)

    def __str__(self):
        return self.title