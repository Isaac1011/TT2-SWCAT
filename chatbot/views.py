# chatbot/views.py
from django.shortcuts import render
import openai


def chatbot(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=2048  # Ajusta este valor según tus necesidades
        )
        bot_response = response.choices[0].text
    else:
        bot_response = None

    return render(request, 'chatbot.html', {'bot_response': bot_response})
