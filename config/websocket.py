async def websocket_application(scope, receive, send):
    while True:
        event = await receive()

        if event["type"] == "websocket.connect":
            await send({"type": "websocket.accept"})

        if event["type"] == "websocket.disconnect":
            break

        if event["type"] == "websocket.receive":
            if event["text"] == "ping":
                await send({"type": "websocket.send", "text": "pong!"})

from channels.generic.websocket import JsonWebsocketConsumer

import json
from channels.generic.websocket import AsyncWebsocketConsumer



class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            "notifications",  # Group name
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "notifications",
            self.channel_name
        )

    def notify_book_available(self, event):
        book_title = event['book_title']
        self.send(text_data=json.dumps({
            'message': f'The book "{book_title}" is now available.'
        }))

