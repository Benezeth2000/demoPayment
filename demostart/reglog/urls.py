from django.urls import path
from . import views

app_name = 'reglog'

urlpatterns = [
    path('loginpage/', views.login_view, name='loginpage'),
    path('register/', views.signup_view, name='register'),
    path('mainpage/', views.main_screen, name='mainpage'),
]