from django_filters import rest_framework as filters
from offers_app.models import Offer

class OfferFilter(filters.FilterSet):
    """
    FilterSet for filtering Offer instances based on specific criteria.

    Currently supports filtering offers by maximum delivery time.
    """
    max_delivery_time = filters.NumberFilter(method='filter_max_delivery_time')


    class Meta:
        model = Offer
        fields = []

    def filter_max_delivery_time(self, queryset, name, value):
        """
        Filter offers where the delivery time (in days) is less than
        or equal to the provided value.

        Args:
            queryset: The initial queryset of Offer instances.
            name: The name of the filter (not used here).
            value: Maximum allowed delivery time in days.

        Returns:
            Filtered queryset containing offers with delivery time <= value.
        """
        return queryset.filter(details__delivery_time_in_days__lte=value)
