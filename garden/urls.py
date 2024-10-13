from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup, name='signup'),
    path('employee/', views.employee, name='employee'),
    path('therapist/', views.therapist, name='therapist'),
    path('adminpage/', views.admin, name='adminpage'),
    
    path('admin_services/', views.admin_services, name='admin_services'),
    path('add_service/', views.add_service, name='add_service'),
    path('update_service/<int:service_id>/', views.update_service, name='update_service'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),

    path('user_list/', views.user_list, name='user_list'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),

    path('admin_schedule/', views.admin_schedule, name='admin_schedule'),
    path('add_schedule/', views.add_schedule, name='add_schedule'), 
    path('edit_schedule/<int:schedule_id>/', views.edit_schedule, name='edit_schedule'),
    path('delete_schedule/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),

## USER
## USER

    path('customer/<int:user_id>/', views.customer, name='customer'),
    path('customer_appointment/<int:user_id>/', views.customer_appointment, name='customer_appointment'),
    path('enrollment/<int:user_id>/', views.enrollment_view, name='enrollment'),
    path('customer_therapy/<int:user_id>/', views.customer_therapy, name='customer_therapy'),
    path('edit-profile/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),


# EDUCATOR    
# EDUCATOR    

    path('educator/', views.educator, name='educator'),
    path('add_resources/', views.add_resources, name='add_resources'),
    
]