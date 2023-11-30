# chatbot/views.py
from django.shortcuts import render, redirect
import openai
import spacy


# Cargar el modelo en español de spaCy
nlp = spacy.load("es_core_news_sm")

# Diccionario de preguntas y respuestas
faq = {

    # Preguntas acerca de las tutorías

    "¿Cuál es el objetivo de las tutorías?": " Las tutorías en el IPN tienen el objetivo de fortalecer el aprendizaje para convertirlo en una experiencia significativa, apoyar la formación integral del alumno y ser una guía para alcanzar metas escolares de manera exitosa. La acción tutorial tiene las siguientes acciones: \n\n1. Asesorar académicamente en temas difíciles. \n2. Apoyar a elegir la trayectoria académica ideal para los alumnos. \n3. Fomentar el desarrollo de capacidades, habilidades, valores y actitudes. \n4. Guiar a los alumnos para encontrar las estrategias que permitan lograr aprendizajes significativos. \n5. Promover la autonomía para mejorar el desarrollo personal y el desempeño académico. ",


    "¿Cuáles son las áreas de intervención de las tutorías?": "Las áreas de intervención de las tutorías en el IPN son la siguientes: \n\n1. Sentido de pertenencia. Para que el alumno se reconozca con orgullo como parte del IPN. \n2. Acompañamiento durante la trayectoria escolar. Con el fin de evitar de evitar el riesgo de rezago, reprobación o abandono. \n3. Orientación sobre servicios trámites y apoyos económicos. Desde becas institucionales hasta guiar al alumno a actividades deportivas para su desarrollo integral \n4. Atención especializada y canalización. Se tratan otros factores que afectan el rendimiento escolar que pueden orillar al alumno a abandonar sus estudios, como problemas familiares, económicos o de salud. Los tutores están preparados para identificar problemáticas del estudiante y dirigirlo a las instancias adecuadas para que reciba atención y ayuda especializada.",

    "¿Qué es el Programa Institucional de Tutorías?": "El Programa Institucional de Tutorías (PIT) es una estrategia que tiene como propósito organizar la tutoría en todas las Unidades Académicas del IPN para acompañar a los alumnos en temas personales y académicos, a lo largo de su trayectoria escolar. El PIT es una estrategia colaborativa para brindar acompañamiento personalizado a los estudiantes de nivel medio superior y superior durante su trayectoria escolar",

    "¿Qué es el PIT?": "El Programa Institucional de Tutorías (PIT) es una estrategia que tiene como propósito organizar la tutoría en todas las Unidades Académicas del IPN para acompañar a los alumnos en temas personales y académicos, a lo largo de su trayectoria escolar. El PIT es una estrategia colaborativa para brindar acompañamiento personalizado a los estudiantes de nivel medio superior y superior durante su trayectoria escolar",


    # Preguntas acerca del sistema SWCAT

    "¿Cómo inscribirme a una tutoría grupal?": "Para inscribirte a una tutoría grupal en SWCAT, debes seguir estos pasos: \n\n1. Iniciar Sesión como Tutorado en SWCAT \n2. Dar clic en 'Inscribirse a Tutoría Grupal' \n3. Identificar la Tutoría Grupal de tu interés, el sistema cuenta con un buscador donde ingresas el ID de la Tutoría Grupal que previamente te proporcionó tu Tutorado. \n4. Una vez seleccionada la Tutoría Grupal, ingresa al contraseña del grupo, esta contraseña debe ser proporcionada por tu Tutor que creó el grupo. Si ya estás inscrito en 3 tutorías no podrás incribirte \n5. Listo, ya estás inscrito",

    "¿Cómo inscribirme a una tutoría individual?": "Para inscribirte a una tutoría individual en SWCAT debes ponerte en contacto con la Tutora o Tutor que deseas tomar la tutoría, tu Tutora o Tutor se encargará de crear la Tutoría Individual, solo necesitas tener una cuenta en SWCAT",

    "¿Cómo crear a una tutoría individual?": "Para inscribirte a una tutoría grupal en SWCAT, debes seguir estos pasos: \n\n1. Iniciar Sesión como Tutor en SWCAT \n2. Dar clic en 'Crear Tutoría Individual' \n3. Seleccionar el Tutorado que desea tomar la tutoría, este debe una cuenta en SWCAT. Si ya estás inscrito en 3 tutorías no podrás incribirte \n4. Darle un nombre a la tutoría individual \n5.- Listo, se ha creado la tutoría individual",

    "¿Cómo crear a una tutoría grupal?": "Para inscribirte a una tutoría grupal en SWCAT, debes seguir estos pasos: \n\n1. Iniciar Sesión como Tutor en SWCAT \n2. Dar clic en 'Crear Tutoría Grupal' \n3. Darle un nombre a la tutoría grupal \n4. Definir el salón donde se impartirá la tutoría en caso de que se reunan presencialmente \n5. Listo, se ha creado la tutoría grupal",

    "¿Cómo crear una reunión?": "Para crear una reunión, ya sea de una Tutoría Individual o Grupal se deben seguir los siguientes pasos: \n\n1. Es necesario que la Tutora o Tutor actualicen su información para agregar su ID de Zoom, esto se hace dando clic en el nombre que aparece en el menú de inicio de la Tutora o Tutor. \n2. Una vez hecho lo anterior, se accede a la Tutoría que desea crear la reunión, dar clic en el botón azúl 'Crear reunión' y darle un nombre a la reunión. \n3. Listo, ahora aparecerá el botón verda para Iniciar la reunión para el Tutor y automáticamente le aparecerá el botón para Unirse a la Reunión a los Tutorados ",

    "¿Cómo puedo saber mi ID de Zoom?": "Para obtener el ID de una cuenta de Zoom se deben seguir los siguientes pasos:\n\n1. Descargar el software de Zoom en tu laptop o PC. \n2. Iniciar sesión o crear una cuenta de Zoom. \n3. Descargar el software Postman. \n4. Ingresar la siguiente URL en Postman y enviar la petición usando la petición 'GET'. \n5. En Postman aparecerá el ID de Zoom en el campo 'user_id'.",

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

    if max_similarity < 0.8:
        best_match = None

    return best_match


def chatbot(request):

    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un tutor, redirige al inicio.
    if request.method == 'POST':
        # Si el usuario hizo clic en una pregunta de FAQ, envía automáticamente esa pregunta al chatbot
        if 'faq_question' in request.POST:
            user_input = request.POST.get('faq_question')
        else:
            user_input = request.POST.get('user_input')

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

        # Obtener o inicializar la lista de conversaciones desde la sesión
        conversations = request.session.get('conversations', [])

        # Agregar la pregunta y respuesta actual a la lista de conversaciones
        conversations.append(
            {'user_input': user_input, 'bot_response': bot_response})

        # Actualizar la sesión con la nueva lista de conversaciones
        request.session['conversations'] = conversations
    else:
        user_input = None
        bot_response = None

    # Obtener la lista de conversaciones desde la sesión
    conversations = request.session.get('conversations', [])

    # Obtener el estado de inicio de sesión
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Verificar si el usuario está cerrando sesión
    if not logged_in:
        # Limpiar la lista de conversaciones si el usuario cierra sesión
        request.session['conversations'] = []

    return render(request, 'chatbot.html', {'user_input': user_input,
                                            'bot_response': bot_response,
                                            'logged_in': logged_in,
                                            'rol': rol,
                                            'conversations': conversations,
                                            'faq': faq, })
