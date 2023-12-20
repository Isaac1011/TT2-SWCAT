from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 3)  # Tiempo de espera entre solicitudes en segundos

    @task
    def access_homepage(self):
        self.client.get("")

    @task
    def access_menu(self):
        self.client.get("menu/")

    @task
    def register_tutor(self):
        self.client.get("registroTutor/")

    @task
    def register_tutorado(self):
        self.client.get("registroTutorado/")

    @task
    def inicioSesion_tutor(self):
        self.client.get("inicioSesionTutor/")

    @task
    def inicioSesion_tutorado(self):
        self.client.get("inicioSesionTutorado/")

    @task
    def cerrar_sesion(self):
        self.client.get("cerrarSesion/")

    @task
    def create_individual_meeting(self):
        tutoria_id = 1  # Puedes ajustar esto según tus necesidades
        url = f"crearReunionIndividual/{tutoria_id}/"
        self.client.get(url)

    @task
    def create_grupal_meeting(self):
        tutoria_id = 1  # Puedes ajustar esto según tus necesidades
        url = f"crearReunionGrupal/{tutoria_id}/"
        self.client.get(url)

    @task
    def access_chatbot(self):
        self.client.get("chatbot/")

    @task
    def access_material_didactico(self):
        self.client.get("materialDidactico/")

    @task
    def send_message(self):
        tutor_id = 1  # Puedes ajustar esto según tus necesidades
        tutorado_id = 1  # Puedes ajustar esto según tus necesidades
        url = f"menu/enviar_mensaje/{tutor_id}/{tutorado_id}/"
        self.client.get(url)

    @task
    def access_tutoria_individual(self):
        tutoria_id = 1  # Puedes ajustar esto según tus necesidades
        url = f"menu/detalleTutoriaIndividual/{tutoria_id}/"
        self.client.get(url)

    @task
    def access_tutorias_grupales(self):
        self.client.get("menu/tutoriasGrupales")

    @task
    def enroll_in_tutoria_grupal(self):
        tutoria_id = 1  # Puedes ajustar esto según tus necesidades
        url = f"menu/inscribirseTutoriaGrupal/{tutoria_id}"
        self.client.get(url)

    @task
    def search_tutoria_grupal(self):
        self.client.get("buscar_tutoria_grupal/")

    @task
    def create_tutoria_grupal(self):
        self.client.get("menu/crearTutoriaGrupal")

    @task
    def access_tutoria_grupal(self):
        tutoria_id = 1  # Puedes ajustar esto según tus necesidades
        url = f"menu/detalleTutoriaGrupal/{tutoria_id}"
        self.client.get(url)

    # Agrega más tareas según sea necesario para simular el comportamiento de los usuarios en tu aplicación
    # Por ejemplo, tareas para acceder a otras partes de tu aplicación como inicio de sesión, tutorías individuales, tutorías grupales, etc.

# Ejecuta Locust desde la línea de comandos
# locust -f locustfile.py
