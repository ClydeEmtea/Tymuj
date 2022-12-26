from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.Login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('falselogin/', views.falselogin, name='falselogin'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.user, name='user'),
]
