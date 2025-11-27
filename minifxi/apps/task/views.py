

from turtle import st
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View
from apps.gestion.models import *
#from apps.gestion.models import Task, Cliente, AuthUser, Requerimientos, TaskFaseActividad
from apps.task.forms import *
from django.db.models import Q
import datetime
import calendar

import json 


 
 

"""  =============================  T A S K ========================= """

class TaskCrearRef(CreateView):
	model=Task
	form_class=TaskForm
	template_name='task/crear.html'
	success_url=reverse_lazy('panel')

	def get_form(self, form_class=None):
		form=super(CreateView,self).get_form(form_class=self.form_class)
		form.fields["requerimiento"].queryset=Requerimientos.objects.filter(idrequerimiento=self.kwargs['pk'])
		form.fields["requerimiento"].initial=Requerimientos.objects.get(idrequerimiento=self.kwargs['pk'])
		return form

	def post(self,request,*args,**kwargs):

		# Creamos su código de task
		cod = CrearCodigoTask(self.request.POST.get('requerimiento'))

		# Get date
		if self.request.POST.get('fecha_fin') == '':
			fn = None
		else:
			fn = self.request.POST.get('fecha_fin')


		if self.request.POST.get('esfuerzo_total_estandar') == '':
			ete = 0
			ee = 0
		else:
			ete = self.request.POST.get('esfuerzo_total_estandar')
			ee = ete

		task = Task(id_interno = cod,
			requerimiento = Requerimientos.objects.get(pk=int(self.request.POST.get('requerimiento'))),
			responsable = AuthUser.objects.get(pk=self.request.user.pk),
			fecha_fin = fn,
			subtarea =self.request.POST.get('subtarea'),
			fase_actividad = TaskFaseActividad.objects.get(pk=int(self.request.POST.get('fase_actividad'))),
			fecha_inicio = self.request.POST.get('fecha_inicio'),
			esfuerzo_total_estandar = ete,
    		esfuerzo_ejecutado = ee,
    		estado =TaskEstado.objects.get(pk=1),
    		subida_a_fenix = 0 )
		task.save()
		return redirect('panel')




# Para actualizaciones rápidas
class TaskCrearRef_GRCL(CreateView):
	model=Task
	form_class=TaskForm
	template_name='task/crear.html'
	success_url=reverse_lazy('panel')

	def get_form(self, form_class=None):
		form=super(CreateView,self).get_form(form_class=self.form_class)
		form.fields["requerimiento"].queryset=Requerimientos.objects.filter(idrequerimiento=self.kwargs['pk'])
		form.fields["requerimiento"].initial=Requerimientos.objects.get(idrequerimiento=self.kwargs['pk'])
		return form

	def post(self,request,*args,**kwargs):

		# get last id
		# Creamos un Id Código par ala task ( 'Cod cliente' + 'Correlativo' )
		req01 = Requerimientos.objects.get(pk=int(self.request.POST.get('requerimiento')))
		cdg = req01.peticion.cliente.codigo
		task1 = Task.objects.filter(id_interno__contains=str(cdg)).last().id_interno
		cod = ''
		cod1 = 0
		print(" >>> ok 2")

		cod1 = int(task1[len(cdg):(len(cdg)+6)]) + 1
		#print("  >> "+str(len(cdg))+"  >> "+str(task1)+"  >> "+str(cod))
		if cod1 < 10:
			cod = str(req01.peticion.cliente.codigo)+'00000'+str(cod1)
		if cod1 < 100:
			cod = str(req01.peticion.cliente.codigo)+'0000'+str(cod1)
		elif cod1 < 1000:
			cod = str(req01.peticion.cliente.codigo)+'000'+str(cod1)
		elif cod1 < 10000:
			cod = str(req01.peticion.cliente.codigo)+'00'+str(cod1)
		elif cod1 < 100000:
			cod = str(req01.peticion.cliente.codigo)+'0'+str(cod1)
		else:
			cod = str(req01.peticion.cliente.codigo)+str(cod1)
		#print("  >> "+str(cod))

		# Get date
		if self.request.POST.get('fecha_fin') == '':
			fn = None
		else:
			fn = self.request.POST.get('fecha_fin')

		if self.request.POST.get('esfuerzo_total_estandar') == '':
			ete = 0
			ee = 0
		else:
			ete = self.request.POST.get('esfuerzo_total_estandar')
			ee = ete

		task = Task(id_interno = cod,
			requerimiento = req01,
			responsable = AuthUser.objects.get(pk=self.request.POST.get('responsable')),
			fecha_fin = fn,
			subtarea =self.request.POST.get('subtarea'),
			fase_actividad = TaskFaseActividad.objects.get(pk=int(self.request.POST.get('fase_actividad'))),
			fecha_inicio = fn,
			esfuerzo_total_estandar = ete,
    		esfuerzo_ejecutado = ee,
    		estado =TaskEstado.objects.get(pk=1),
    		subida_a_fenix = 0 )
		task.save()
		return redirect('panel')


