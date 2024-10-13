from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_admin= models.BooleanField('Is admin', default=False)
    is_customer = models.BooleanField('Is customer', default=False)
    is_employee = models.BooleanField('Is employee', default=False)
    is_therapist = models.BooleanField('Is therapist', default=False)
    is_educator = models.BooleanField('Is educator', default=False)
    birthdate = models.DateField(null=True, blank=True)  # Add birthdate field
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # Add profile picture field
    
    @property
    def profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        else:
            return '/path/to/default/picture.jpg'  # specify your default image path here
        
    def __str__(self):
        return self.username

class Category(models.Model):
    category = models.CharField(null=True, max_length=255)

    def __str__(self):
        return self.category

class Service(models.Model):
    category_id = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(null=True,)
    availability = models.BooleanField(null=True, default=True)

    def __str__(self):
        return self.name
    
    @property
    def availability_text(self):
        return "Yes" if self.availability else "No"

class Schedule(models.Model):
    educator_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='educator_schedules')
    service_id = models.ForeignKey(Service, null=True, on_delete=models.CASCADE)
    day = models.CharField(null=True, max_length=10)
    time_start = models.TimeField(null=True)
    time_end = models.TimeField(null=True)

    def __str__(self):
        return f"{self.educator_id.username} - {self.servie_id.name} - {self.day} {self.time_start} - {self.time_end}"

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # If applicable

    def __str__(self):
        return f'Appointment for {self.user.username} on {self.date} at {self.time}'

class Resources(models.Model):
    resource_name = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=255)
    availability = models.BooleanField(null=True, default=True)

    def __str__(self):
        return self.resource_name