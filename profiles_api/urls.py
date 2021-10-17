from django.urls import path, re_path
from profiles_api import views

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
]
