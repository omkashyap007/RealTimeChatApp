from rest_framework.decorators import api_view
from rest_framework.response import Response 
from  base.models import Chatroom 
from base.api.serializers import ChatRoomSerializer

@api_view(["GET"])
def getRoutes(request) : 
    
    routes = [
        "GET/api",
        "GET/api/rooms" ,
        "GET/api/rooms/:id",
    ]
    
    return Response(routes)


def convert(rooms) : 
    big_l = []
    for i in rooms:
        l = []
        l.append(i.id)
        l.append(i.roomname)
        big_l.append(l)
    return big_l
        


@api_view(["GET"])
def getRooms(request) : 
    rooms = Chatroom.objects.all()
    serializer = ChatRoomSerializer(rooms , many= True)
    # data = convert(rooms)
    return Response(serializer.data)

 
    # return Response(rooms) 
    # this will give an error that json is not a serializer . 
    # the response(rooms) , rooms are the python list of objects . 
    # we have to make the serializers .
    # objects can not be converted to the json objects by their own 
    # use the serializers for that 
    

@api_view(["GET"])
def getRoom(request ,pk) : 
    room = Chatroom.objects.get(id=pk)
    serializer = ChatRoomSerializer(room , many= False)
    return Response(serializer.data)