from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_inbox, name='chat_inbox'),
    path('create-room/', views.create_demo_room, name='create_room'),
    path('<int:room_id>/', views.chat_room, name='chat_room'),
]