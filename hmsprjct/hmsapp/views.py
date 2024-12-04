from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MortuaryTableSerializer,UpdateComplaintSerializer,ComplaintSerializer,LeaveregisterSerializer,FeedbackSerializer,FeedbackCreateSerializer,PatientdetailsSerializer
from .serializers import PatientReportsSerializer
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
    try:
        # Fetch complaints where action_comp is 0
        complaints = Complaints.objects.filter(action_comp=0)

        # Apply pagination
        paginator = ComplaintPagination()
        paginated_complaints = paginator.paginate_queryset(complaints, request)

        # Serialize the data
        serializer = ComplaintSerializer(paginated_complaints, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)

    except Complaints.DoesNotExist:
        raise APIException("No complaints found.")
    except Exception as e:
        return Response(
            {"error": str(e)},
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

    # Provide default for patient_reports if not included
    data['patient_reports'] = data.get('patient_reports', "")

    # Generate patient ID
    last_two_digits_of_year = datetime.datetime.now().strftime('%y')
    max_id = Patientdetails.objects.aggregate(Max('id'))['id__max']
    next_id = max_id + 1 if max_id else 1
    custom_id = f"HP{last_two_digits_of_year}{str(next_id).zfill(6)}"

    # Debug: Log custom_id and input data
    print(f"Custom ID: {custom_id}")
    print(f"Input Data: {data}")

    # Validate and map department ID
    department_id = data.get('department')
    try:
        department = Department.objects.get(id=department_id)
        data['department'] = department.id  # Ensure the department is referenced by ID
    except Department.DoesNotExist:
        return Response({"error": f"Department with id {department_id} does not exist"}, status=400)

    # Use the serializer to validate and save the data
    serializer = PatientdetailsSerializer(data=data)
    if serializer.is_valid():
        patient = serializer.save()
        patient.patientid = custom_id
        patient.regdate = datetime.datetime.now().strftime('%Y/%m/%d')
        patient.save()

        return Response({"message": "Patient created successfully", "patient_id": custom_id}, status=201)
    else:
        # Debug: Print validation errors
        print(serializer.errors)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_patient_details(request):
    # Extract query parameter
    fname = request.GET.get('patientnamecontroller', None)

    # Validate the query parameter
    if not fname:
        return Response({"error": "Parameter 'patientnamecontroller' is required"}, status=400)

    try:
        # Filter patients based on firstname or patientid
        patients = Patientdetails.objects.filter(
            Q(firstname__icontains=fname) | Q(patientid=fname)
        )

        if not patients.exists():
            return Response({"message": "No matching patients found"}, status=404)

        # Prepare response data
        json_data = []
        for patient in patients:
            # Get the related department name
            depart = patient.department  # Assuming department stores the department ID or name
            department = Department.objects.filter(id=depart).first()  # Change `id` if needed to `name`

            json_data.append({
                "fname": patient.firstname,
                "lname": patient.lastname,
                "pid": patient.patientid,
                "doc": patient.docname,
                "presc": patient.presc,
                "mob": patient.mobnumber,
                "dob": patient.dob,
                "Address": patient.address,
                "Department": department.department if department else '',  # Use the correct field
                "email": patient.email,
                "img": patient.image,
                "reltype": patient.relativetype,
                "relcontact": patient.relativecontactnum,
                "gender": patient.gender,
                "bldgrp": patient.bloodgroup,
            })

        # Return JSON response
        return Response({"list": json_data}, status=200)

    except Department.DoesNotExist:
        return Response({"error": "Department not found for one or more patients"}, status=404)

    except Exception as e:
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