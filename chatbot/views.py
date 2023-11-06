# chatbot/views.py
from django.shortcuts import render
import openai
import spacy

# Cargar el modelo en español de spaCy
nlp = spacy.load("es_core_news_sm")

# Diccionario de preguntas y respuestas
faq = {
    "¿Cuál es el objetivo de las tutorías?": "El objetivo de las tutorías es proporcionar apoyo académico personalizado para ayudarte a comprender mejor los temas y mejorar tu rendimiento académico.",

    "¿Cómo inscribirme a una tutoría?": "Para inscribirte a una tutoría, debes seguir estos pasos: [Pasos detallados].",
}

# Función para encontrar la pregunta más similar en el diccionario de FAQ


def get_most_similar_question(user_question, faq):
    max_similarity = 0.0  # Índice de similitud, va de 0 a 1
    best_match = None  # Va a guardar la pregunta más similar

    for question, _ in faq.items():
        # Calcula la similitud semántica entre la pregunta del usuario y las preguntas del diccionario
        similarity = nlp(user_question).similarity(nlp(question))
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = question

    if max_similarity < 0.7:
        best_match = None

    return best_match


def chatbot(request):

    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        bot_response = None

        # Buscar la pregunta más similar en el diccionario de FAQ
        best_match = get_most_similar_question(user_input, faq)

        if best_match:
            # Si se encuentra una pregunta similar, muestra la respuesta correspondiente
            bot_response = faq[best_match]
        else:
            # Si no se encuentra una respuesta similar, llama a la API de OpenAI
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=user_input,
                # Ajusta este valor según tus necesidades (4096 como máximo)
                max_tokens=3900
            )
            bot_response = response.choices[0].text
    else:
        user_input = None
        bot_response = None

    return render(request, 'chatbot.html', {'bot_response': bot_response,
                                            'user_input': user_input})
