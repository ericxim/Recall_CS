from django.db.models import fields
from django.db.models.fields.related import ForeignKey
from django.db.models.query import QuerySet
from .forms import FeedbackForm, JoinCommunityForm, QuestionForm, QuestionResponseForm, RegistrationForm, CreateCommunityForm, CreatePostForm
from django.shortcuts import render

from django.http import HttpResponseRedirect, request

from django.contrib import messages
from django.urls import reverse_lazy
from django.urls.base import reverse

from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .mixins import CheckQuestionObjectMixin, CheckCommunityAdminMixin, CheckMember, CheckQuestionUser
from . filters import QuestionResponseFilter, QuestionFilter

from .models import *
from django.http import Http404

import uuid 

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
    
class CreateCommunityView(CreateView):
    template_name = 'recall/create-community.html'
    form_class = CreateCommunityForm
    
    def form_valid(self, form):
        form.instance.admin = self.request.user
        while True:
            code = uuid.uuid4().hex[:6].upper()
            if not Community.objects.filter(community_code=code):
                break
        form.instance.community_code = code
        return super(CreateCommunityView, self).form_valid(form)

class JoinCommunityView(FormView):
    template_name = 'recall/join-community.html'
    form_class = JoinCommunityForm
        
    def form_valid(self, form):
        community = Community.objects.filter(community_code=form.cleaned_data['community_code'])
        if community:
            community = Community.objects.get(community_code=form.cleaned_data['community_code'])
            
            if self.request.user.communities.filter(name=community).exists():
                messages.error(self.request, f"Already in {community}")
                return super(JoinCommunityView, self).form_valid(form)
            
            community.users.add(self.request.user)
            messages.success(self.request, f"Joined {community}")
            return super(JoinCommunityView, self).form_valid(form)
        
        messages.error(self.request, f"Community does not exist")
        return super(JoinCommunityView, self).form_invalid(form)
    
    def get_success_url(self):
        return reverse('home')

class QuestionView(CheckQuestionUser, UpdateView):
    template_name = 'recall/question.html'
    model = QuestionResponse
    form_class = QuestionResponseForm
    
    def post(self, request, **kwargs):
        if 'submit' in request.POST:
            request.POST = request.POST.copy()
            request.POST['is_complete'] = 'on'

        return super(QuestionView, self).post(request, **kwargs)
    
    def get_success_url(self):
        return reverse('community', kwargs={'pk':self.object.question.community.id})
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        question = Question.objects.get(id=self.object.question.id)
        context['question'] = question
        context['status'] = self.object.is_complete
        context['response'] = self.object.content
        context['mark'] = self.object.mark
        context['feedback'] = Feedback.objects.filter(response=self.object)
        return context

class CommunityView(CheckMember, DetailView):
    template_name = 'recall/community.html'
    model = Community
    
    def get_context_data(self, **kwargs):
        context = super(CommunityView, self).get_context_data(**kwargs)
        questions = QuestionResponse.objects.select_related('question').filter(question__community_id=self.kwargs['pk'],user=self.request.user).order_by('-question__date_assigned')
        context['questions'] = questions
        return context

class CommunityPostsView(CheckMember, ListView):
    template_name='recall/community-posts.html'
    model = Post
    context_object_name = 'posts'
    
    def get_queryset(self):
        posts = Post.objects.filter(community_id=self.kwargs['pk'])
        return posts


    def get_context_data(self, **kwargs):
        context = super(CommunityPostsView, self).get_context_data(**kwargs)
        community = Community.objects.get(id = self.kwargs['pk'])
        context['community'] = community
        return context

    

class ManageCommunityView(CheckCommunityAdminMixin,DetailView):
    template_name = 'recall/manage-community.html'
    model = Community
    context_object_name = "community"

    def get_context_data(self, **kwargs):
        context = super(ManageCommunityView, self).get_context_data(**kwargs)
        community = Community.objects.get(id = self.kwargs['pk'])
        users = community.users.all()
        context['users'] = users
        return context

