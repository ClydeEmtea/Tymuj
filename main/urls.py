from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.Login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('falselogin/', views.falselogin, name='falselogin'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.user, name='user'),
    path('teams/', TeamList.as_view(), name='teams'),
    path('team/<int:pk>/', TeamDetail.as_view(), name='team-detail'),
    path('team-create/', TeamCreate.as_view(), name='team-create'),
    path('team-delete/<int:pk>/', TeamDelete.as_view(), name='team-delete'),
    path('team-update/<int:pk>/', TeamUpdate.as_view(), name='team-update'),
    path('event/<int:pk>/', EventDetail.as_view(), name='event'),
    path('event-create/', EventCreate.as_view(), name='event-create'),
]
