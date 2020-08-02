from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from .models import *
from authentication.models import *
from django.contrib.auth import authenticate
from adminpanel.models import *

class HomeView(View):
    template_name = "user/index.html"
    def get(self, request):
        return render(request, self.template_name)
  
class EmployeeLogInView(View):
    template_name = "user/login.html"
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['email']
        password = request.POST['password']
        account = authenticate(username=username,password=password)
        if account is not None and account.account_type == 'E':
            emp = Employee.objects.get(account__email=username)
            from datetime import date
            today = date.today()
            date = today.strftime("%d/%m/%Y")
            context = {'emp':emp,'date':date}
            return render(request, 'user/attendance_sheet.html', context)
        else:
            context = {"message":"Credential Not Match"}
            return render(request, self.template_name, context)

class EmployeeAttendanceView(View):

    def post(self, request):
        data = request.POST['entry']
        value = data.split(" ")
        msg = value[0]
        user = value[1]
        from datetime import datetime
        date = datetime.today().strftime('%d-%m-%Y')
        time = datetime.today().strftime('%I:%M %p')
        if msg == "entry":
            user = Employee.objects.get(name=user)
            obj = EmployeeAttendance.objects.filter(employee=user,current_date=date)
            if obj:
                return redirect('../../')
            else:
                user = Employee.objects.get(name=user)
                emp = EmployeeAttendance(employee=user,current_date=date,entry_time=time)
                emp.save()
                return redirect('../../')
        if msg == "exit": 
            user = Employee.objects.get(name=user)
            obj = EmployeeAttendance.objects.filter(employee=user,current_date=date)
            if obj:
                emp = EmployeeAttendance.objects.get(employee=user,current_date=date)
                emp.exit_time=time
                emp.save()
                return redirect('../../')
            else:
                return redirect('../../')
        return redirect('../login/')

class LoginSuccessView(View):
    template_name = "user/employee_attendance.html"
    def get(self, request):
        return render(request, self.template_name)