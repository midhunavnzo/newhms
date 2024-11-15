
from django.urls import path
from .views import DepartmentListView,MortuaryTableCreateView

urlpatterns = [

    path('api/departments/', DepartmentListView.as_view(), name='department-list'),
    path('api/mortuary-records/', MortuaryTableCreateView.as_view(), name='mortuary_record_create')
]
