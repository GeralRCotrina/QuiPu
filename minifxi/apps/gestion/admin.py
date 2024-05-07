from django.contrib import admin

from apps.gestion.models import *

admin.site.register(Peticion)
admin.site.register(Requerimientos)
admin.site.register(Task)
admin.site.register(ColCategoria)
admin.site.register(AuthUser)
admin.site.register(Cliente)
admin.site.register(Gant)
admin.site.register(ModulosSap)
admin.site.register(Pais)
admin.site.register(PeticionEstado)
admin.site.register(PeticionGestion)
admin.site.register(PeticionTipo)
admin.site.register(ReqCalidadInput)
admin.site.register(ReqEstado)
admin.site.register(ReqEstimAltoNivel)
admin.site.register(ReqPrioridad)
admin.site.register(Riesgo)
admin.site.register(RiesgoCategoria)
#admin.site.register(RiesgoEstado)
#admin.site.register(RiesgoResolucion)
#admin.site.register(RiesgoSeguimiento)
#admin.site.register(RiesgoTipo)
admin.site.register(TaskEstado)
admin.site.register(TaskFaseActividad)


