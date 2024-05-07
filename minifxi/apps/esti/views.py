

from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.urls import reverse_lazy
from django.shortcuts     import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View
from apps.gestion.models import EstimPeso, EstDetalle, Zdificultad, TaskFaseActividad, PeticionTipo, Requerimientos, AuthUser,Task,TaskEstado
from apps.esti.forms import *
import datetime
#import numpy as np
from django.db.models import Q



"""  ========================== E S T I M A C I Ó N  ===========================  """
	

class EstimCre(CreateView):
	model=EstimPeso
	form_class=EstimPesoForm
	template_name='esti/cre.html'
	success_url=reverse_lazy('estim_lis')

class EstimLis(ListView):
	model=EstimPeso
	template_name='esti/lis.html'

class EstimEdi(UpdateView):
	model=EstimPeso
	form_class=EstimPesoEdiForm
	template_name='esti/cre.html'
	success_url=reverse_lazy('estim_lis') 

class EstimEli(DeleteView):
	model=EstimPeso
	form_class=EstimPesoForm
	template_name='esti/eli.html'
	success_url=reverse_lazy('estim_lis')




#=======================  Servir peso de estimación  =========================#

class DetPeso(View):
	def get(self, request, *args, **kwargs):

		#
		tip = self.request.GET.get('tip') # TIPO
		sub = self.request.GET.get('sub') # SUBTIPO
		dif = self.request.GET.get('dif') # DIFICULTAD
		cli = self.request.GET.get('cli') # CLIENTE

		rpta = ' '
		if EstimPeso.objects.filter(tarea_tipo=tip,tarea_subtipo=sub,dificultad=dif).exists():
			rpta0 = EstimPeso.objects.filter(tarea_tipo=tip,tarea_subtipo=sub,dificultad=dif).count()
			if rpta0 != 1:
				rpta = 'm2'
			else:
				rpta = str(EstimPeso.objects.get(tarea_tipo=tip,tarea_subtipo=sub,dificultad=dif).peso)
		else:
			rpta = 'ne'
		return HttpResponse(rpta)

"""
ne = No existe
m2 = Mas de 2 configuraciones para ese peso
"""





#=======================  D E T   C R E A  =========================#


class DetCre(View):
	def get(self, request, *args, **kwargs):

		rpta = ''
		estdet = EstDetalle()

		estdet.esfuerzo = self.request.GET.get('esf') # ESFUERZO
		estdet.peso = self.request.GET.get('esf') # ESFUERZO
		estdet.creador = AuthUser.objects.get(pk=self.request.user.pk).alias
		estdet.fecha = datetime.datetime.now()

		# REQUERIMIENTO
		if Requerimientos.objects.filter(pk=int(self.request.GET.get('req'))).exists():
			estdet.requerimiento = Requerimientos.objects.get(pk=int(self.request.GET.get('req'))) 

			# TIPO
			if PeticionTipo.objects.filter(pk=int(self.request.GET.get('tip'))).exists() :
				estdet.tipo = PeticionTipo.objects.get(pk=int(self.request.GET.get('tip')))

				# SUBTIPO
				if TaskFaseActividad.objects.filter(pk=int(self.request.GET.get('sub'))).exists():
					estdet.suptipo = TaskFaseActividad.objects.get(pk=int(self.request.GET.get('sub')))

					# DIFICULTAD
					if Zdificultad.objects.filter(pk=int(self.request.GET.get('dif'))).exists():
						estdet.dificultad = Zdificultad.objects.get(pk=int(self.request.GET.get('dif')))
						estdet.save()
					else:
						rpta = 'ndf'
				else:
					rpta = 'nsb'
			else:
				rpta = 'nti'
		else:
			rpta = 'nrq'

		if rpta == '':
			rpta =  '{"alias":"' + estdet.creador + '",'
			rpta += ' "fecha":"' + str(estdet.fecha) + '",'
			rpta += ' "idest":"' + str(estdet.pk) + '"}'

		
		return HttpResponse(rpta)

