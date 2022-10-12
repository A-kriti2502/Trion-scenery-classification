from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('imgUpload',views.imgUpload, name="imgUpload"),
    path('predictImage2',views.predictImage2, name="predictImage2"),
    path('predictImage3',views.predictImage3, name="predictImage3"),
    path('displayimg',views.displayimg, name="displayimg"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
