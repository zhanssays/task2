from django.urls import path
from chat.views import ThreadMessageList, LoginView

app_name = 'chat'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('<slug:recipient>/', ThreadMessageList.as_view(), name='thread'),
]