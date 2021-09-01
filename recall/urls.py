from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', login_required(views.HomeView.as_view()), name="home"),
    path('community/<int:pk>/', login_required(views.CommunityView.as_view()), name="community"),
    path('community/<int:pk>/responses/', login_required(views.ResponseView.as_view()), name="responses"),
    path('question/<int:pk>/', login_required(views.QuestionView.as_view()), name="question"),
    path('community/<int:pk>/manage/', login_required(views.ManageCommunityView.as_view()), name="manage-community"),
    path('community/join/', login_required(views.JoinCommunityView.as_view()), name="join-community"),
    path('responses/<str:user>/<int:pk>/', login_required(views.UserResponseView.as_view()), name="user-response"),
    path('community/<int:pk>/create-question/', login_required(views.CreateQuestionView.as_view()), name="create-question"),
    path('community/create/', login_required(views.CreateCommunityView.as_view()), name="create-community")
    
]

handler404 = 'recall.views.handler404'
handler505 = 'recall.view.handler505'