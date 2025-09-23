from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('get-specific-options/', views.get_specific_options, name='get_specific_options'),
]