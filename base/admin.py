from django.contrib import admin

# Register your models here.

from .models import Activity, Room, Location, Message, Tour, User, Day

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Location)
admin.site.register(Message)
admin.site.register(Day)
admin.site.register(Tour)
admin.site.register(Activity)