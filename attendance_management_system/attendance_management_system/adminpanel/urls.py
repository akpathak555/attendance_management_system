from django.urls import path
from . import views

urlpatterns = [
    path('', views.AdminLoginView.as_view(), name="admin_login"),
    path('ragister/', views.EmployeeFormView.as_view(), name="employee_form"),
    path('list/', views.EmployeeListView.as_view(), name="employee_list"),
    path('update/<int:pk>', views.EmployeeUpdateView.as_view(), name="employee_update"),
    path('delete/<int:pk>', views.EmployeeDeleteView.as_view(), name="employee_delete"),
    path('sheet/', views.AttendanceSheetView.as_view(), name="attendance_sheet")
]