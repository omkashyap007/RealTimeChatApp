from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.contrib.auth.models  import User
from base.models import Chatroom , Message

class ChatConsumer(AsyncWebsocketConsumer) : 
    
    
    async def connect(self): 
        self.roomId = self.scope["url_route"]["kwargs"]["roomId"]
        self.room_group_name = "chat_group_%s"%self.roomId 
        print(self.room_group_name) 
        print("Connection established !") 
        # ye to ho gya connect karne ka kaam . matlab koi connection aayega to iska room id se room group create karenge . 
        
        
        # uske baad isko channel layer se wrap kar denge taaki messages aur async connection ban jaye over http with websocket . 
        
        await self.channel_layer.group_add(
            self.room_group_name ,
            self.channel_name 
        )
        
        # ab agar sub value hogi to isko accept kar lenge 
        
        await self.accept() 
        # connection accepted .
        
        print("Connection accepted !") 
        
        
    async def disconnect(self , close_code) : 
        await self.channel_layer.group_discard(
            self.room_group_name , 
            self.channel_name
        )
        print("Connection terminated !") 
        
        
        
    async def receive(self , text_data) : 
        text_data_json = json.loads(text_data)
        print("Data was received from the websocket !") 
        # all the message which was sent from the websocket js from front will be received here . 
        
        message = text_data_json["message"]
        roomId = text_data_json["roomId"]
        user = text_data_json["user"]
        roomName = text_data_json["roomName"]
        userId = text_data_json["userId"]
        
        await self.save_message(message , roomId , user , roomName)
        
        # this message was received from the websocket . this needs to be sent to the group .
        
        
        
        
        # that means to the channel_layer group me send karna hai . us group me jisme ye banda hai 
        
        
        await self.channel_layer.group_send(
            self.room_group_name ,
            {
                "type" : "send_message" , # this is the send message event handler . 
                "message" : message ,
                "roomId" : roomId , 
                "user" : user ,
                "roomName" : roomName ,
                "userId" : userId 
            }
        )    
        
        
    async def send_message(self , event) : 
        message = event["message"]
        roomId = event["roomId"]
        user = event["user"]
        roomName = event["roomName"]
        userId = event["userId"]
        # send this message to the websocket 
        
        await self.send(text_data = json.dumps(
            {
                "message" : message , 
                "roomId" : roomId , 
                "user" : user , 
                "roomName" : roomName ,
                "userId" : userId 
            }
        ))
        
        print("The data was sent to the websocket !") 
        
    @sync_to_async
    def save_message(self , message , roomId , user , roomName ): 
        user = User.objects.get(username = user)
        room = Chatroom.objects.get(roomname = roomName , id = roomId)
        message = Message(user = user , room = room , body = message)
        message.save()
        print(message)
        print("The message was saved !") 