from django.contrib import admin
from .models import *


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'town','province')


admin.site.register(Province)
admin.site.register(Town)
admin.site.register(City, CityAdmin)
