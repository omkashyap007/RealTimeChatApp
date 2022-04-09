from django.contrib import admin
from base.models import Topic , Message , Chatroom , Profile

admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Chatroom)
admin.site.register(Profile)