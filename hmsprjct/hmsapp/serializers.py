# # serializers.py
from rest_framework import serializers
from .models import mortuary_table,Complaints,Leaveregister, Department,Patientdetails,Feedback,patient_reports
from .models import Leaveregister,DialysisBooking
from datetime import time
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
    to_whom = serializers.CharField(source='to_whom.department')  # Access department name

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



class DialysisBookingSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patientdetails.objects.all())

    class Meta:
        model = DialysisBooking
        fields = [
            'patient', 'doctor', 'department', 'reason', 'time_slot', 'date',
            'id', 'booking_id', 'created_at','first_name','last_name','mobile','email'
        ]  # Include only required fields for input/output

        # Mark fields as read-only where applicable
        read_only_fields = ['id', 'booking_id', 'created_at',]

    def validate_time_slot(self, value):
        from datetime import time
        allowed_slots = [
            time(10, 0), time(11, 0), time(12, 0), time(13, 0),
            time(14, 0), time(15, 0), time(16, 0), time(17, 0),
            time(18, 0), time(19, 0), time(20, 0)
        ]
        if value not in allowed_slots:
            raise serializers.ValidationError(
                f"Invalid time slot. Allowed slots are: {', '.join(map(str, allowed_slots))}"
            )
        return value

    def validate(self, data):
        # Check if the slot is already booked
        if DialysisBooking.objects.filter(
            date=data['date'],
            time_slot=data['time_slot'],
            department=data['department']
        ).exists():
            raise serializers.ValidationError("The selected time slot is already booked.")
        return data

    def create(self, validated_data):
        # Generate a unique booking_id
        from uuid import uuid4
        validated_data['booking_id'] = f"BK-{uuid4().hex[:8].upper()}"
        
        # Handle default booking type if not provided
        if 'booking_type' not in validated_data:
            validated_data['booking_type'] = 'Standard'
        
        return super().create(validated_data)

class Doctornameserializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField()

    class Meta:
        model=Staffdetails
        fields = ['FirstName', 'LastName']

