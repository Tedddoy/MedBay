from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('signup/', views.signup, name='signup'),
    path('adminpage/', views.admin, name='adminpage'),
    path('add_service/', views.add_service, name='add_service'),
    path('update_service/<int:service_id>/', views.update_service, name='update_service'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
    path('services/', views.services, name='services'),
    path('customer/', views.customer, name='customer'),
    path('employee/', views.employee, name='employee'),
    path('therapist/', views.therapist, name='therapist'),
    path('user_list/', views.user_list, name='user_list'),
    path('register/', views.register, name='register'),
    path('success/', views.success_view, name='success'),
    path('admin_schedule/', views.admin_schedule, name='admin_schedule'),
]