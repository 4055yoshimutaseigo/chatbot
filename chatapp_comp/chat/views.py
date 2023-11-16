from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import openai

from .models import Message


def index(request):
    messages = Message.objects.order_by('-created_at').reverse()
    context = {'messages': messages}
    return render(request, 'chat/index.html', context)


def post(request):
    openai.api_key = ''

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "日本語で応答してください"
            },
            {
                "role": "user",
                "content": request.POST['contents']
            },
        ]
    )
    results = response["choices"][0]["message"]["content"]

    Message.objects.create(
        contents=request.POST['contents'],
        response=results,
        created_at=timezone.now()
    )
    return redirect('chat:index')
