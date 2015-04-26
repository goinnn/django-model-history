from django.contrib import admin
from django.utils.translation import ugettext as _


class ModelHistoryProviderAdmin(admin.ModelAdmin):
    list_filter = ('history_status', )

    def get_fieldsets(self, request, obj=None):
        if self.fieldsets:
            return self.fieldsets
        metafields = ('history_status', 'history')
        data_fields = [f for f in self.get_fields(request, obj)
                       if f not in metafields]

        return [(None, {'fields': metafields}),
                (_('Data'), {'fields': data_fields})]