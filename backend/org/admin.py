from django.contrib import admin
from .models import *


class BudgetInline(admin.TabularInline):
    model = Budget


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'father')
    inlines = [BudgetInline, ]


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(People)
admin.site.register(Executor)
admin.site.register(Synonym)
admin.site.register(Budget)
