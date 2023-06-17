from django.urls import path  
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('about_me/', lambda request: redirect('https://yspkm.github.io')),
    path('about_blog/', views.about_blog),
    path('', views.landing),
]
