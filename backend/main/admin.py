from django.contrib import admin
from .models import *
from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple
from bitfield.admin import BitFieldListFilter

class ContractAdmin(admin.ModelAdmin):
    list_display = ('id','title' ,'top_organization', 'organization', 'executor','city', 'price','category', 'contract_date')
    # list_filter = (
    #     ('errors', BitFieldListFilter,)
    # )

admin.site.register(Contract,ContractAdmin)
admin.site.register(GeneralRule)
admin.site.register(CreditSource)
admin.site.register(Category)