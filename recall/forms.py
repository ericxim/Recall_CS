  
from django import forms
from django.db.models.base import Model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Feedback, Post, Question, QuestionResponse, User, Community

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

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

class CreatePostForm(forms.ModelForm):

        
    class Meta:
        model = Post
        fields = ['title','content','community']
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super (CreatePostForm,self ).__init__(*args,**kwargs)
        self.fields['community'].queryset = self.request.user.communities.all()
        
        
    