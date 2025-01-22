from django.contrib import admin
from .models import *

@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    pass


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    pass


@admin.register(RideEvent)
class RideEventAdmin(admin.ModelAdmin):
    pass
