from django_filters import (FilterSet, NumberFilter, ChoiceFilter)
from django.db.models import F
from django.db.models.functions import Sqrt, Power
from django.core.exceptions import ValidationError

from .models import Ride


class RideFilter(FilterSet):
    latitude = NumberFilter(
        label='Latitude',
        method='filter_by_distance'
    )
    longitude = NumberFilter(
        label='Longitude',
        method='filter_by_distance'
    )
    sort_by = ChoiceFilter(
        label='Sort By',
        choices=[
            ('pickup_time', 'Pickup Time Ascending'),
            ('-pickup_time', 'Pickup Time Descending'),
            ('distance', 'Distance Ascending'),
            ('distance', 'Distance Descending'),
        ],
        method='filter_sorting'
    )

    class Meta:
        model = Ride
        fields = ['status', 'id_rider__email']

    def filter_by_distance(self, queryset, name, value):
        """
            Filters and sorts rides by distance to the given latitude and longitude.
        """
        latitude = self.data.get('latitude')
        longitude = self.data.get('longitude')

        if latitude and longitude:
            try:
                latitude = float(latitude)
                longitude = float(longitude)
                queryset = queryset.annotate(
                    distance=Sqrt(
                        Power(F('pickup_latitude') - latitude, 2) +
                        Power(F('pickup_longitude') - longitude, 2)
                    )
                )
            except ValueError:
                raise ValidationError('Invalid latitude or longitude.')
        return queryset

    def filter_sorting(self, queryset, name, value):
        return queryset.order_by(value)