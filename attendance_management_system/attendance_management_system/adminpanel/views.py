from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from .models import *
from authentication.models import *
from django.contrib.auth import authenticate

class AdminLoginView(View):
    template_name = "adminpanel/admin_login.html"
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['email']
        password = request.POST['password']
        account = authenticate(username=username,password=password)
        if account is not None and account.account_type == 'A':
            return render(request, 'adminpanel/basic.html', {'admin':username})
        else:
            context = {"message":"Credential Not Match"}
            return render(request, self.template_name, context)
        
class EmployeeFormView(View):
    template_name = "adminpanel/registration_form.html"
    def get(self, request):
        return render(request, self.template_name)
   
    def post(self, request):
        emp_id = request.POST['id']
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        image = request.POST['img']
        gender = request.POST['gender']
        date_of_birth = request.POST['date_of_birth']
        if password != confirm_password:
            context = {"message":"Password Doesn't Match!"}
            return render(request, self.template_name, context)
        if emp_id.isnumeric():
            account = Account.objects.get(email=email,account_type='E')
            account.set_password(password)
            account.save()
            emp = Employee.objects.get(id=emp_id)
            emp.name=name
            emp.phone=phone
            emp.image=image
            emp.gender=gender
            emp.date_of_birth=date_of_birth
            emp.account=account
            emp.save()
            return redirect('../../adminpanel/list/')
        else:
            account = Account(email=email,account_type='E')
            account.set_password(password)
            account.save()
            emp = Employee(name=name,phone=phone,image=image,gender=gender,date_of_birth=date_of_birth,account=account)
            emp.save()
        return render(request, self.template_name)
        
class EmployeeUpdateView(View):
    template_name = "adminpanel/registration_form.html"
    def get(self, request, pk):
        emp = Employee.objects.get(id=pk)
        return render(request, self.template_name, {'emp':emp})

class EmployeeListView(View):
    template_name = "adminpanel/employee_list.html"
    def get(self, request):
        emp = Employee.objects.all()
        return render(request, self.template_name, {'emp':emp})

class EmployeeDeleteView(View):
    template_name = "adminpanel/employee_list.html"
    def get(self, request, pk):
        emp = Employee.objects.get(id=pk)
        emp.delete()
        return redirect('../list/')

class AttendanceSheetView(View):
    template_name = "adminpanel/attendance_sheet.html"
    def get(self, request):
        emp = Employee.objects.all()
        return render(request, self.template_name, {'emp':emp})

    def post(self, request):
        from_date = request.POST['start_date']
        to_date = request.POST['end_date']
        user = request.POST['user']
        from datetime import datetime
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        user_id = Employee.objects.get(name=user)
        data = EmployeeAttendance.objects.filter(employee=user_id)
        emp = []
        for value in data:
            current_date = datetime.strptime(value.current_date, "%d-%m-%Y")
            if current_date >= from_date and current_date <= to_date:
                emp.append({
                    'employee':value.employee,
                    'current_date':value.current_date,
                    'entry_time':value.entry_time,
                    'exit_time':value.exit_time
                })
        return render(request, "adminpanel/attendance_list.html", {'emp':emp})
