from django.contrib import admin

from news.models import NewsItem, NewsItemHistory


class NewsItemAdmin(admin.ModelAdmin):
    pass


class NewsItemHistoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(NewsItemHistory, NewsItemHistoryAdmin)