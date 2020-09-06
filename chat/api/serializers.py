from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from chat.models import Message, User, Thread


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(max_length=100, required=True)
    recipient = serializers.CharField(max_length=100, required=True)

    def validate_sender(self, username):
        try:
            sender = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("User {} doesn't exist".format(username))

        return username

    def validate_recipient(self, username):
        try:
            sender = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("User {} doesn't exist".format(username))

        return username

    def to_representation(self, instance):
        thread = instance.thread
        recipient = thread.owner
        if thread.owner == instance.sender:
            recipient = thread.opponent
        return {
            'text': instance.text,
            'sender': instance.sender.username,
            'recipient': recipient.username,
        }

    def create(self, validated_data):
        sender = User.objects.get(username=validated_data['sender'])
        recipient = User.objects.get(username=validated_data['recipient'])
        threads = Thread.objects.filter(Q(owner=sender) | Q(opponent=sender))
        if threads.exists():
            thread = threads.first()
        else:
            thread = Thread.objects.create(
                owner=sender,
                opponent=recipient,
            )
        message = Message.objects.create(
            text=validated_data['text'],
            thread=thread,
            sender=sender,
        )
        message.send()
        return message

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'text']



