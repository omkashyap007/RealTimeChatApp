from django import forms
from base.models import Chatroom , Profile 
from django.contrib.auth.models import User


class ChatRoomForm(forms.ModelForm) : 
    class Meta : 
        model = Chatroom
        fields = "__all__"
        exclude = ["host" ,"participants"]
       
       
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta : 
        model = User 
        fields = ["username" , "email"]
     
class ProfileUpdateForm(forms.ModelForm): 
    
    class Meta : 
        model = Profile
        fields = "__all__"
        exclude = ["user"]