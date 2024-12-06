# # serializers.py
from rest_framework import serializers
from .models import mortuary_table,Complaints,Leaveregister, Department,Patientdetails,Feedback,patient_reports
from .models import Leaveregister,Staffdetails

# class DepartmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Department
#         fields = ['name',]

class MortuaryTableSerializer(serializers.ModelSerializer):
    dod = serializers.DateField(required=False, allow_null=True)
    
    class Meta:
        model = mortuary_table
        fields = ['fullname', 'dod', 'gender', 'cause_of_death', 'death_cert_num', 'mortuary_fee']


  


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


class PatientdetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patientdetails
        fields = '__all__'
         # Remove 'read_only' for patientid here, as you'll be generating it manually in the view
        extra_kwargs = {
            'patientid': {'read_only': True},  # Make patientid read-only
            'regdate': {'read_only': True},   # Make regdate read-only
        }


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            'id', 
            'patientid', 
            'name', 
            'mobile', 
            'response', 
            'action_response', 
            'date_reg', 
            'date_action', 
            'mail_reg', 
            'approved_by', 
            'pending'
        ]

class FeedbackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['patientid', 'name', 'mobile', 'response', 'date_reg', 'mail_reg']

    def create(self, validated_data):
        # Automatically set default values
        validated_data['action_response'] = '0'
        validated_data['date_action'] = '0'
        validated_data['pending'] = 1
        return super().create(validated_data)
    
class PatientReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = patient_reports
        fields = ['patient_id', 'doctor_id', 'date', 'file_path']

class Doctornameserializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField()

    class Meta:
        model=Staffdetails
        fields = ['FirstName', 'LastName']