from django.urls import path
from base import views as base_views

urlpatterns = [
    path("", base_views.HomePage, name="chat-home"),
    path("room/<int:pk>", base_views.Room, name="chat-room"),
    path("create/room/", base_views.CreateRoom, name="create-room"),
    path("update/room/<int:pk>", base_views.UpdateRoom, name="update-room"),
    path("join/room/<int:pk>" , base_views.JoinRoom , name = "join-room") ,
    path("delete/room/<int:pk>", base_views.DeleteRoom, name="delete-room"),
    path("delete/message/<int:pk>/" , base_views.DeleteMessage , name = "delete-message"),
    path("profile/<int:pk>/" , base_views.UserProfile , name = "user-profile") ,
    path("profile/udpate/<int:pk>" , base_views.editProfile , name = "edit-profile") ,
    path("topics/" , base_views.topicPage , name = "topics-page"),
    
    ]