from django.views.generic import ListView, FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist


from chat.models import Message, Thread, User
from chat.forms import UserForm


class ThreadMessageList(ListView):
    template_name = 'chat/thread.html'

    def __init__(self):
        super().__init__()
        self.sender = None
        self.recipient = None

    def dispatch(self, request, *args, **kwargs):
        username = request.session.get('username', None)
        try:
            self.sender = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return redirect(reverse_lazy('chat:login'))

        self.recipient, created = User.objects.get_or_create(username=self.kwargs['recipient'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['sender'] = self.sender
        ctx['recipient'] = self.recipient
        return ctx

    def get_queryset(self):
        threads = Thread.objects.filter(Q(owner=self.sender) | Q(opponent=self.sender))
        if threads.exists():
            thread = threads.first()
        else:
            thread = Thread.objects.create(
                owner=self.sender,
                opponent=self.recipient,
            )
        return Message.objects.filter(thread=thread)


class LoginView(FormView):
    form_class = UserForm
    template_name = 'chat/login.html'

    def form_valid(self, form):
        request = self.request
        user, created = User.objects.get_or_create(username=form.cleaned_data['username'])
        request.session['username'] = user.username

        return HttpResponse("You can open a chat by opening chat/username")

