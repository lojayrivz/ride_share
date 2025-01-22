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
            "id_user", "first_name", "last_name", "role", "email", "phone_number"
        ]


class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    permission_classes = [IsUserRoleAdmin]
    serializer_class = UserAccountSerializer


class RideEventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserAccount
        fields = [
            "id_ride_event", "id_ride", "description", "created_at"
        ]


class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    permission_classes = [IsUserRoleAdmin]
    serializer_class = RideEventSerializer


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = [
            "id_ride", "status", "id_rider", "id_driver", "pickup_latitude", 
            "pickup_longitude", "dropoff_latitude", "dropoff_longitude", "pickup_time",
            "ride_events"
        ]


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    permission_classes = [IsUserRoleAdmin]
    serializer_class = RideSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RideFilter

