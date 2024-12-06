from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MortuaryTableSerializer,UpdateComplaintSerializer,ComplaintSerializer,LeaveregisterSerializer,FeedbackSerializer,FeedbackCreateSerializer,PatientdetailsSerializer
from .serializers import PatientReportsSerializer,DialysisBookingSerializer
from .models import Complaints, Staffdetails, Department,Leaveregister,Feedback,Patientdetails,patient_reports
from datetime import datetime
from .pagination import ComplaintPagination
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.db.models import Max
from django.db.models import Q
from django.shortcuts import get_object_or_404
import os
from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from datetime import time, timedelta
from rest_framework import serializers
from .models import DialysisBooking, Patientdetails
from rest_framework.exceptions import NotFound






@api_view(['POST'])
def mortuary_table_create_view(request):
    if request.method == 'POST':
        serializer = MortuaryTableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_complaint(request):
    """
    API to update complaints based on modecontroller.
    """
    serializer = UpdateComplaintSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Extract validated data
    mode = serializer.validated_data['modecontroller']
    comp_id = serializer.validated_data['compidcontroller']
    reason = serializer.validated_data['reasoncontroller']

    # Fetch the complaint
    complaint = Complaints.objects.get(id=comp_id)

    # Process based on mode
    if mode == 1:  # Rejected
        complaint.action_comp = 1
        complaint.reason = reason
        complaint.remarks = "Rejected"
    elif mode == 2:  # On Hold
        complaint.action_comp = 0
        complaint.reason = reason
        complaint.remarks = "On hold"
    elif mode == 3:  # Resolved
        complaint.action_comp = 1
        complaint.reason = reason
        complaint.remarks = "Resolved"

    complaint.save()
    return Response({"message": "Complaint updated successfully."}, status=status.HTTP_200_OK)

