from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login
from .models import *


def index(request):
    services = Service.objects.all()
    total_users = User.objects.filter(is_customer=True).count()
    return render(request, 'index.html', {'services': services, 'total_users': total_users})


def admin(request):
    services = Service.objects.all()
    categories = Category.objects.all()
    total_users = User.objects.filter(is_customer=True).count()
    return render(request, 'admin/admin.html', {'total_users': total_users, 'services': services, 'categories': categories})


def customer(request):
    return render(request,'customer.html')

def employee(request):
    return render(request,'employee.html')

def therapist(request):
    return render(request,'therapist.html')


def register(request):
       msg = None
       if request.method == 'POST':
           form = SignUpForm(request.POST)
           if form.is_valid():
               user = form.save(commit=False)  

               role = request.POST.get('role') 

               setattr(user, f"is_{role}", True)  

               user.save() 
               msg = 'User created successfully'
               return redirect('user_list')  
           else:
               msg = 'Form is not valid'
       else:
           form = SignUpForm()
       return render(request, 'admin/add_user.html', {'form': form, 'msg': msg})

def signup(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  

         
            user.is_admin = False  
            user.is_customer = True 
            user.is_employee = False
            user.is_therapist = False
            user.is_educator - False
           

            user.save() 
            msg = 'User created successfully'
            return redirect('customer')  
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form, 'msg': msg})


def success_view(request):
    return render(request, 'admin_user.html')


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_customer:
                login(request, user)
                return redirect('customer')
            elif user is not None and user.is_employee:
                login(request, user)
                return redirect('employee')
            elif user is not None and user.is_therapist:
                login(request, user)
                return redirect('therapist')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})


def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminpage') 
    else:
        form = ServiceForm()
    return render(request, 'admin/add_service.html', {'form': form})

def services(request):
    services = Service.objects.all()
    categories = Category.objects.all()
    return render(request, 'services.html', {'services': services, 'categories': categories})


def update_service(request, service_id):
    service = Service.objects.get(pk=service_id)

    if request.method == 'POST':
        service.name = request.POST.get('name')
        service.description = request.POST.get('description')
        service.price = request.POST.get('price')
        service.category = request.POST.get('category')
        service.save()
        return redirect('admin/services')

    return render(request, 'update_service.html', {'service': service})

def delete_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    service.delete()
    return redirect('services')

def user_list(request):
    return render(request,'admin/admin_users.html')

def admin_schedule(request):
    return render(request,'admin/admin_schedule.html')