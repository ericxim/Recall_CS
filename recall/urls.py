from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', login_required(views.HomeView.as_view()), name="home"),
    path('community/<int:pk>', login_required(views.CommunityView.as_view()), name="community"),
    path('question/<int:pk>', login_required(views.QuestionView.as_view()), name="question"),
    path('community/<int:pk>/manage', login_required(views.ManageCommunityView.as_view()), name="manage-community"),
    path('community/join', login_required(views.JoinCommunityView.as_view()), name="join-community")
] 