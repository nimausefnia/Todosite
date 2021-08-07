from todo import views
from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns=[ 
path('todo/', views.TodoListCreate.as_view()),    
path('todo/<int:pk>', views.TodoRetrieveUpdateDestroyAPI.as_view()), 
path('todo/<int:pk>/complete', views.TodoComplete.as_view()),    
path('todo/compeleted', views.TodoCompletedList.as_view()),

path('signup', views.signup),
path('login', views.login),











]