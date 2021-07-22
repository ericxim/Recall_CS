from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', login_required(views.HomeView.as_view())),
] 