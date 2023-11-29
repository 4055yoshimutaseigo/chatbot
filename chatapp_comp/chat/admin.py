from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ['contents', 'created_at']



admin.site.register(Message, MessageAdmin)

# Register your models here.
