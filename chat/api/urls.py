from django.urls import include, path
from rest_framework.routers import DefaultRouter
from chat.api.views import MessageViewSet

app_name = 'chat_api'

router = DefaultRouter()
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('chat/', include(router.urls)),
]
