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
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('registroTutor/', views.registro_tutor, name='registro_tutor'),
    # Vista principal Tutor
    path('menu/', views.menu, name='menu'),
    path('inicioSesionTutor/', views.inicio_sesion_tutor,
         name='inicio_sesion_tutor'),
    path('cerrarSesion/', views.cerrar_sesion,
         name='cerrar_sesion'),
    path('registroTutorado/', views.registro_tutorado, name='registro_tutorado'),
    path('inicioSesionTutorado/', views.inicio_sesion_tutorado,
         name='inicio_sesion_tutorado'),
    path('menu/crearTutoriaIndividual/', views.crear_tutoriaIndividual,
         name='crear_tutoriaIndividual'),
    path('menu/tutoriaIndividual/<int:tutoria_id>/',
         views.detalle_tutoriaIndividual, name='detalle_tutoriaIndividual'),
    path('menu/tutoriaIndividual/crearBitacora/<int:tutoria_id>/',
         views.bitacora_tutor_tutoriaIndividual, name='crear_bitacora_tutoriaIndividual'),
    path('menu/tutoriaIndividual/crearNota/<int:tutoria_id>/',
         views.nota_tutorado_tutoriaIndividual, name='crear_nota_tutoriaIndividual'),
    path('menu/crearTutoriaGrupal', views.crear_tutoriaGrupal,
         name='crear_tutoriaGrupal'),
    path('menu/tutoriaGrupal/<int:tutoria_id>',
         views.detalle_tutoriaGrupal, name='detalle_tutoriaGrupal')
]
