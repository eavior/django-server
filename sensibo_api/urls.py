from django.urls import path, re_path
from sensibo_api import views

urlpatterns = [
    path('sensibo/me/pods/<apiKey>/', views.SensiboGetDevicesView.as_view()),
    path('sensibo/ac/<itemId>/<apiKey>/', views.SensiboGetDeviceData.as_view()),
    path('sensibo/ac/<itemId>/<property>/<apiKey>/', views.SensiboPatchDeviceData.as_view()),
]
