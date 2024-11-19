# # views.py
# from rest_framework import status
# from rest_framework.views import APIView
# # from .serializers import MortuaryTableSerializer
# from rest_framework import generics
# from rest_framework.response import Response
# from .models import Department


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

# class MortuaryTableCreateView(APIView):
#     def post(self, request):
#         serializer = MortuaryTableSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#updated