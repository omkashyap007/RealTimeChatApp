from django.urls import path 
from base.api import views as api_views

urlpatterns = [ 
        path("" , api_views.getRoutes) , 
        path("rooms/", api_views.getRooms),
        path("rooms/<int:pk>" , api_views.getRoom)
        ]