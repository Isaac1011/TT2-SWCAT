"""
URL configuration for SWCAT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from crud import views
from zoom import views as viewsZoom
from chatbot import views as viewsChatbot


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),

    # Menú
    path('menu/', views.menu, name='menu'),

    # Registro
    path('registroTutor/', views.registro_tutor, name='registro_tutor'),
    path('registroTutorado/', views.registro_tutorado, name='registro_tutorado'),

    # Inicio sesión
    path('inicioSesionTutor/', views.inicio_sesion_tutor,
         name='inicio_sesion_tutor'),
    path('inicioSesionTutorado/', views.inicio_sesion_tutorado,
         name='inicio_sesion_tutorado'),

    # Cerrar sesión
    path('cerrarSesion/', views.cerrar_sesion,
         name='cerrar_sesion'),

    # Tutoría Individual
    path('menu/crearTutoriaIndividual/', views.crear_tutoriaIndividual,
         name='crear_tutoriaIndividual'),
    path('menu/detalleTutoriaIndividual/<int:tutoria_id>/',
         views.detalle_tutoriaIndividual, name='detalle_tutoriaIndividual'),
    path('menu/detalleTutoriaIndividual/detalleBitacoraIndividual/<int:id_tutoria>/',
         views.detalle_bitacora_individual, name='detalle_bitacora_individual'),
    path('menu/detalleTutoriaIndividual/detalleBitacoraIndividual/crearBitacoraIndividual/<int:tutoria_id>/',
         views.bitacora_tutor_tutoriaIndividual, name='crear_bitacora_tutoriaIndividual'),
    path('menu/detalleTutoriaIndividual/notasTutorado/<int:tutoria_id>/',
         views.notas_tutorado_tutoria_individual, name='notas_tutorado_tutoria_individual'),
    path('menu/detalleTutoriaIndividual/notasTutorado/crearNota/<int:tutoria_id>/',
         views.nota_tutorado_tutoriaIndividual, name='crear_nota_tutoriaIndividual'),

    # Tutoría Grupal
    path('menu/tutoriasGrupales', views.tutorias_grupales_disponibles,
         name='tutorias_grupales_disponibles'),
    path('menu/inscribirseTutoriaGrupal/<int:tutoria_id>',
         views.inscribirse_tutoria_grupal, name='inscribirse_tutoria_grupal'),
    path('buscar_tutoria_grupal/', views.buscar_tutoria_grupal,
         name='buscar_tutoria_grupal'),
    path('menu/crearTutoriaGrupal', views.crear_tutoriaGrupal,
         name='crear_tutoriaGrupal'),
    path('menu/detalleTutoriaGrupal/<int:tutoria_id>',
         views.detalle_tutoriaGrupal, name='detalle_tutoriaGrupal'),
    path('menu/detalleTutoriaGrupal/detalleBitacoraGrupal/<int:tutoria_id>/',
         views.detalle_bitacora_grupal, name='detalle_bitacora_grupal'),
    path('menu/detalleTutoriaGrupal/detalleBitacoraGrupal/crearBitacoraGrupal/<int:tutoria_id>/',
         views.bitacora_tutor_tutoriaGrupal, name='bitacora_tutor_tutoriaGrupal'),
    path('menu/detalleTutoriaGrupal/anunciosGrupales/<int:tutoria_id>/',
         views.anuncios_grupales_tutor, name='anuncios_grupales_tutor'),
    path('menu/detalleTutoriaGrupal/anunciosGrupales/crearAnuncio/<int:tutoria_id>/',
         views.anuncio_tutor_tutoriaGrupal, name='anuncio_tutor_tutoriaGrupal'),

    # Zoom
    path('verReuniones/', viewsZoom.zoom_meetings,
         name='zoom_meetings'),
    path('crearReunionIndividual/<int:tutoria_id>/',
         viewsZoom.crear_reunion_individual, name='crear_reunion_individual'),
    path('crearReunionGrupal/<int:tutoria_id>/',
         viewsZoom.crear_reunion_grupal, name='crear_reunion_grupal'),
    path('eliminarReunionIndividual/<int:reunion_id>/',
         viewsZoom.eliminar_reunion_individual, name='eliminar_reunion_individual'),
    path('eliminarReunionGrupal/<int:reunion_id>/',
         viewsZoom.eliminar_reunion_grupal, name='eliminar_reunion_grupal'),
    path('crear_reunion_instantanea/', viewsZoom.crear_reunion_instantanea,
         name='crear_reunion_instantanea'),

    # Chatbot
    path('menu/chatbot/', viewsChatbot.chatbot, name='chatbot'),

    # Materiales didácticos
    path('visor-imagenes/', views.visor_imagenes, name='visor_imagenes'),

]
