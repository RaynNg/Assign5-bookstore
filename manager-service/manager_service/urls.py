from django.urls import path
from app.views import (
    ManagerListCreate,
    ManagerDetail,
    StaffManagement,
    ReportView,
    api_index,
)

urlpatterns = [
    path("", api_index),
    path("managers/", ManagerListCreate.as_view()),
    path("managers/<int:pk>/", ManagerDetail.as_view()),
    path("managers/staff/", StaffManagement.as_view()),
    path("managers/reports/", ReportView.as_view()),
]
