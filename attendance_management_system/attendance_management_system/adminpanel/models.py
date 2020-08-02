from django.db import models
from authentication.models import *

class Employee(models.Model):
    gender_type = (('Male','Male'),
                ('Female','Female'),)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='employee_account')
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, unique=True)
    image = models.FileField(upload_to='profile_pic/', null=True)
    gender = models.CharField(choices=gender_type, max_length=10, null=True)
    date_of_birth = models.DateField(null=True)

    def __str__(self):
        return self.name

class EmployeeAttendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_attendance')
    current_date = models.CharField(max_length=250, blank=True, null=True)
    entry_time = models.CharField(max_length=250, blank=True, null=True)
    exit_time = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return str(self.employee.name)