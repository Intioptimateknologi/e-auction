from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

class PracticeConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(
            "auction", self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard('auction', self.channel_name)


    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        print(text_data)
        if text_data == 'PING':
            await self.send('PONG')
    
    async def on_message(self, event):
        print(event)
        message = event["status"]
        await self.send(text_data=message) #json.dumps({"message": message}))
        #await self.send_json(message)