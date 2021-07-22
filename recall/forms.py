  
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']
