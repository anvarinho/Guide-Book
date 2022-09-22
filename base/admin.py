from django.contrib import admin

# Register your models here.
# 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

from .models import Activity, ImageModel, Region, Room, Location, Message, Sight, Tour, User, Day

admin.site.register(User)
admin.site.register(Sight)
admin.site.register(Region)
admin.site.register(Room)
admin.site.register(Location)
admin.site.register(Message)
admin.site.register(Day)
admin.site.register(Tour)
admin.site.register(Activity)
admin.site.register(ImageModel)