from django.contrib import admin
from . models import mortuary_table,Complaints
# # Register your models here.

# admin.site.register(Department)
admin.site.register(mortuary_table)
@admin.register(Complaints)
class ComplaintsAdmin(admin.ModelAdmin):
    list_display = ('empcode', 'complaint', 'date_reg', 'action_comp', 'name', 'to_whom', 'remarks', 'reason')
    search_fields = ('empcode', 'name', 'complaint')
    list_filter = ('action_comp', 'date_reg')