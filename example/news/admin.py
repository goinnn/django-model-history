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


from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from model_history.admin import ModelHistoryProviderAdmin

from news.models import NewsItem, NewsItemHistory, Event, EventHistory

from news.models import ContentTypeHistory


class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', )


class NewsItemHistoryAdmin(ModelHistoryProviderAdmin):
    list_display = ('title', 'history_status', 'history_timestamp')


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', )


class EventHistoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'history_status', 'history_timestamp')


class ContentTypeHistoryAdmin(ModelHistoryProviderAdmin):
    pass


admin.site.register(ContentType)
admin.site.register(ContentTypeHistory, ContentTypeHistoryAdmin)

admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(NewsItemHistory, NewsItemHistoryAdmin)

admin.site.register(Event, EventAdmin)
admin.site.register(EventHistory, EventHistoryAdmin)