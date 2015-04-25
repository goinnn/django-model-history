from django.contrib import admin

from news.models import NewsItem, NewsItemHistory


class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', )


class NewsItemHistoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    list_filter = ('status', )


admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(NewsItemHistory, NewsItemHistoryAdmin)