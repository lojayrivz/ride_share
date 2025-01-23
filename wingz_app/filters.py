from django_filters import (FilterSet, NumberFilter, ChoiceFilter, CharFilter)
from django.db.models import F
from django.db.models.functions import Sqrt, Power
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

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
    status = ChoiceFilter(
        choices=[
            ('en-route', 'En-Route'),
            ('pickup', 'Pick Up'),
            ('dropoff', 'Drop Off'),
        ],
        method='filter_by_status'
    )
    id_rider__email = CharFilter(method='filter_by_email')

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
        """
            Sort and Ensure sort_by is one of the allowed choices.
        """
        valid_sorting = ['pickup_time', '-pickup_time', 'distance', '-distance']
        if value not in valid_sorting:
            raise ValidationError(f"Invalid sorting '{value}'. Allowed values are: {', '.join(valid_sorting)}")

        return queryset.order_by(value)


    def filter_by_status(self, queryset, name, value):
        """
            Filter and Ensure status is one of the allowed choices.
        """
        valid_statuses = ['en-route', 'pickup', 'dropoff']
        if value not in valid_statuses:
            raise ValidationError(f"Invalid status '{value}'. Allowed values are: {', '.join(valid_statuses)}")
        return queryset.filter(status=value)
    

    def filter_by_email(self, queryset, name, value):
        """
            Filter and Ensure the email is valid and filter rides by the rider's email.
        """
        try:
            validate_email(value)
        except ValidationError:
            raise ValidationError(f"Invalid email address: {value}")
        return queryset.filter(id_rider__email=value)
