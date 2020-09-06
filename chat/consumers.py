import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Message, Thread, User
from django.db.models import Q


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None
        self.sender = None
        self.recipient = None
        self.thread = None

    def connect(self):
        self.sender = User.objects.get(
            username=self.scope['url_route']['kwargs']['sender']
        )
        self.recipient = User.objects.get(
            username=self.scope['url_route']['kwargs']['recipient']
        )
        self.thread = Thread.objects.get(Q(owner=self.sender) | Q(opponent=self.sender))
        self.room_group_name = 'thread_%s' % self.thread.pk

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']
        sender = text_data_json['sender']

        Message.objects.create(
            text=message_text,
            thread=self.thread,
            sender=self.sender,
        )

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender': sender,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': "{}: {}".format(sender, message)
        }))
