
from django.urls import path
from . import views

urlpatterns = [ 
    path('api/mortuary-records/', views.mortuary_table_create_view,name='mortuary_record_create'),
    path('api/update_complaint/',views.update_complaint, name='update_complaint'),
    path('api/fetch_complaints/', views.fetch_complaints, name='fetch_complaints'),
    path('api/register-leave-post/',views.register_leave, name='register_leave'),
    path('api/leave-requests-get/', views.get_leave_requests, name='leave-request-list'),
]
