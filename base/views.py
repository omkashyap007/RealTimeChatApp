from django.shortcuts import render, redirect
from base.models import Chatroom, Message, Topic
from base.forms import ChatRoomForm , UserUpdateForm , ProfileUpdateForm
from django.db.models import Q , Count
from django.contrib import messages 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User

def HomePage(request):
    q = request.GET.get("q").strip() if request.GET.get("q") != None else ""
    rooms = Chatroom.objects.filter(
        Q(topic__name__icontains=q) |
        Q(roomname__icontains=q) |
        Q(description__icontains=q)
    )
    rooms_count = rooms.count()
    rooms = rooms[:6]
    topics = Topic.objects.all()
    topics_count = topics.count()
    topics = topics[:5]
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains = q)
    )[:5]
    
    context = {"rooms": rooms, "topics": topics, "room_messages" : room_messages , "rooms_count": rooms_count , "topics_count" : topics_count}
    return render(request, "base/homePage.html", context)


def Room(request, pk):
    user = request.user 
    room = Chatroom.objects.get(id = pk)
    if not room : 
        return redirect("chat-home")
    room_messages = room.message_set.all()[:20]
    context = {"room": room , "room_messages" : room_messages , "user" : user } 
    return render(request, "base/roomPage.html", context)

@login_required
def CreateRoom(request):
    topics = Topic.objects.all()
    if request.method == "POST":
        form = ChatRoomForm(request.POST)
        topic_name = request.POST.get("topic")
        topic , created = Topic.objects.get_or_create(name = topic_name )
        
        new_room = Chatroom.objects.create(
            host=request.user , 
            roomname = request.POST.get("roomname") , 
            topic = topic , 
            description = request.POST.get("description" )
        )
        new_room.participants.add(request.user.id)
        
        return redirect("chat-room" , pk=new_room.id)
    else:
        form = ChatRoomForm()
    context = {"form": form, "button_value": "Create" , "topics" : topics}
    return render(request, "base/room_form.html", context)

@login_required 
def UpdateRoom(request, pk):
    room = Chatroom.objects.get(id=pk)
    if not room : 
        return redirect("chat-home")
    form = ChatRoomForm(instance = room)
    if request.user != room.host :
        messages.error(request , "You are not allowed to Edit Room Settings !") 
        return redirect("chat-home")
    if request.method == "POST":
        room.roomname = request.POST.get("roomname")
        room.topic , created = Topic.objects.get_or_create(name = request.POST.get("topic"))
        room.description = request.POST.get("description")
        room.save()
        return redirect("chat-room" , pk=room.id)
    context = {"form": form, "button_value": "Update"  , "room" : room }
    return render(request, "base/room_form.html", context)

def JoinRoom(request , pk) : 
    room = Chatroom.objects.get(id = pk)
    if not room : 
        return redirect("chat-home")
    if request.user.is_authenticated : 
        room.participants.add(request.user)
    else : 
        messages.error(request , "You have to Login first in order to join a room !")    
    return redirect("chat-room" , pk=pk)

def DeleteRoom(request, pk):
    object = Chatroom.objects.filter(id=pk).first()
    if not object : 
        return redirect("chat-home")
    topic = object.topic
    context = {"object": object}
    if request.user == object.host :
        if request.method == "POST":
            object.delete()
            if topic.chatroom_set.all().count() ==  0 : 
                topic.delete()
            return redirect("chat-home")
        return render(request, "base/delete.html", context)
    else : 
        messages.error(request , "You are not allowed to do this !")
        

@login_required
def DeleteMessage(request , pk) :
    message = Message.objects.get(id = pk)
    if request.user == message.user :
        message.delete()
        messages.success(request , "The message \"{}..\" has been deleted".format(message.body[:30]))
    else : 
        messages.error(request , "You are not allowed to delete this !")
    return redirect(request.META["HTTP_REFERER"])    


def UserProfile(request , pk) :
    user = User.objects.get(id = pk)
    rooms = Chatroom.objects.filter(host=  user)[:10]
    room_messages = user.message_set.all()[:10]
    topics = Topic.objects.all()[:10]
    profile_page = True
    context = {"user" : user , "rooms" : rooms , "topics" : topics , "room_messages" : room_messages,"profile_page":profile_page} 
    return render(request , "base/profile.html" , context)

def editProfile(request , pk) : 
    user = User.objects.get(id=pk) 
    if request.method == "POST" : 
        user_update_form = UserUpdateForm(request.POST , instance = user)
        profile_update_form = ProfileUpdateForm(request.POST , request.FILES , instance = user.profile )
        
        if user_update_form.is_valid() and profile_update_form.is_valid() : 
            user_update_form.save()
            profile_update_form.save()
            return redirect("user-profile" , pk=pk)
        else : 
            print(user_update_form.errors)
            print(profile_update_form.errors)
            
    else : 
        user_update_form = UserUpdateForm(instance= user)
        profile_update_form = ProfileUpdateForm(instance= user.profile)
    context = {
        "user_update_form" : user_update_form ,
        "profile_update_form" : profile_update_form 
    }
    return render(request , "base/edit_profile.html" , context )

def topicPage(request) :  
    topic_name =  request.GET.get("topic_name") if request.GET.get("topic_name") else "" 
    topics = Topic.objects.filter(
        Q(name__icontains = topic_name) |
        Q(name__startswith = topic_name )
    )
    if topic_name == "" : 
        topics = topics[:5]
    context= {"topics" : topics }
    return render(request , "base/topics_page.html" , context )

# omkashyap007
# testing123

# omkashyap008
# testingagain123

# omkashyap001
# somepasswordfortheuser123

# room =Chatroom.objects.annotate(num_participants = Count("participants"))
# print(room[pk-1].num_participants)
# annotate the queryset for the room by the count of participants .