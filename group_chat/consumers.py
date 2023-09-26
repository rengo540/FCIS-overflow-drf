import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
from .models import Group
from channels.db import database_sync_to_async





class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        if self.user:
            print(self.user)
            
        self.user_groups = await self.get_user_groups(self.user)
        for group in self.user_groups:
            # Join room group
            await self.channel_layer.group_add(group.slug, self.channel_name)
        
        await self.accept()
        
    async def disconnect(self, code):
        for group in self.user_groups:
            await self.channel_layer.group_discard(
                group.slug, self.channel_name
            )
    
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        group=text_data_json["group"]
        message = self.user.username+" : "+message
        # Send message to room group
        await self.channel_layer.group_send(
            group, {"type": "chat.message", "message": message,"group":group}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        group = event["group"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message,"group":group}))
        
    @sync_to_async
    def get_user_groups(self,user):
        groups = Group.objects.filter(member=user)
        print(groups[0].name)
        return groups