class TaskCrear(CreateView):
	model=Task
	form_class=TaskForm
	template_name='task/crear.html'
	success_url=reverse_lazy('panel')


	def get_form(self, form_class=None):
		form=super(CreateView,self).get_form(form_class=self.form_class)
		form.fields["requerimiento"].queryset=Requerimientos.objects.filter(estado=1)
		return form

	def post(self,request,*args,**kwargs):

		# get last id
		req01 = Requerimientos.objects.get(pk=int(self.request.POST.get('requerimiento')))
		task1 = Task.objects.last().id_interno
		cod = ''
		
		print(" >>> "+str(task1))  # pro grcl4 22.04.2021
		tam = len(task1)
		tam2 = tam - 4
		cod = int(task1[tam2:tam]) + 1
		print(" >>> "+str(cod))


		if cod < 10:
			cod = str(req01.peticion.cliente.codigo)+'0000'+str(cod)
		elif cod < 100:
			cod = str(req01.peticion.cliente.codigo)+'000'+str(cod)
		elif cod < 1000:
			cod = str(req01.peticion.cliente.codigo)+'00'+str(cod)
		elif cod < 10000:
			cod = str(req01.peticion.cliente.codigo)+'0'+str(cod)
		else:
			cod = str(req01.peticion.cliente.codigo)+str(cod)


		if self.request.POST.get('fecha_fin') == '':
			fn = None
		else:
			fn = self.request.POST.get('fecha_fin')

		if self.request.POST.get('esfuerzo_ejecutado') == '':
			ee = 0
		else:
			ee = self.request.POST.get('esfuerzo_ejecutado')

		task = Task(id_interno = cod,
			requerimiento = Requerimientos.objects.get(pk=int(self.request.POST.get('requerimiento'))),
			responsable = AuthUser.objects.get(pk=self.request.user.pk),
			subtarea =self.request.POST.get('subtarea'),
			fase_actividad = TaskFaseActividad.objects.get(pk=int(self.request.POST.get('fase_actividad'))),
			fecha_inicio =self.request.POST.get('fecha_inicio'),
			fecha_fin = fn,
			esfuerzo_total_estandar =self.request.POST.get('esfuerzo_total_estandar'),
    		esfuerzo_ejecutado = ee,
    		estado =TaskEstado.objects.get(pk=1),
    		subida_a_fenix = 0 )
		task.save()
		return redirect('panel')
		
"""
task = Task(idtask = '',id_interno = '',requerimiento = '',responsable ='',subtarea = '',
	fase_actividad = '',fecha_inicio = '',fecha_fin = '', esfuerzo_total_estandar = '',
    esfuerzo_ejecutado ='', estado = '',subida_a_fenix ='',zultima_modificacion = '', zestado='')
"""

class TaskEliminar(DeleteView):
	model=Task
	form_class=TaskForm
	template_name='task/eliminar.html'
	success_url=reverse_lazy('panel')


""""
	def post(self,request,*args,**kwargs):
		if Task.objects.filter(pk=self.kwargs['pk']).exists():
			task_d=Task.objects.get(pk=self.kwargs['pk'])
			task_d.zestado=9
			task_d.save()
			LogDeAccion(str(self.request.user.pk),'task','ze',2,'9',task_d.pk, '')
		else:
			print("  > No está....")
		return redirect('task_listar')
"""






class TaskEditar(UpdateView):
	model = Task
	form_class = TaskEdiForm
	template_name = 'task/crear.html'
	success_url = reverse_lazy('panel') 

	def get_form(self, form_class=None):
		form=super(UpdateView,self).get_form(form_class=self.form_class)
		tsk = Task.objects.get(pk=self.kwargs['pk'])
		rqs = Requerimientos.objects.filter(peticion=tsk.requerimiento.peticion).exclude(estado=3)
		form.fields["requerimiento"].queryset= rqs
		return form




