from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    path('properties/<int:pk>/book/', views.booking_page, name='booking_page'),
    path('properties/<int:pk>/save/', views.save_property, name='save_property'),
    path('properties/<int:pk>/unsave/', views.unsave_property, name='unsave_property'),
    path('properties/<int:pk>/message/', views.message_landlord, name='message_landlord'),

    path('property/create/', views.property_create, name='property_create'),
    path('property/<int:pk>/edit/', views.property_edit, name='property_edit'),
]