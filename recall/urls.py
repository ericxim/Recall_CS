from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from recall.models import Question
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', login_required(views.HomeView.as_view()), name="home"),
    path('community/<int:pk>/', login_required(views.CommunityView.as_view()), name="community"),
    path('community/<int:pk>/posts/', login_required(views.CommunityPostsView.as_view()), name="community-posts"),
    path('create-post/', login_required(views.CreatePostView.as_view()), name="create-post"),
    path('post/<int:pk>/', login_required(views.PostView.as_view()), name="post"),
    path('community/<int:pk>/responses/', login_required(views.ResponseView.as_view()), name="responses"),
    path('community/<int:pk>/questions/', login_required(views.QuestionsView.as_view()), name="questions"),
    path('question/<int:pk>/', login_required(views.QuestionView.as_view()), name="question"),
    path('community/<int:pk>/manage/', login_required(views.ManageCommunityView.as_view()), name="manage-community"),
    path('community/join/', login_required(views.JoinCommunityView.as_view()), name="join-community"),
    path('responses/<str:user>/<int:pk>/', login_required(views.UserResponseView.as_view()), name="user-response"),
    path('community/<int:pk>/create-question/', login_required(views.CreateQuestionView.as_view()), name="create-question"),
    path('community/create/', login_required(views.CreateCommunityView.as_view()), name="create-community"),
    path('community/<int:community>/questions/<int:pk>/delete/', login_required(views.DeleteQuestionView.as_view()), name="delete-question")
]

handler404 = 'recall.views.handler404'
handler505 = 'recall.view.handler505'