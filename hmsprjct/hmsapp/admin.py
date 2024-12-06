from django.contrib import admin
from . models import mortuary_table,Complaints,Staffdetails,Leaveregister,Patientdetails,Feedback,Department
# # Register your models here.

# admin.site.register(Department)
admin.site.register(mortuary_table)
admin.site.register(Department)



class ComplaintsAdmin(admin.ModelAdmin):
    # Display fields in the admin list view
    list_display = ('id', 'empcode', 'complaint', 'date_reg', 'action_comp', 'name', 'remarks', 'reason', 'get_department_name')
    
    # Add search functionality for department and name
    search_fields = ('name', 'to_whom__department')  # Ensure 'department' matches the field name in Department

    # Allow filtering by department in the admin interface
    list_filter = ('to_whom', 'action_comp')

    # Define a method to retrieve the department name from the related Department model
    def get_department_name(self, obj):
        # Use the correct field name from the Department model
        return obj.to_whom.department if obj.to_whom else "No Department"
    get_department_name.short_description = 'Department'  # Custom column header

# Register the model with the custom admin class
admin.site.register(Complaints, ComplaintsAdmin)


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