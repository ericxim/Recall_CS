  
from django import forms
from django.db.models.base import Model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import QuestionResponse, User, Community

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

class JoinCommunityForm(forms.Form):
    community_code = forms.CharField(max_length=6)
    
class QuestionResponseForm(forms.ModelForm):
    class Meta:
        model = QuestionResponse
        fields = ['content']
    