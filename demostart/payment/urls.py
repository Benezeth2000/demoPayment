from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('payment_details/', views.mode_payment, name='payment_details'),
]