"""
Err = Error en el servidor
ndf = Dificultad no encontrada
nsb = Subtipo no encontrado
nti = Tipo no encontrado
nrq = Requerimiento no encontrado.
"""




class DetApro(View):
	
	def get(self, request, *args, **kwargs):
		#si el requerimiento existe, falta aprobar y tiene estimación detalle
		
		
		
		if Requerimientos.objects.filter(pk=int(self.request.GET.get('req'))).exists() :
			req =  Requerimientos.objects.get(pk=int(self.request.GET.get('req')))
			estDet = EstDetalle.objects.filter(requerimiento=req)

			if req.estimacion_aprobada != 1  and estDet.exists():
				if estDet.exists():
					for detalle in estDet:
						lastIdInterno = Task.objects.last().id_interno
						cod = int(lastIdInterno[3:8]) + 1
						lastIdInterno = str(req.peticion.cliente.codigo).ljust(5- len(str(cod)),'0') if (5- len(str(cod)) ) > 0 else str(req.peticion.cliente.codigo)
						lastIdInterno = lastIdInterno + str(cod)

						task = Task(id_interno = lastIdInterno,
						requerimiento = req,
						responsable = AuthUser.objects.get(pk=self.request.user.pk),
						
						subtarea ='estimada',
						fase_actividad = detalle.suptipo,
						fecha_inicio = detalle.fecha,
						fecha_fin = detalle.fecha,
						esfuerzo_total_estandar = detalle.esfuerzo,
						esfuerzo_ejecutado = 0,
						estado =TaskEstado.objects.get(pk=1),
						subida_a_fenix = 0 )
						task.save()
					req.estimacion_aprobada=1
					req.save()
					return JsonResponse({'result':True})
				else:
					return JsonResponse({'result':False,'message':'sin estimación'})

			else:
				return JsonResponse({'result':False,'message':'estimación aprobada previamente'})
		else:
			return JsonResponse({'result':False,'message':'no existe requerimiento'})





class DetLis(View):
	def get(self, request, *args, **kwargs):

		rpta = ''
		
		
		# REQUERIMIENTO
		if Requerimientos.objects.filter(pk=int(self.request.GET.get('req'))).exists():
			req = Requerimientos.objects.get(pk=int(self.request.GET.get('req'))) 
			reqResponse = {
				'idrequerimiento':req.pk,
				'idpeticion':req.peticion.pk,
				'idtipo_peticion':req.peticion.tipo.pk,
				'tipo':req.peticion.tipo.tipo,
				'estimacion_aprobada':req.estimacion_aprobada
			}
			if EstDetalle.objects.filter(requerimiento=req).exists():
				lst_dest = EstDetalle.objects.filter(requerimiento=req)
				detalle = [] #ecarpiod
				cont = 0
				for x in lst_dest:
					detalle.append([
						x.pk, # '0'
						x.tipo.tipo, # '1'
						x.suptipo.fase_actividad, # '2'
						x.dificultad.dificultad, # '3'
						x.esfuerzo, # '4'
						x.creador, # '5'
						x.fecha, # '6'
						x.ajus_cantidad if x.ajus_cantidad != None else '', # '7'
						x.ajus_descripcion if x.ajus_descripcion != None else '', # '8'
						x.ajus_por.alias if x.ajus_por != None else '', # '9'
						x.ajus_fecha, # '10'
						x.peso # '11'
					])

				return JsonResponse({
					'req':reqResponse,
					'detalle':detalle
				})
			
			else:
				return JsonResponse({
					'req':reqResponse,
					'detalle':[]
				})		
		else:
			rpta = 'nrq'

		#print(" >> " + rpta )

		return HttpResponse(rpta)

"""
Err = Error en el servidor
sde = Sin estimaciones
"""





