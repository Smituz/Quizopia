from django.contrib import admin
from django.urls import path,include
from . import views 

urlpatterns = [
    path('',views.login,name='login'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('home',views.home,name='home'),
    path('gen_quiz',views.gen_quiz,name='gen_quiz'),
    path('add_que',views.add_que,name='add_que'),
    path('join_quiz',views.join_quiz,name='join_quiz'),
]