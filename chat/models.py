from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class User(models.Model):
    username = models.CharField(max_length=100, unique=True, null=False, blank=False)

    def __str__(self):
        return self.username


class Thread(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    opponent = models.ForeignKey(User, on_delete=models.CASCADE)


class Message(models.Model):
    text = models.TextField(null=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

    def send(self):
        room_group_name = 'thread_%s' % self.thread.pk
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                'type': 'chat_message',
                "message": self.text,
                "sender": self.sender.username,
            }
        )

    def __str__(self):
        return "message from {}".format(self.sender)