class TaskListar(View):

	def get(self,request,*args,**kwargs):

		clie = self.request.GET.get('clie')
		fecha_desde = self.request.GET.get('fecha_desde')
		fecha_hasta = self.request.GET.get('fecha_hasta')

		# Para el matcode de clientes
		obj2 = Cliente.objects.all()
		for ob in obj2:
			pass
		
		# Obtenemos el cliente para el filtro personalizado
		# Solo si la consulta no viene desde el listado
		# y si el usuario está asignado a algún cliente
		if clie == None:
			userpk = self.request.user.pk
			if AuthCliente.objects.filter( idauth = userpk ).exists():
				asig01 = AuthCliente.objects.filter( idauth = userpk ).first()
				clie = asig01.idcliente.pk
			else:
				clie = '0'

		# Contruímos las fechas de inicio y fin del mes		
		if fecha_desde == None:
			fh1 = datetime.datetime.now()
			fecha_desde = "'"+str(fh1.year)+"-"+str(fh1.month)+"-01'"
		if fecha_hasta == None:
			fh = datetime.datetime.now()
			cant_dias = calendar.monthrange(fh.year,fh.month)
			fecha_hasta = "'"+str(fh.year)+"-"+str(fh.month)+"-"+str(cant_dias[1])+"'"

		# Lanzamos el proc.
		from django.db import connection
		object_list = []		
		cursor = connection.cursor()
		if clie == '0':
			cursor.execute("CALL sp_task_x_fecha ("+str(fecha_desde)+","+str(fecha_hasta)+")")
		else:
			cursor.execute("CALL sp_task_x_fecha_1 ("+str(fecha_desde)+","+str(fecha_hasta)+","+str(clie)+")")
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
		cursor.close()

		# Bluid mensaje
		msj =  "Reporte de tareas entre el "+str(fecha_desde)+" hasta "+str(fecha_hasta)
		if clie != '0':
			for x in (x for x in obj2 if x.idcliente == int(clie)):
				msj = msj + " en "+str(x.cliente)

		# Diccionario.
		dicc = { 
			'object_list': object_list,
			'lst_cliente': obj2,
			'msj': msj
		}
		
		return render(request,'task/listar.html',dicc)




class TaskPorCodigo(View):

	def get(self,request,*args,**kwargs):
		idr = self.request.GET.get('idr')
		sf = self.request.GET.get('sf')

		# Para el matcode de clientes
		obj2 = Cliente.objects.all()
		for ob in obj2:
			pass
		
		# Optenemos el codigo
		if idr == 'mias':
			idr = AuthUser.objects.get(pk=int(self.request.user.pk)).codigo

		from django.db import connection
		object_list = []		
		cursor = connection.cursor()
		lv_qry = "CALL sp_task_x_resp ("+str(idr)+","+str(sf)+")"
		cursor.execute(lv_qry)
		resultado = cursor.fetchall()

		# print("  >> resultado : "+str(len(resultado))+"   idr : "+str(idr))  grcl /*
		print(" >>___________________"+lv_qry+"______________________")
		
		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
			print(" >> dic= "+str(dic))# grcl
		cursor.close()

		dicc = { 
			'object_list':object_list,
			'msj': "Tareas sin subir a fenix responsabilidad de "+str(idr)+".",
			'lst_cliente': obj2,
		}
		return render(request,'task/listar.html',dicc)



class TaskPorReq(View):

	def get(self,request,*args,**kwargs):
		idr = self.request.GET.get('idr')
		req = Requerimientos.objects.get(pk=int(idr))

		# Para el matcode de clientes
		obj2 = Cliente.objects.all()
		for ob in obj2:
			pass
		
		from django.db import connection
		object_list = []		
		cursor = connection.cursor()
		cursor.execute("CALL sp_task_x_req ("+str(idr)+")")
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
		cursor.close()

		dicc = { 
			'object_list':object_list,
			'lst_cliente': obj2,
			'msj': "Reporte de tareas por requerimiento "+str(req.codigo)+" - "+str(req.codigo_cliente)+" "+str(req.breve_descripcion)+".",
		}
		return render(request,'task/listar.html',dicc)



