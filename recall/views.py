from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.urls import reverse_lazy
from django.urls.base import reverse

from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *



def index(request):
    if request.user.is_authenticated:
        return HomeView.as_view()(request)
    return render(request,"recall/index.html")


class HomeView(ListView):
    template_name="recall/home.html"
    context_object_name='Posts'
    model = Post

    def get_context_data(self, **kwargs):
        communitites = CommunityMember.objects.filter(user_id=self.request.user.id)
        context = super(HomeView, self).get_context_data(**kwargs)
        return context

class QuestionView(DetailView):
    pass
    

    
class RegisterView(CreateView):
  template_name = 'recall/register.html'
  success_url = reverse_lazy('login')
  form_class = RegistrationForm

class LoginView(LoginView):
    template_name="recall/login.html"
    redirect_field_name="home"
