from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Service)
admin.site.register(Category)
admin.site.register(Schedule)
admin.site.register(Appointment)