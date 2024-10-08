from django.shortcuts import get_object_or_404, render, redirect
from .forms import *
from django.contrib.auth import authenticate, login
from .models import *


def index(request):
    services = Service.objects.all()
    total_users = User.objects.filter(is_customer=True).count()
    return render(request, 'index.html', {'services': services, 'total_users': total_users})


def customer(request):
    return render(request,'customer.html')


def employee(request):
    return render(request,'employee.html')


def therapist(request):
    return render(request,'therapist.html')


def admin(request):
    services = Service.objects.all()
    categories = Category.objects.all()
    total_users = User.objects.filter(is_customer=True).count()
    return render(request, 'admin/admin.html', {'total_users': total_users, 'services': services, 'categories': categories})


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

# USER LIST FUNCTIONS
# USER LIST FUNCTIONS
# USER LIST FUNCTIONS
# USER LIST FUNCTIONS
# USER LIST FUNCTIONS

def user_list(request):
    therapists = User.objects.filter(is_therapist=True).count()
    educators = User.objects.filter(is_educator=True).count()
    employees = User.objects.filter(is_employee=True).count()
    customers = User.objects.filter(is_customer=True).count()
    users = User.objects.filter(is_therapist=True) | User.objects.filter(is_educator=True) | User.objects.filter(is_employee=True) | User.objects.filter(is_customer=True)
    context = {
        'users': users,
        'total_therapists': therapists,
        'total_educators': educators,
        'total_employees': employees,
        'total_customers': customers
    }
    return render(request, 'admin/admin_users.html', context)

def add_user(request):
    msg = None
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                msg = 'Username already exists'
            elif User.objects.filter(email=email).exists():
                msg = 'Email already exists'
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password1
                )
                setattr(user, f"is_{role}", True)
                user.save()
                msg = 'User created successfully'
                return redirect('user_list')
        else:
            msg = 'Passwords do not match'
    return render(request, 'admin/add_user.html', {'msg': msg})

def delete_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.delete()
    return redirect('user_list')

def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    msg = None
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')

        if password1 == password2:
            if User.objects.filter(username=username).exclude(id=user_id).exists():
                msg = 'Username already exists'
            elif User.objects.filter(email=email).exclude(id=user_id).exists():
                msg = 'Email already exists'
            else:
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                if password1:
                    user.set_password(password1)
                user.is_therapist = False
                user.is_educator = False
                user.is_employee = False
                user.is_customer = False
                setattr(user, f"is_{role}", True)
                user.save()
                msg = 'User updated successfully'
                return redirect('user_list')
        else:
            msg = 'Passwords do not match'
    return render(request, 'admin/edit_user.html', {'user': user, 'msg': msg})

# SERVICES FUNCTIONS
# SERVICES FUNCTIONS
# SERVICES FUNCTIONS
# SERVICES FUNCTIONS
# SERVICES FUNCTIONS

def admin_services(request):
    services = Service.objects.all()
    categories = Category.objects.all()
    total_users = User.objects.filter(is_customer=True).count()
    return render(request, 'admin/admin_services.html', {'total_users': total_users, 'services': services, 'categories': categories})

def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminpage') 
    else:
        form = ServiceForm()
    return render(request, 'admin/add_service.html', {'form': form})

def update_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        service.name = request.POST.get('name')
        service.description = request.POST.get('description')
        service.price = request.POST.get('price')
        service.availability = request.POST.get('availability') == 'True'
        service.category_id = Category.objects.get(pk=request.POST.get('category_id'))
        service.save()
        return redirect('adminpage')

    return render(request, 'update_service.html', {'service': service, 'categories': categories})

def delete_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    service.delete()
    return redirect('services')

# ADMIN SCHEDULE FUNCTIONS
# ADMIN SCHEDULE FUNCTIONS
# ADMIN SCHEDULE FUNCTIONS
# ADMIN SCHEDULE FUNCTIONS
# ADMIN SCHEDULE FUNCTIONS

def admin_schedule(request):
    schedules = Schedule.objects.all()
    return render(request, 'admin/admin_schedule.html', {'schedules': schedules})

def add_schedule(request):
    educators = User.objects.filter(is_educator=True)
    services = Service.objects.all()

    if request.method == 'POST':
        educator_id = request.POST.get('educator_id')
        service_id = request.POST.get('service_id')
        day = request.POST.get('day')
        time_start = request.POST.get('time_start')
        time_end = request.POST.get('time_end')

        try:
            educator = User.objects.get(pk=educator_id)
            service = Service.objects.get(pk=service_id)
            new_schedule = Schedule(
                educator_id=educator,
                service_id=service,
                day=day,
                time_start=time_start,
                time_end=time_end
            )
            new_schedule.save()
            return redirect('admin_schedule')
        except (User.DoesNotExist, Service.DoesNotExist):
            return render(request, 'admin/add_schedule.html', {'educators': educators, 'services': services, 'error': 'Invalid educator or service'})

    return render(request, 'admin/add_schedule.html', {'educators': educators, 'services': services})

def edit_schedule(request, schedule_id):
    schedule = Schedule.objects.get(pk=schedule_id)
    educators = User.objects.filter(is_educator=True)
    services = Service.objects.all()

    if request.method == 'POST':
        educator_id = request.POST.get('educator_id')
        service_id = request.POST.get('service_id')
        day = request.POST.get('day')
        time_start = request.POST.get('time_start')
        time_end = request.POST.get('time_end')

        try:
            educator = User.objects.get(pk=educator_id)
            service = Service.objects.get(pk=service_id)
            schedule.educator_id = educator
            schedule.service_id = service
            schedule.day = day
            schedule.time_start = time_start
            schedule.time_end = time_end
            schedule.save()
            return redirect('admin_schedule')
        except (User.DoesNotExist, Service.DoesNotExist):
            # Handle errors (e.g., display an error message)
            return render(request, 'admin/edit_schedule.html', {'schedule': schedule, 'educators': educators, 'services': services, 'error': 'Invalid educator or service'})

    return render(request, 'admin/edit_schedule.html', {'schedule': schedule, 'educators': educators, 'services': services})

def delete_schedule(request, schedule_id):
    schedule = Schedule.objects.get(pk=schedule_id)
    schedule.delete()
    return redirect('admin_schedule')


# ADMIN SERVICES FUNCTIONS
# ADMIN SERVICES FUNCTIONS
# ADMIN SERVICES FUNCTIONS
# ADMIN SERVICES FUNCTIONS
# ADMIN SERVICES FUNCTIONS

