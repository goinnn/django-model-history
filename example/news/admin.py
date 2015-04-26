from django.contrib import admin

from news.models import NewsItem, NewsItemHistory, Event, EventHistory


class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', )


class NewsItemHistoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'history_status')
    list_filter = ('history_status', )


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', )


class EventHistoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'history_status')
    list_filter = ('history_status', )


admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(NewsItemHistory, NewsItemHistoryAdmin)

admin.site.register(Event, EventAdmin)
admin.site.register(EventHistory, EventHistoryAdmin)