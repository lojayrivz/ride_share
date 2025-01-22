from django.utils.timezone import now, timedelta
from django.db.models import Prefetch

from rest_framework import serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .filters import *
from .permissions import *

class UserAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserAccount
        fields = [
            'id_user',
            'first_name',
            'last_name',
            'role',
            'email',
            'phone_number'
        ]


class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    permission_classes = [IsUserRoleAdmin]
    serializer_class = UserAccountSerializer


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = [
            'id_ride_event',
            'id_ride',
            'description',
            'created_at'
        ]


class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    permission_classes = [IsUserRoleAdmin]
    serializer_class = RideEventSerializer


class RideSerializer(serializers.ModelSerializer):
    todays_ride_events = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = [
            'id_ride', 'status', 'id_rider', 'id_driver', 'pickup_latitude', 
            'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude', 'pickup_time',
            'todays_ride_events'
        ]
    
    def get_todays_ride_events(self, obj):
        """
            Return the RideEvents from the last 24 hours.
            Utilize the prefetched `todays_ride_events_field`.
        """
        ride_events = getattr(obj, 'todays_ride_events_field', [])
        
        return RideEventSerializer(ride_events, many=True).data


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    permission_classes = [IsUserRoleAdmin]
    serializer_class = RideSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RideFilter

    def get_queryset(self):
        """
            Optimize the queryset to reduce SQL queries:
            - `select_related` for rider and driver (FK relationships).
            - `prefetch_related` for today's RideEvents.
        """
        last_24_hours = now() - timedelta(hours=24)
        return Ride.objects.select_related('id_rider', 'id_driver').prefetch_related(
            Prefetch(
                'ride_events',
                queryset=RideEvent.objects.filter(created_at__gte=last_24_hours),
                to_attr='todays_ride_events_field'
            )
        )

