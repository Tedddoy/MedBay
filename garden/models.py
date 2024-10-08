from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_admin= models.BooleanField('Is admin', default=False)
    is_customer = models.BooleanField('Is customer', default=False)
    is_employee = models.BooleanField('Is employee', default=False)
    is_therapist = models.BooleanField('Is therapist', default=False)
    is_educator = models.BooleanField('Is educator', default=False)

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
        return f"{self.educator_id.username} - {self.service_id.name} - {self.day} {self.time_start} - {self.time_end}"
