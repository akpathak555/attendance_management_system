from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('login/', views.EmployeeLogInView.as_view(), name='employee_login'),
    path('login-success/', views.LoginSuccessView.as_view(), name='login_success'),
    path('attendance-check/', views.EmployeeAttendanceView.as_view(), name='attendance_mark')
]