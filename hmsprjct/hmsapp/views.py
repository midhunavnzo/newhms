from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MortuaryTableSerializer,UpdateComplaintSerializer,ComplaintSerializer,LeaveregisterSerializer
from .models import Complaints, Staffdetails, Department,Leaveregister
from datetime import datetime
from .pagination import ComplaintPagination
from rest_framework.exceptions import APIException


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
        data = request.data
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

