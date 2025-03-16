import json
from channels.generic.websocket import AsyncWebsocketConsumer
# from django.contrib.auth.models import User
from home.models import CustomUser
from .models import Chat_Messages
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """ Establish a WebSocket connection for two users. """
        self.user = self.scope["user"]
        self.other_user_id = self.scope["url_route"]["kwargs"]["user_id"]

        if not self.user.is_authenticated:
            await self.close()
            return

        # Ensure both user IDs are different for private chat
        self.other_user = await sync_to_async(CustomUser.objects.get)(id=self.other_user_id)
        if not self.other_user or self.user.id == self.other_user.id:
            await self.close()
            return

        # Create a unique room name using both user IDs (sorted to avoid duplication)
        self.room_name = f"chat_{min(self.user.id, int(self.other_user_id))}_{max(self.user.id, int(self.other_user_id))}"

        # Join the WebSocket group
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """ Leave the WebSocket group on disconnect. """
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        """ Handle incoming messages. """
        data = json.loads(text_data)
        message = data["message"]
        receiver_id = data.get("receiver_id")

        if not receiver_id or receiver_id == self.user.id:
            return  # Prevent users from sending messages to themselves

        # Save message to database
        chat_message = await self.save_message(self.user.id, receiver_id, message)

        # Send message to WebSocket group
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat_message",
                "sender": self.user.username,
                "message": message,
                "created_at": chat_message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            },
        )

    async def chat_message(self, event):
        """ Send received message to WebSocket clients. """
        await self.send(text_data=json.dumps({
            "sender": event["sender"],
            "message": event["message"],
            "created_at": event["created_at"],
        }))

    @sync_to_async
    def save_message(self, sender_id, receiver_id, message):
        """ Save chat message to the database asynchronously. """
        sender = CustomUser.objects.get(id=sender_id)
        receiver = CustomUser.objects.get(id=receiver_id)
        return Chat_Messages.objects.create(sender=sender, receiver=receiver, message=message)