# Task por petición
class TaskXPet(View):

	def get(self,request,*args,**kwargs):
		idp = self.request.GET.get('idp')
		pet = Peticion.objects.get(pk=int(idp))

		# Para el matcode de clientes
		obj2 = Cliente.objects.all()
		for ob in obj2:
			pass
		
		from django.db import connection
		object_list = []		
		cursor = connection.cursor()
		cursor.execute("CALL sp_task_x_pet ("+str(idp)+")")
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
		cursor.close()

		dicc = { 
			'object_list':object_list,
			'lst_cliente': obj2,
			'msj': "Reporte de tareas por peticion "+pet.nombre+"."
		}
		return render(request,'task/listar.html',dicc)





class SubidaAFenix(View):
	def get(self, request, *args, **kwargs):
		idt = self.request.GET.get('idtask')
		rpta = '9'
		task1=Task.objects.get(idtask =int(idt))
		if task1.subida_a_fenix == '1':
			task1.subida_a_fenix = '0';
			task1.save();
			rpta = '0'
		elif task1.subida_a_fenix == '0' or task1.subida_a_fenix == '' :
			task1.subida_a_fenix = '1';
			task1.save();
			rpta = '1'
		else:
			rpta = '9'
		return HttpResponse(rpta)



class ActTask(View):
	def get(self, request, *args, **kwargs):
		idt = self.request.GET.get('idtask')
		campo = self.request.GET.get('campo')
		valor = self.request.GET.get('valor')

		rpta = '9'
		task1=Task.objects.get(idtask =int(idt))
			
		if campo == 'esfuerzo_total_estandar':
			task1.esfuerzo_total_estandar = valor
			task1.save();
			rpta = '1'
		elif campo == 'esfuerzo_ejecutado':
			task1.esfuerzo_ejecutado = valor
			task1.save();
			rpta = '1'
		else:
			rpta = '9'
		return HttpResponse(rpta)






class TaskACC(View):

	def get(self,request,*args,**kwargs):
		cod = self.request.GET.get('cod')
		rpta = ""
		dicc = {}
		if AuthUser.objects.filter(codigo=cod).exists():
			usu = AuthUser.objects.filter(codigo=cod).first()
			from django.db import connection
			object_list = []		
			cursor = connection.cursor()
			cursor.execute("CALL sp_acc_x_codigo ("+str(cod)+")")
			resultado = cursor.fetchall()

			for row in resultado:
				dic = dict(zip([col[0] for col in cursor.description], row))
				object_list.append(dic)
			cursor.close()
			
			dicc = {
				'object_list':object_list,
				'msj': "Reporte de ACC no cargadas a fenix de "+usu.alias+"."
			}
		else:
			dicc = { 
				'msj': "Código no encontrado."
			}
		
		return render(request,'task/acc.html',dicc)


