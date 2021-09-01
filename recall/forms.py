  
from django import forms
from django.db.models.base import Model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Feedback, Question, QuestionResponse, User, Community

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

class JoinCommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['community_code']
    
class QuestionResponseForm(forms.ModelForm):
    class Meta:
        model = QuestionResponse
        fields = ['content', 'is_complete']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['content']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'mark']
        
class CreateCommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description']
        
    