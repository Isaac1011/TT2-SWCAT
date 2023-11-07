# chatbot/views.py
from django.shortcuts import render
import openai
import spacy


# Cargar el modelo en español de spaCy
nlp = spacy.load("es_core_news_sm")

# Diccionario de preguntas y respuestas
faq = {
    "¿Cuál es el objetivo de las tutorías?": " Las tutorías en el IPN tienen el objetivo de fortalecer el aprendizaje para convertirlo en una experiencia significativa, apoyar la formación integral del alumno y ser una guía para alcanzar metas escolares de manera exitosa. La acción tutorial tiene las siguientes acciones: 1. Asesorar académicamente en temas difíciles. 2. Apoyar a elegir la trayectoria académica ideal para los alumnos. 3. Fomentar el desarrollo de capacidades, habilidades, valores y actitudes. 4. Guiar a los alumnos para encontrar las estrategias que permitan lograr aprendizajes significativos. 5. Promover la autonomía para mejorar el desarrollo personal y el desempeño académico. ",

    "¿Cuáles son las áreas de intervención de las tutorías?": "1. Sentido de pertenencia. Para que el alumno se reconozca con orgullo como parte del IPN. 2. Acompañamiento durante la trayectoria escolar. Con el fin de evitar de evitar el riesgo de rezago, reprobación o abandono. 3. Orientación sobre servicios trámites y apoyos económicos. Desde becas institucionales hasta guiar al alumno a actividades deportivas para su desarrollo integral 4. Atención especializada y canalización. Se tratan otros factores que afectan el rendimiento escolar que pueden orillar al alumno a abandonar sus estudios, como problemas familiares, económicos o de salud. Los tutores están preparados para identificar problemáticas del estudiante y dirigirlo a las instancias adecuadas para que reciba atención y ayuda especializada.",

    "¿Cómo inscribirme a una tutoría grupal?": "Para inscribirte a una tutoría grupal en SWCAT, debes seguir estos pasos: 1. Iniciar Sesión como Tutorado en SWCAT 2. Dar clic en 'Inscribirse a Tutoría Grupal' 3. Seleccionar la Tutoría Grupal de tu interés. Si ya estás inscrito en 3 tutorías no podrás incribirte 4. Listo, ya estás inscrito",

    "¿Cómo inscribirme a una tutoría individual?": "Para inscribirte a una tutoría individual en SWCAT debes ponerte en contacto con la Tutora o Tutor que deseas tomar la tutoría, tu Tutora o Tutor se encargará de crear la Tutoría Individual, solo necesitas tener una cuenta en SWCAT",

    "¿Cómo crear a una tutoría individual?": "Para inscribirte a una tutoría grupal en SWCAT, debes seguir estos pasos: 1. Iniciar Sesión como Tutor en SWCAT 2. Dar clic en 'Crear Tutoría Individual' 3. Seleccionar el Tutorado que desea tomar la tutoría, este debe una cuenta en SWCAT. Si ya estás inscrito en 3 tutorías no podrás incribirte 4. Darle un nombre a la tutoría individual 5.- Listo, se ha creado la tutoría individual",

    "¿Cómo crear a una tutoría grupal?": "Para inscribirte a una tutoría grupal en SWCAT, debes seguir estos pasos: 1. Iniciar Sesión como Tutor en SWCAT 2. Dar clic en 'Crear Tutoría Grupal' 3. Darle un nombre a la tutoría grupal 4. Definir el salón donde se impartirá la tutoría 5. Listo, se ha creado la tutoría grupal",

    "¿Qué es el Programa Institucional de Tutorías (PIT)?": "El Programa Institucional de Tutorías (PIT) es una estrategia que tiene como propósito organizar la tutoría en todas las Unidades Académicas del IPN para acompañar a los alumnos en temas personales y académicos, a lo largo de su trayectoria escolar. El PIT es una estrategia colaborativa para brindar acompañamiento personalizado a los estudiantes de nivel medio superior y superior durante su trayectoria escolar"
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

    print('Similitud')
    print(max_similarity)

    if max_similarity < 0.6:
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

    return render(request, 'chatbot.html', {'user_input': user_input,
                                            'bot_response': bot_response})