class CreateQuestionView(CheckCommunityAdminMixin, CreateView):
    template_name = 'recall/create-question.html'
    model = Question
    form_class = QuestionForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        community = Community.objects.get(id=self.kwargs['pk'])
        form.instance.community = community
        return super(CreateQuestionView, self).form_valid(form)

    def get_success_url(self):
        return reverse('community', args=[self.kwargs['pk']])

class QuestionsView(CheckCommunityAdminMixin,ListView):
    template_name = 'recall/questions.html'
    model = Question
    
    def get_context_data(self, **kwargs):
        context = super(QuestionsView, self).get_context_data(**kwargs)
        questions = Question.objects.filter(community=self.kwargs['pk'])
        question_filter = QuestionFilter(self.request.GET, queryset=questions)
        questions = question_filter.qs
        context['questions'] = questions
        context['question_filter'] = question_filter
        return context
    
class ResponseView(CheckCommunityAdminMixin,ListView):
    template_name = 'recall/responses.html'
    model = QuestionResponse
    
    def get_context_data(self, **kwargs):
        context = super(ResponseView, self).get_context_data(**kwargs)
        responses = QuestionResponse.objects.filter(question__community=self.kwargs['pk'])
        response_filter = QuestionResponseFilter(self.request.GET, queryset=responses)
        responses = response_filter.qs
        context['responses'] = responses
        context['response_filter'] = response_filter
        return context

class UserResponseView(CreateView):
    template_name = 'recall/view-response.html'
    model = Feedback
    form_class = FeedbackForm
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('mark', False):
            response = QuestionResponse.objects.get(id=self.kwargs['pk'], user__username=self.kwargs['user'])
            if int(request.POST['mark']) > response.question.mark or int(request.POST['mark']) < 0:
                return HttpResponseRedirect(reverse('responses', kwargs={'pk': response.question.community.id }))
            response.mark = request.POST['mark']
            response.save()
        super(UserResponseView, self).post(request, *args, **kwargs)
        response = QuestionResponse.objects.get(id=self.kwargs['pk'], user__username=self.kwargs['user'])
        return HttpResponseRedirect(reverse('responses', kwargs={'pk': response.question.community.id }))

    def form_valid(self, form):
        response = QuestionResponse.objects.get(id=self.kwargs['pk'], user__username=self.kwargs['user'])
        if not form.instance.content:
            return HttpResponseRedirect(reverse('responses', kwargs={'pk': response.question.community.id }))
        form.instance.user = self.request.user
        form.instance.response = response
        return super(UserResponseView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UserResponseView, self).get_context_data(**kwargs)
        user_response = QuestionResponse.objects.get(id=self.kwargs['pk'], user__username=self.kwargs['user'])
        context['question'] = user_response
        context['feedback'] = Feedback.objects.filter(response=user_response)
        return context

    def get_success_url(self):
        obj = QuestionResponse.objects.get(id=self.kwargs['pk'], user__username=self.kwargs['user'])
        return reverse('community', args=[obj.question.community.id])

class CreatePostView(CreateView):
    model = Post
    template_name = 'recall/create-post.html'
    form_class = CreatePostForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostView(DetailView):
    model = Post
    template_name ='recall/post.html'
    
    
     
class DeleteQuestionView(DeleteView):
    model=Question
    template_name = 'recall/delete-question.html'
    
    def get_object(self, queryset=None):
        obj = super(DeleteView, self).get_object()
        if not obj.community.admin == self.request.user:
            raise Http404
        return obj
    
    def get_success_url(self):
        return reverse('questions', args=[self.kwargs['community']])
    
class RegisterView(CreateView):
  template_name = 'recall/register.html'
  success_url = reverse_lazy('login')
  form_class = RegistrationForm

class LoginView(LoginView):
    template_name="recall/login.html"
    redirect_field_name="home"


def handler404(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 404
    return response

def handler505(request, exception, template_name="505.html"):
    response = render(template_name)
    response.status_code = 505
    return response

