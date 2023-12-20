from django.contrib import admin
from .models import Tutor, Tutorado, TutoriaIndividual, BitacoraIndividualTutor, NotasIndividualesTutorado, TutoriaGrupal, ListaTutoriaGrupal, BitacoraGrupalTutor, AnunciosGrupalesTutor, VideoconferenciasIndividuales, VideoconferenciasGrupales, Chat, Mensaje, TokenZoom

# Register your models here.
admin.site.register(Tutor)
admin.site.register(Tutorado)
admin.site.register(TutoriaIndividual)
admin.site.register(BitacoraIndividualTutor)
admin.site.register(NotasIndividualesTutorado)
admin.site.register(TutoriaGrupal)
admin.site.register(ListaTutoriaGrupal)
admin.site.register(BitacoraGrupalTutor)
admin.site.register(AnunciosGrupalesTutor)
admin.site.register(VideoconferenciasIndividuales)
admin.site.register(VideoconferenciasGrupales)
admin.site.register(Chat)

admin.site.register(TokenZoom)
