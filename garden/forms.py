from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'availability', 'category_id']

    category_id = forms.ModelChoiceField(
    queryset=Category.objects.all(),
    empty_label="Select Category",
    widget=forms.Select(attrs={'class': 'form-control'}),
    label='Category',
   )
    
class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['educator_id', 'service_id', 'day', 'time_start', 'time_end']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['educator_id'].queryset = User.objects.filter(is_educator=True)
        self.fields['service_id'].queryset = Service.objects.all()
    