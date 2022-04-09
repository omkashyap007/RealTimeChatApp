from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Topic(models.Model) : 
    name = models.CharField(max_length = 100) 
    created = models.DateTimeField(auto_now_add = True)
    class Meta : 
        ordering = ["created"]
    
    def __str__(self): 
        return str(self.name)


class Chatroom(models.Model) : 
    host = models.ForeignKey(User , on_delete = models.CASCADE ) 
    topic = models.ForeignKey("base.Topic", verbose_name="topic", on_delete=models.SET_NULL , null = True)
    roomname = models.CharField(max_length = 200 )
    description = models.TextField(null = True ,  blank = True)
    participants = models.ManyToManyField(User, verbose_name="participants" , related_name = "participants"  )
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    
    class Meta : 
        ordering = ["-updated" , "-created"]
    
    def __str__(self) : 
        return str(self.roomname)  + " created by -> " + str(self.host) + " on " + str(self.topic) 
    
class Message(models.Model) : 
    user = models.ForeignKey(User , on_delete = models.CASCADE) 
    room = models.ForeignKey(Chatroom , on_delete = models.CASCADE) 
    body = models.TextField()
    udpated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True) 
    
    class Meta: 
        ordering = ["-udpated" , "-created"]
    
    def __str__(self) : 
        return str(self.user) + "texted ->" + str(self.body)[:50]
    
class Profile(models.Model) :
    user = models.OneToOneField(User , on_delete = models.CASCADE)
    image = models.ImageField(default = "default.jpg" , upload_to = "profile_pics")
    first_name = models.CharField(max_length=50 , blank = True , null = True)
    last_name = models.CharField(max_length=50 , blank = True , null = True)
    aboutuser = models.TextField(null = True , blank = True)
    
    def __str__(self) : 
        return str(self.user) +"'s profile "
    
    def save(self , *args , **kwargs) :
        super().save(*args , **kwargs) 
        
        img = Image.open(self.image)
        
        if img.height > 300 or img.width > 500 : 
            img.thumbnail((300,300))
            img.save(self.image.path)