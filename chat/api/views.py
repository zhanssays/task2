from rest_framework import viewsets, mixins
from chat.models import Message
from chat.api.serializers import MessageSerializer


class MessageViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
