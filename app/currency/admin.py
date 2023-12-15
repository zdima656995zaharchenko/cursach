from django.contrib import admin
from .models import Source
from currency.models import Rate

class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'source_url', 'exchange_address', 'phone_number')

admin.site.register(Source, SourceAdmin)


class ContactUsReadOnlyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    fields = '__all__'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'buy',
        'sell',
        'currency',
        'source',
        'created',
    )
    list_filter = (
        'currency',
        'created',

    )

    search_fields = (
        'buy',
        'sell',
        'source',
    )

    def has_delete_permission(self, request, obj=None):
        return False