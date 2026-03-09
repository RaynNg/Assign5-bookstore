from django.urls import path
from app.views import StaffListCreate, StaffDetail, ManageBook, StaffLogin, api_index

urlpatterns = [
    path("", api_index),
    path("staff/", StaffListCreate.as_view()),
    path("staff/login/", StaffLogin.as_view()),
    path("staff/<int:pk>/", StaffDetail.as_view()),
    path("staff/manage-book/", ManageBook.as_view()),
    path("staff/manage-book/<int:book_id>/", ManageBook.as_view()),
]
