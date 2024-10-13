from django.shortcuts import get_object_or_404, render, redirect
from .forms import *
from django.contrib.auth import authenticate, login
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.views.decorators.http import require_POST


def index(request):
    services = Service.objects.all()
    total_users = User.objects.filter(is_customer=True).count()
    return render(request, 'index.html', {'services': services, 'total_users': total_users})

def employee(request):
    return render(request,'employee.html')


def therapist(request):
   
    therapist_user = request.user if request.user.is_therapist else None
    
    context = {
        'therapist': therapist_user
    }
    
    return render(request, 'Therapist/therapist.html', context)  # Replace with your actual template name


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
            user.is_educator = False
           

            user.save() 
            msg = 'User created successfully'
            return redirect('customer')  
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form, 'msg': msg})

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
                return redirect('customer',user_id=user.id)
            elif user is not None and user.is_employee:
                login(request, user)
                return redirect('employee')
            elif user is not None and user.is_therapist:
                login(request, user)
                return redirect('therapist')
            elif user is not None and user.is_educator:
                login(request, user)
                return redirect('educator')
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
    total_service = Service.objects.all().count()
    total_availability = Service.objects.filter(availability=True).count()
    total_therapy = Category.objects.all().values().count()
    return render(request, 'admin/admin_services.html', {'total_therapy': total_therapy, 'total_availability': total_availability,
                                                          'total_service': total_service, 'services': services, 'categories': categories})

def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_services') 
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
        return redirect('admin_services')

    return render(request, 'admin/update_service.html', {'service': service, 'categories': categories})

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



# CUSTOMER FUNCTIONS
# CUSTOMER FUNCTIONS
# CUSTOMER FUNCTIONS
# CUSTOMER FUNCTIONS

def customer(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'customer/customer.html', {'user': user})

def enrollment(request):
    return render(request,'customer/enrollment.html')

def enrollment_view(request, user_id):
    class_category = Category.objects.filter(category__iexact='class').first()
    services = Service.objects.filter(category_id=class_category) if class_category else []

    return render(request, 'customer/enrollment.html', {'services': services, 'user_id': user_id})

def customer_therapy(request, user_id):
    return render(request, 'customer/customer_therapy.html', {'user_id': user_id})

def customer_appointment(request, user_id): 
    therapy_category = Category.objects.filter(category__iexact='therapy').first()
    services = Service.objects.filter(category_id=therapy_category) if therapy_category else []

    return render(request, 'customer/customer_appointment.html', {'user_id': user_id, 'services': services})
     
def edit_profile(request, user_id):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.birthdate = request.POST.get('birthdate')  # If you have a birthdate field
        
        # Handle profile picture upload
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        messages.success(request, 'Your profile was updated successfully.')
        return redirect('customer', user_id=user_id)  # Redirect to the user page after successful update

    return render(request, 'customer_page.html', {'user': user})  # Replace with your actual template if different 

@require_POST
def book_appointment(request):
    user = request.user
    date = request.POST.get('date')
    time = request.POST.get('time')
    service_id = request.POST.get('service_id')

    try:
        # Get the service instance
        service = Service.objects.get(id=service_id)

        # Create the appointment
        appointment = Appointment.objects.create(user=user, date=date, time=time, service=service)

        return JsonResponse({
            'success': True,
            'message': 'Appointment booked successfully!',
            'service_name': service.name,
            'appointment_id': appointment.id  # Return the appointment ID
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
#EDUCATOR FUNCTIONS
#EDUCATOR FUNCTIONS
#EDUCATOR FUNCTIONS
#EDUCATOR FUNCTIONS


def educator(request):
    schedules = Schedule.objects.filter(educator_id=request.user) 
    return render(request, 'educator/educator.html', {'schedules': schedules})


def add_resources(request):
    if request.method == 'POST':
        resource_name = request.POST.get('resource_name')
        resource_type = request.POST.get('resource_type')
        availability = request.POST.get('availability') == 'True'

        new_resource = Resources(
            resource_name=resource_name,
            resource_type=resource_type,
            availability=availability
        )
        new_resource.save()
        return redirect('educator')

    return render(request, 'educator/add_resources.html')