# Crea varias tareas para un requerimiento
class TaskCreLst(View):

	def get(self,request,*args,**kwargs):

		idr = self.request.GET.get('idr')
		jsn = self.request.GET.get('jsn')
		rpta = '{"0":'
		#print("  >> idr: "+str(idr)+"   jsn: "+str(jsn))

		# Splits for convert in JSON 
		lst_jsn = jsn.split("~")
		rpta += '"ok"'

		# Eliminamos las que ya no regresan del frontend
		tsk_lst = Task.objects.filter(requerimiento=idr)
		if len(tsk_lst) > 0:
			for t in tsk_lst:
				flag = False
				for r in lst_jsn:
					if r != '':
						#pass
						js_tsk = json.loads(r)
						if int(js_tsk['idtsk']) == int(t.pk):
							flag = True
				# Validamos si está, si no la borramos
				if flag == True:
					pass
				else:
					#print("  > ... Se borra "+str(t.pk))
					flag = False
					t.delete()


		# Creamos o editamos las nuevas
		for x in lst_jsn:
			if x != '':
				#pass
				js_tsk = json.loads(x)
				#print("  >> -- > "+str(js_tsk))

				if js_tsk['idtsk'] == 0:
					tsk = Task()
					tsk.id_interno = CrearCodigoTask(js_tsk['idRequerimiento'])
					tsk.requerimiento = Requerimientos.objects.get(pk=int(js_tsk['idRequerimiento']))
					tsk.responsable = AuthUser.objects.get(pk=js_tsk['idEmpleado'])
					tsk.fecha_inicio =  js_tsk['fechaInicio']
					tsk.fecha_fin = js_tsk['fechaFin']
					tsk.subtarea = js_tsk['subTarea']
					tsk.fase_actividad = TaskFaseActividad.objects.get(pk=int(js_tsk['id_faseActividad']))
					tsk.esfuerzo_total_estandar = js_tsk['esfuerzoTotEstandar']
					tsk.esfuerzo_ejecutado = js_tsk['esfuerzoEjecutado'] #amjo Agregar "Esfuerzo ejecutado"
					tsk.estado = TaskEstado.objects.get(pk=1)
					tsk.subida_a_fenix = 0
					tsk.save()
					rpta += ',"'+js_tsk['idtsk_local']+'":"'+str(tsk.pk)+'~'+str(tsk.id_interno)+'~XXX"'
				
				else:
					if Task.objects.filter(idtask=js_tsk['idtsk']).exists():
						tsk = Task.objects.get(pk=js_tsk['idtsk'])
						tsk.responsable = AuthUser.objects.get(pk=js_tsk['idEmpleado'])
						tsk.fecha_inicio =  js_tsk['fechaInicio']
						tsk.fecha_fin = js_tsk['fechaFin']
						tsk.subtarea = js_tsk['subTarea']
						tsk.fase_actividad = TaskFaseActividad.objects.get(pk=int(js_tsk['id_faseActividad']))
						tsk.esfuerzo_total_estandar = js_tsk['esfuerzoTotEstandar']
						tsk.esfuerzo_ejecutado = js_tsk['esfuerzoEjecutado'] #amjo Agregar "Esfuerzo ejecutado"
						tsk.save()
						rpta += ',"'+js_tsk['idtsk_local']+'":"'+str(tsk.pk)+'~'+str(tsk.id_interno)+'~XXX"'
					else:
						print("    -3")

		rpta += '}'
		#print("  >> rpta : "+rpta)

		return HttpResponse(rpta)

""" 

"""





# grcl4
class TaskLstExt(View):
	def get(self,request,*args,**kwargs):

		idr = self.request.GET.get('idr')
		#print("  >> idr: "+str(idr))
 
		rpta = '{"0":'

		tsk_lst = Task.objects.filter(requerimiento=idr)

		if len(tsk_lst) > 0:
			rpta += '"ok"'
			cnt = 0
			for t in tsk_lst:			#print("    :->"+str(t))
				cnt += 1
				rpta += ',"id_tsk_local_'+str(cnt)+'":'			# *
				rpta += '"'+str(t.pk)							# 0
				rpta += '~'+t.id_interno 						# 1
				rpta += '~'+t.subtarea 							# 2
				rpta += '~'+t.fase_actividad.fase_actividad		# 3
				rpta += '~'+str(t.fecha_inicio)					# 4
				rpta += '~'+str(t.fecha_fin)					# 5
				rpta += '~'+str(t.esfuerzo_total_estandar)		# 6
				rpta += '~'+str(t.esfuerzo_ejecutado)			# 7
				rpta += '~'+t.responsable.alias					# 8
				rpta += '~'+str(t.responsable.pk)				# 9
				rpta += '~'+str(t.fase_actividad.pk)+'"'  		# 10
			rpta += '}'

		else:
			rpta += '"Vac"}'
		
		#print("  >> rpta : "+rpta)
		return HttpResponse(rpta)

"""
	'Vac' : Sin tareas aún

"""






