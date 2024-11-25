# # serializers.py
from rest_framework import serializers
from .models import mortuary_table,Complaints,Leaveregister, Department

# class DepartmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Department
#         fields = ['name',]

class MortuaryTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = mortuary_table
        fields = '__all__'  # or specify the fields you want to include in the API




class UpdateComplaintSerializer(serializers.Serializer):
    modecontroller = serializers.ChoiceField(choices=[1, 2, 3])
    compidcontroller = serializers.IntegerField()
    reasoncontroller = serializers.CharField(max_length=250)

    def validate_compidcontroller(self, value):
        # Ensure the complaint exists
        if not Complaints.objects.filter(id=value).exists():
            raise serializers.ValidationError("Complaint not found.")
        return value
    
class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaints
        fields = [
            "id",
            "empcode",
            "complaint",
            "date_reg",
            "action_comp",
            "name",
            "to_whom",
            "remarks",
            "reason",
        ]
from rest_framework import serializers
from .models import Leaveregister

class LeaveregisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaveregister
        fields = [
            'empid',
            'name',
            'leave_requested',
            'return_date',
            'leave_status',
            'leave_approved_by',
            'department',
            'reason',
            'cancelled',
            'pending',
        ]
        read_only_fields = ['leave_status', 'pending']
    
    cancelled = serializers.IntegerField(required=False)
    
    def validate(self, data):
        # Ensure start_date (leave_requested) is before end_date (return_date)
        if data.get('leave_requested') and data.get('return_date'):
            if data['leave_requested'] > data['return_date']:
                raise serializers.ValidationError({"return_date": "End date must be after start date."})
        return data



class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department']