class DetEli(View):
	def get(self, request, *args, **kwargs):

		rpta = ''

		# REQUERIMIENTO
		if EstDetalle.objects.filter(pk=int(self.request.GET.get('detest'))).exists():
			EstDetalle.objects.get(pk=int(self.request.GET.get('detest'))).delete()
			rpta = 'Ok'
		else:
			rpta = 'nde'

		#print(" >> " + rpta )
		
		return HttpResponse(rpta)

"""
sde = No se encontró el datalle de la estimación
"""





class DetAjs(View):
	def get(self, request, *args, **kwargs):

		rpta = ''

		# REQUERIMIENTO
		if EstDetalle.objects.filter(pk=int(self.request.GET.get('det'))).exists():
			det = EstDetalle.objects.get(pk=int(self.request.GET.get('det')))

			if EstimPeso.objects.filter(Q(tarea_tipo=det.tipo.pk) & Q(tarea_subtipo=det.suptipo.pk) & Q(dificultad=det.dificultad.pk)).exists():
				lst_pes = EstimPeso.objects.filter(Q(tarea_tipo=det.tipo.pk) & Q(tarea_subtipo=det.suptipo.pk) & Q(dificultad=det.dificultad.pk))
				if lst_pes.count() == 1:
					pes = EstimPeso.objects.get(Q(tarea_tipo=det.tipo.pk) & Q(tarea_subtipo=det.suptipo.pk) & Q(dificultad=det.dificultad.pk))
					det.esfuerzo = ( float(pes.peso) + float(self.request.GET.get('ajs')))
					det.ajus_cantidad = float(self.request.GET.get('ajs'))
					det.ajus_descripcion = self.request.GET.get('des')
					det.ajus_por = AuthUser.objects.get(pk=self.request.user.pk)
					det.ajus_fecha = datetime.datetime.now()
					det.save()
					rpta = ''+str(det.esfuerzo)+''

				else:
					rpta = 'var'
			else:
				rpta = 'dne'
		else:
			rpta = 'nde'

		#print(" >> " + rpta )
		return HttpResponse(rpta)

"""
sde = No se encontró el datalle de la estimación
dne = Detalle no encontrado
var = Varios pesos conficurado para la msima convinación.
"""




class DetExp(View):
	def get(self, request, *args, **kwargs):

		# req
		req = self.request.GET.get('req')

		# Consulta de sp_
		from django.db import connection, transaction
		object_list = []		
		cursor = connection.cursor()
		cursor.execute("CALL sp_estim_exp ("+str(req)+")")
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
			#print(" >> "+str(dic))
		cursor.close()

		dicc = { 
			'object_list':object_list,
			'msj': "Guardar estimador",
		}
		return render(request,'esti/exp.html',dicc)


"""

"""



"""

    tarea_tipo = models.ForeignKey('PeticionTipo', models.DO_NOTHING, db_column='tarea_tipo')
    tarea_subtipo = models.ForeignKey('TaskFaseActividad', models.DO_NOTHING, db_column='tarea_subtipo')
    dificultad = models.ForeignKey('Zdificultad', models.DO_NOTHING, db_column='dificultad')
    peso = models.FloatField()
    peso_hist = models.FloatField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    alta = models.CharField(max_length=2, blank=True, null=True)


class EstDetalle(models.Model):
    id_est_det = models.AutoField(primary_key=True)
    requerimiento = models.ForeignKey('Requerimientos', models.DO_NOTHING, db_column='requerimiento')
    tipo = models.ForeignKey('PeticionTipo', models.DO_NOTHING, db_column='tipo')
    suptipo = models.ForeignKey('TaskFaseActividad', models.DO_NOTHING, db_column='suptipo')
    dificultad = models.ForeignKey('Zdificultad', models.DO_NOTHING, db_column='dificultad')
    esfuerzo = models.FloatField()
    creador = models.IntegerField()
    fecha = models.DateField()
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    ajus_cantidad = models.FloatField(blank=True, null=True)
    ajus_descripcion = models.CharField(max_length=100, blank=True, null=True)
    ajus_por = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='ajus_por', blank=True, null=True)
    ajus_fecha = models.DateField(blank=True, null=True)

"""

