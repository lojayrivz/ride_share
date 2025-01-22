from django_filters import rest_framework as filters
from django.db.models import F, FloatField
from django.db.models.functions import Sqrt, Power
from .models import Ride


class RideFilter(filters.FilterSet):
    latitude = filters.NumberFilter(method='filter_by_distance')
    longitude = filters.NumberFilter(method='filter_by_distance')
    sort_by = filters.ChoiceFilter(
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
                raise filters.FilterSetValidationError("Invalid latitude or longitude.")
        return queryset

    def filter_sorting(self, queryset, name, value):
        return queryset.order_by(value)