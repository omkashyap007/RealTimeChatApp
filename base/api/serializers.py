from rest_framework.serializers import ModelSerializer
from base.models import Chatroom

class ChatRoomSerializer(ModelSerializer) :
    class Meta : 
        model = Chatroom
        fields = "__all__"
        # this means take the model and serialize it  