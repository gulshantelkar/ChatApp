
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
        else:
            self.roomGroupName =  self.user.username
            await self.channel_layer.group_add(
            self.roomGroupName ,
            self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
       await self.channel_layer.group_discard(
            self.roomGroupName ,
            self.channel_layer
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        recipient_username = data['recipient_username']


        try:
            recipient_user = await sync_to_async(User.objects.get)(username=recipient_username)
            
            if recipient_user.is_online:
                await self.channel_layer.group_send(
                    recipient_username, {
                        "type": "sendMessage",
                        "message": message,
                        "username": self.user.username,
                    }
                )
                await self.send(text_data=json.dumps({'message': 'message sent successfully'}))
            else:
                await self.send(text_data=json.dumps({'error': 'Recipient is offline or not available.'}))

        except User.DoesNotExist:
            await self.send(text_data=json.dumps({'error': 'Recipient is offline or not available.'}))

            
    async def sendMessage(self , event) :
        message = event["message"]
        username = event["username"]
        await self.send(text_data = json.dumps({"message":message ,"username":username}))

        