@api_view(['GET'])
def fetch_complaints(request):
    """
    Fetch complaints filtered by department name and start date.
    """
    try:
        # Retrieve query parameters
        department_name = request.query_params.get('department', None)
        start_date = request.query_params.get('start_date', None)

        # Start with all complaints
        complaints = Complaints.objects.all()

        # Filter by department name
        if department_name:
            complaints = complaints.filter(to_whom__department__iexact=department_name)

        # Filter by start date
        if start_date:
            complaints = complaints.filter(date_reg__gte=start_date)

        # Serialize and return the complaints
        serializer = ComplaintSerializer(complaints, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": f"An error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def register_leave(request):
    """
    Registers a leave request with fields: empid, name, department, start_date, end_date, reason.
    """
    try:
        data = request.data.copy()  # Make the data mutable

        department_name = data.get('department')  # Assume department is provided as a name

        # Validate department
        try:
            department = Department.objects.get(department=department_name)
        except Department.DoesNotExist:
            return Response({'status': 'error', 'message': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)

        # Include department ID in data
        data['department'] = department.id

        # Serialize and validate data
        serializer = LeaveregisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Leave registered successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_leave_requests(request):
    department_name = request.GET.get('departmentcontroller') 

    # Validate departmentcontroller
    if not department_name:
        return Response({"status": "error", "message": "Department name is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Get department by name
    try:
        department = Department.objects.get(department=department_name)
    except Department.DoesNotExist:
        return Response({"status": "error", "message": "Department not found."}, status=status.HTTP_404_NOT_FOUND)

    # Fetch leave requests for the department
    leaves = Leaveregister.objects.filter(department=department.id, cancelled=False, pending=1).order_by('leave_requested')

    if not leaves.exists():
        return Response({"status": "error", "message": "No leave records found for the given department."}, status=status.HTTP_404_NOT_FOUND)

    # Serialize data with department name
    serialized_data = [
        {
            "empid": leave.empid,
            "name": leave.name,
            "department": department.department,  # Include department name
            "leave_requested": leave.leave_requested,
            "leave_approved": leave.leave_approved,
            "leave_status": leave.leave_status,
            "leave_approved_by": leave.leave_approved_by,
            "return_date": leave.return_date,
            "cancelled": leave.cancelled,
            "reason": leave.reason,
            "pending": leave.pending,
        }
        for leave in leaves
    ]

    return Response({"status": "success", "data": serialized_data}, status=status.HTTP_200_OK)



# @api_view(['GET'])
# def get_feedback(request):
#     # Fetch feedback with action_response=False and pending=True
#     feedbacks = Feedback.objects.filter(action_response=False, pending=True)

#     # Serialize the data
#     serializer = FeedbackSerializer(feedbacks, many=True)
    
#     return Response(serializer.data)

@api_view(['GET'])
def get_feedback(request):
    try:
        # Fetch feedback where pending = 1 and action_response = '0'
        feedbacks = Feedback.objects.filter(pending=1, action_response="0")
        
        # Serialize the data
        serializer = FeedbackSerializer(feedbacks, many=True)

        # Return the response
        return Response(serializer.data)

    except Exception as e:
        return Response({'error': f'An error occurred: {str(e)}'}, status=500)





@api_view(['POST'])
def feedback_response(request):
    try:
        # Deserialize input data
        serializer = FeedbackCreateSerializer(data=request.data)
        
        # Validate the data
        if serializer.is_valid():
            serializer.save()  # Save the feedback record
            return Response({"message": "Success"}, status=status.HTTP_201_CREATED)
        
        # If invalid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error occurred: {str(e)}")
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)


@api_view(['POST'])
def update_feedback_status(request):
    """
    Updates feedback status when given appropriate data.
    """
    try:
        # Extract fields from the request data
        dates1 = request.data.get('datecontroller')
        approved_by = request.data.get('approvedbycontroller')
        response_back = request.data.get('responsebackcontroller')
        leave_id = request.data.get('feedbackidcontroller')

        # Check if all required fields are present
        if not all([dates1, approved_by, response_back, leave_id]):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the feedback entry
        feedback = Feedback.objects.filter(id=leave_id, pending=1).first()

        if not feedback:
            return Response({'error': 'Feedback not found or already updated'}, status=status.HTTP_404_NOT_FOUND)

        # Update feedback fields
        feedback.pending = 0
        feedback.date_action = dates1
        feedback.action_response = response_back
        feedback.approved_by = approved_by
        feedback.save()  # Save the updated object to the database

        return Response({'message': 'Feedback updated successfully'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST'])
def add_patient(request):
    data = request.data

    # Handle file upload
    image_file = request.FILES.get('image', None)
    data['image'] = image_file  # Pass the uploaded file to the serializer

    # Generate patient ID
    last_two_digits_of_year = datetime.datetime.now().strftime('%y')
    max_id = Patientdetails.objects.aggregate(Max('id'))['id__max']
    next_id = max_id + 1 if max_id else 1
    custom_id = f"HP{last_two_digits_of_year}{str(next_id).zfill(6)}"

    # Validate and map department by name
    department_name = data.get('department')
    if not department_name:
        return Response({"error": "Department name is required"}, status=400)
    
    try:
        department = Department.objects.get(department=department_name)
        data['department'] = department.id  # Replace the name with the ID for saving
    except Department.DoesNotExist:
        return Response({"error": f"Department with name '{department_name}' does not exist"}, status=400)

    # Use the serializer to validate and save the data
    serializer = PatientdetailsSerializer(data=data)
    if serializer.is_valid():
        patient = serializer.save()
        patient.patientid = custom_id
        patient.regdate = datetime.datetime.now().strftime('%Y/%m/%d')
        patient.save()

        return Response({"message": "Patient created successfully", "patient_id": custom_id}, status=201)
    else:
        return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_patient_details(request):
    # Extract the `patientid` query parameter
    patient_id = request.GET.get('patientid')

    # Validate the query parameter
    if not patient_id:
        return Response({"error": "Parameter 'patientid' is required"}, status=400)

    try:
        # Get the patient details
        patient = get_object_or_404(Patientdetails, patientid=patient_id)

        # Retrieve the related department details, if available
        department = Department.objects.filter(id=patient.department).first()
        department_name = department.department if department else "Unknown"

        # Prepare the response data
        response_data = {
            "first_name": patient.firstname,
            "last_name": patient.lastname,
            "patient_id": patient.patientid,
            "doctor": patient.docname,
            "prescription": patient.presc,
            "mobile_number": patient.mobnumber,
            "date_of_birth": patient.dob,
            "address": patient.address,
            "department": department_name,
            "email": patient.email,
            "image": request.build_absolute_uri(patient.image.url) if patient.image else None,  # Full image URL
            "relative_type": patient.relativetype,
            "relative_contact_number": patient.relativecontactnum,
            "gender": patient.gender,
            "blood_group": patient.bloodgroup,
        }

        return Response(response_data, status=200)

    except NotFound:
        return Response({"error": f"Patient with ID '{patient_id}' not found."}, status=404)

    except Exception as e:
        # Log error for debugging if needed
        print(f"Unexpected error: {str(e)}")
        return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=500)


@api_view(['POST'])
def deactivate_patient(request):
    # Extract the patientid from the request data
    patientid = request.data.get('patientidcontroller')

    # Validate that patientid is provided
    if not patientid:
        return Response({"error": "Parameter 'patientidcontroller' is required"}, status=400)

    try:
        # Find the patient by patientid
        patient = get_object_or_404(Patientdetails, patientid=patientid)

        # Update the 'active' field to 0
        patient.active = 0
        patient.save()

        return Response({"message": "Record deactivated successfully."}, status=200)

    except Exception as e:
        # Return error if something goes wrong
        return Response({"error": str(e)}, status=500)
    
class FileUpload(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        if 'file' not in request.FILES:
            raise ParseError("File is required.")

        # Retrieve the uploaded file
        file = request.FILES['file']
        
        # Ensure the reports directory exists
        reports_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
        os.makedirs(reports_dir, exist_ok=True)

        # Save the file
        file_path = os.path.join(reports_dir, file.name)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        # Save the data in the patient_reports model
        patient_id = request.data.get('patient_id', 'unknown')
        doctor_id = request.data.get('doctor_id', 'unknown')
        date = request.data.get('date', None)

        model_obj, created = patient_reports.objects.get_or_create(
            patient_id=patient_id,
            doctor_id_id=doctor_id,  # Adjust based on your ForeignKey setup
            date=date,
            file_path=f"reports/{file.name}"
        )
        
        return Response({
            "message": "File uploaded successfully.",
            "file_path": f"reports/{file.name}"
        }, status=201)

@api_view(['POST'])
def book_dialysis(request):
    if request.method == 'POST':
        serializer = DialysisBookingSerializer(data=request.data)
        if serializer.is_valid():
            # Generate a unique booking ID if not provided
            if not serializer.validated_data.get('booking_id'):
                import uuid
                serializer.validated_data['booking_id'] = str(uuid.uuid4())
            
            serializer.save()
            return Response({"message": "Booking created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        # Return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def available_slots(request):
    date = request.GET.get('date')
    department = request.GET.get('department')

    if not date or not department:
        return Response({"error": "Date and department are required."}, status=400)

    # Define allowed slots
    allowed_slots = [
        time(10, 0), time(11, 0), time(12, 0), time(13, 0),
        time(14, 0), time(15, 0), time(16, 0)
    ]

    # Get already booked slots
    booked_slots = DialysisBooking.objects.filter(date=date, department=department).values_list('time_slot', flat=True)

    # Find available slots
    available_slots = [slot for slot in allowed_slots if slot not in booked_slots]

    return Response({"available_slots": available_slots}, status=200)

# class DepartmentListView(generics.ListAPIView):
#     def get_queryset(self):
#         queryset = Department.objects.all()
#         name = self.request.query_params.get('name', None)
#         if name:
#             queryset = queryset.filter(name__icontains=name)
#         return queryset

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         # Extract the department names as a list
#         department_names = list(queryset.values_list('name', flat=True))
#         # Return only the list of names
#         return Response(department_names)

