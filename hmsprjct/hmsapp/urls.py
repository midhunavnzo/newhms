
from django.urls import path
from . import views


urlpatterns = [ 
    path('api/mortuary-records-POST/', views.mortuary_table_create_view,name='mortuary_record_create'),
    path('api/update_complaint-POST/',views.update_complaint, name='update_complaint'),
    path('api/fetch_complaints-GET/', views.fetch_complaints, name='fetch_complaints'),
    path('api/register-leave-POST/',views.register_leave, name='register_leave'),
    path('api/leave-requests-GET/', views.get_leave_requests, name='leave-request-list'),
    path('api/feedback-get/', views.get_feedback, name='get_feedback'),
    path('api/feedback_response-post/', views.feedback_response, name='feedback_response'),
    path('api/update-feedback-post/',views.update_feedback_status, name='update_feedback_status'),
    path('api/add_patient_registration-post/', views.add_patient, name='add_patient'),
    path('api/get_patient_details/', views.get_patient_details, name='get_patient_details'),
    path('api/deactivate_patient-delete/', views.deactivate_patient, name='deactivate_patient'),
    path('api/upload_report-POST/',views.FileUpload.as_view(), name='upload_report'),


   
   path('api/departments/',views.Departmentlistview.as_view(),name='department_;ist'),
   path('api/departments/<str:department_name>/doctors/', views.get_doctors_by_department, name='doctor-list-by-department'),
]
   