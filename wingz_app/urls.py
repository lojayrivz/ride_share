from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserAccountViewSet, basename='user')
router.register(r'rides', RideViewSet, basename='ride')
router.register(r'ride-events', RideViewSet, basename='ride-event')

urlpatterns = [
    path('api/', include(router.urls)),
]