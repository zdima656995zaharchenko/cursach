import django_filters
from .models import Rate, Source

class RateFilter(django_filters.FilterSet):

    class Meta:
        model = Rate
        fields = (
            'buy',
            'sell',
            'currency'
        )

class SourceFilter(django_filters.FilterSet):

    class Meta:
        model = Source
        fields = (
            'name',
            'source_url',
            'exchange_address',
            'phone_number'
        )

