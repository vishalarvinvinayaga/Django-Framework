from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('signup/', views.registerUser, name='signup'),
    path('',views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),
    path('create-room/',views.createRoom, name='create-room'),
    path('update-room/<str:pk>',views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>',views.deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>',views.deleteMessage, name='delete-message'),
    path('update-message/<str:pk>',views.updateMessage, name='update-message'),
    path('profile-page/<str:pk>',views.profilePage, name='profile-page'),
    path('update-user/',views.updateUser, name='update-user'),
    path('browse-topic/',views.browseTopics, name='browse-topic'),
    path('activity/',views.activityPage, name='activity'),
]