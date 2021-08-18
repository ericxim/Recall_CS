from django.db.models import fields
from django.db.models.fields.related import ForeignKey
from django.db.models.query import QuerySet
from django.forms.forms import Form
from django.views.generic.base import TemplateResponseMixin, TemplateView
from .forms import JoinCommunityForm, QuestionResponseForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.urls import reverse_lazy
from django.urls.base import reverse

from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . mixins import CheckQuestionObjectMixin

from .models import *

def index(request):
    if request.user.is_authenticated:
        return HomeView.as_view()(request)
    return render(request,"recall/index.html")

class HomeView(CheckQuestionObjectMixin, ListView):
    template_name="recall/home.html"
    context_object_name='communities'
        
    def get_queryset(self):
        communities = self.request.user.communities.all()
        return communities
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['incompleted'] = len(QuestionResponse.objects.filter(user=self.request.user, is_complete=False))
        context['completed'] = len(QuestionResponse.objects.filter(user=self.request.user, is_complete=True))
        try:
            if QuestionResponse.objects.filter(user=self.request.user).order_by('-question__date_assigned')[0]:
                context['recent'] = QuestionResponse.objects.filter(user=self.request.user).order_by('-question__date_assigned')[0]
        except:
            context['recent'] = None
        return context

class JoinCommunityView(FormView):
    template_name = 'recall/join-community.html'
    form_class = JoinCommunityForm
    success_url = reverse_lazy('home')
        
    def form_valid(self, form):
        community = Community.objects.filter(community_code=form.cleaned_data['community_code'])
        if community:
            community = Community.objects.get(community_code=form.cleaned_data['community_code'])
            community.users.add(self.request.user)
        return super().form_valid(form)

class QuestionView(UpdateView):
    template_name = 'recall/question.html'
    model = QuestionResponse
    form_class = QuestionResponseForm
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        question = Question.objects.get(id=self.object.question.id)
        context['question'] = question
        return context

class CommunityView(DetailView):
    template_name = 'recall/community.html'
    model = Community
    
    def get_context_data(self, **kwargs):
        context = super(CommunityView, self).get_context_data(**kwargs)
        questions = QuestionResponse.objects.select_related('question').filter(question__community_id=self.kwargs['pk'],user=self.request.user)
        context['questions'] = questions
        return context
    
class ManageCommunityView(DetailView):
    template_name = 'recall/manage-community.html'
    model = Community
    context_object_name = "community"

    def get_context_data(self, **kwargs):
        context = super(ManageCommunityView, self).get_context_data(**kwargs)
        community = Community.objects.get(id = self.kwargs['pk'])
        users = community.users.all()
        context['users'] = users
        return context
    
class RegisterView(CreateView):
  template_name = 'recall/register.html'
  success_url = reverse_lazy('login')
  form_class = RegistrationForm

class LoginView(LoginView):
    template_name="recall/login.html"
    redirect_field_name="home"
