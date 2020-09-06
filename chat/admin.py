from django.contrib import admin
from chat.models import Message, Thread


class MessageAdmin(admin.ModelAdmin):
    pass


class ThreadAdmin(admin.ModelAdmin):
    pass


admin.site.register(Message, MessageAdmin)
admin.site.register(Thread, ThreadAdmin)
