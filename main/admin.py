from django.contrib import admin

from .models import CustomUser, Works, Builds, Repair, TradeIn, Contacts

admin.site.register(CustomUser)
admin.site.register(Works)
admin.site.register(Builds)
admin.site.register(Repair)
admin.site.register(TradeIn)
admin.site.register(Contacts)