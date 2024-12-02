from django.contrib import admin
from . models import mortuary_table,Complaints,Staffdetails,Leaveregister,Patientdetails,Feedback
# # Register your models here.

# admin.site.register(Department)
admin.site.register(mortuary_table)

@admin.register(Complaints)
class ComplaintsAdmin(admin.ModelAdmin):
    list_display = ('empcode', 'complaint', 'date_reg', 'action_comp', 'name', 'to_whom', 'remarks', 'reason')
    search_fields = ('empcode', 'name', 'complaint')
    list_filter = ('action_comp', 'date_reg')




@admin.register(Leaveregister)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'empid', 'leave_requested', 'leave_approved', 'leave_status', 'leave_approved_by', 'reason')
    list_filter = ('leave_status', 'department')
    search_fields = ('empid', 'name')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_reg', 'action_response', 'pending')
    search_fields = ('name', 'date_reg')


@admin.register(Patientdetails)
class PatientdetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'phnumber', 'email')
    search_fields = ('firstname', 'lastname', 'phnumber')