def CrearCodigoTask(idr):

	# get last id
	# Creamos un Id Código par ala task ( 'Cod cliente' + 'Correlativo' )
	req01 = Requerimientos.objects.get(pk=int(idr))
	#cdg = req01.peticion.cliente.codigo --grcl 24.09.19
	# Tomamos las 3 primeras letras del nombre del cliente
	# para el código de la Task
	cdg = req01.peticion.cliente.cliente[0:3] 
	#print("------------> idr : "+str(idr)+" --|-- cdg: ´"+str(cdg)+"´")
	cod  = ''
	cod1 = 0

	if Task.objects.filter(id_interno__contains=str(cdg)).exists():
		task1 = Task.objects.filter(id_interno__contains=str(cdg)).last().id_interno
		#print(" -------------->> cdg :"+str(cdg)+"  tsk:"+str(task1))
		cod1 = int(task1[len(cdg):(len(cdg)+6)]) + 1
	else:
		cod1 = 0 + 1

	#print("  >> "+str(len(cdg))+"  >> +str(task1)+  >> "+str(cod))
	if cod1 < 10:
		cod = str(req01.peticion.cliente.cliente[0:3])+'00000'+str(cod1)
	if cod1 < 100:
		cod = str(req01.peticion.cliente.cliente[0:3])+'0000'+str(cod1)
	elif cod1 < 1000:
		cod = str(req01.peticion.cliente.cliente[0:3])+'000'+str(cod1)
	elif cod1 < 10000:
		cod = str(req01.peticion.cliente.cliente[0:3])+'00'+str(cod1)
	elif cod1 < 100000:
		cod = str(req01.peticion.cliente.cliente[0:3])+'0'+str(cod1)
	else:
		cod = str(req01.peticion.cliente.cliente[0:3])+str(cod1)
	#print("  >> Por def : "+str(cod))

	return cod





"""

		# get last id
		# Creamos un Id Código par ala task ( 'Cod cliente' + 'Correlativo' )
		req01 = Requerimientos.objects.get(pk=int(self.request.POST.get('requerimiento')))
		cdg = req01.peticion.cliente.codigo
		cod  = ''
		cod1 = 0
		print(" >>> ok 3")

		if Task.objects.filter(id_interno__contains=str(cdg)).exists():
			task1 = Task.objects.filter(id_interno__contains=str(cdg)).last().id_interno
			cod1 = int(task1[len(cdg):(len(cdg)+6)]) + 1
		else:
			cod1 = 0 + 1

		#print("  >> "+str(len(cdg))+"  >> "+str(task1)+"  >> "+str(cod))
		if cod1 < 10:
			cod = str(req01.peticion.cliente.codigo)+'00000'+str(cod1)
		if cod1 < 100:
			cod = str(req01.peticion.cliente.codigo)+'0000'+str(cod1)
		elif cod1 < 1000:
			cod = str(req01.peticion.cliente.codigo)+'000'+str(cod1)
		elif cod1 < 10000:
			cod = str(req01.peticion.cliente.codigo)+'00'+str(cod1)
		elif cod1 < 100000:
			cod = str(req01.peticion.cliente.codigo)+'0'+str(cod1)
		else:
			cod = str(req01.peticion.cliente.codigo)+str(cod1)
		#print("  >> "+str(cod))

		# Get date
		if self.request.POST.get('fecha_fin') == '':
			fn = None
		else:
			fn = self.request.POST.get('fecha_fin')


		if self.request.POST.get('esfuerzo_total_estandar') == '':
			ete = 0
			ee = 0
		else:
			ete = self.request.POST.get('esfuerzo_total_estandar')
			ee = ete

		task = Task(id_interno = cod,
			requerimiento = req01,
			responsable = AuthUser.objects.get(pk=self.request.user.pk),
			fecha_fin = fn,
			subtarea =self.request.POST.get('subtarea'),
			fase_actividad = TaskFaseActividad.objects.get(pk=int(self.request.POST.get('fase_actividad'))),
			fecha_inicio = self.request.POST.get('fecha_inicio'),
			esfuerzo_total_estandar = ete,
    		esfuerzo_ejecutado = ee,
    		estado =TaskEstado.objects.get(pk=1),
    		subida_a_fenix = 0 )
		task.save()
		return redirect('panel')


class Task(models.Model):
    idtask = models.AutoField(primary_key=True)
    id_interno = models.CharField(max_length=10,blank=True)
    requerimiento = models.ForeignKey(Requerimientos, models.DO_NOTHING, db_column='requerimiento')
    responsable = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='responsable')
    subtarea = models.CharField(max_length=100)
    fase_actividad = models.ForeignKey('TaskFaseActividad', models.DO_NOTHING, db_column='fase_actividad',default=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    esfuerzo_total_estandar = models.FloatField()
    esfuerzo_ejecutado = models.FloatField(blank=True, null=True)
    estado = models.ForeignKey('TaskEstado', models.DO_NOTHING, db_column='estado', blank=True ,default='1')
    subida_a_fenix = models.CharField(max_length=1, blank=True, null=True)
    zultima_modificacion = models.DateField(blank=True, null=True)
    zestado = models.CharField(max_length=1, blank=True, null=True,default='1')

"""










