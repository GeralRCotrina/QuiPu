

from django.db import connection
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, View
from apps.gestion.models  import *
from apps.gestion.gv_view import *
from apps.requ.forms import *
import datetime
from django.contrib import messages
from django.db.models import Q





"""  =============================== R E Q U E R I M  I E N T O --------------------- """

class ReqCrearRef(CreateView):
	model=Requerimientos
	form_class=ReqForm
	template_name='requ/crear.html'
	success_url=reverse_lazy('req_listar')


	def get_form(self, form_class=None):

		# Values
		idp = self.kwargs['pk']
		form=super(CreateView,self).get_form(form_class=self.form_class)
		form.fields["peticion"].queryset=Peticion.objects.filter(idpeticion=idp)
		form.fields["peticion"].initial=Peticion.objects.get(idpeticion=idp)
		#	Construir código
		pet = Peticion.objects.get(idpeticion=self.kwargs['pk'])
		corr = pet.cliente.correlativo
		form.fields["codigo"].initial=CrearCodigoReq(corr)
		# Get Client
		clie = ''
		if AuthCliente.objects.filter(idauth=self.request.user.pk).exists():
			clie = AuthCliente.objects.filter(idauth=self.request.user.pk).first().idcliente
		else:
			clie = 1
		form.fields["responsable"].queryset = ObtLstCol(clie.pk,'','')# Colaboradores con asignación activa
		form.fields["responsable"].initial = AuthUser.objects.get(pk=self.request.user.pk)
		return form


	def post(self,request,*args,**kwargs):

		reqs = Requerimientos()
		reqs.codigo=self.request.POST.get('codigo')
		if self.request.POST.get('requerimien_asociado') != '':
			reqs.requerimien_asociado=self.request.POST.get('requerimien_asociado')
		reqs.modulo = ModulosSap.objects.get(pk=int(self.request.POST.get('modulo')))
		reqs.codigo_cliente = self.request.POST.get('codigo_cliente')
		reqs.breve_descripcion = self.request.POST.get('breve_descripcion')
		reqs.descripcion = self.request.POST.get('descripcion')
		reqs.peticion = Peticion.objects.get(pk=int(self.request.POST.get('peticion')))
		reqs.contacto=self.request.POST.get('contacto')

		#reqs.fecha_estimacion= self.request.POST.get('fecha_estimacion')
		reqs.fecha_estimacion = datetime.datetime.now()

		reqs.fecha_inicio_planificada= self.request.POST.get('fecha_inicio_planificada')
		if self.request.POST.get('fehca_inicio_real') != '':
			reqs.fehca_inicio_real= self.request.POST.get('fehca_inicio_real')		
		reqs.fecha_fin_planificada= self.request.POST.get('fecha_fin_planificada')
		if self.request.POST.get('fecha_entrega_real') != '':
			reqs.fecha_entrega_real= self.request.POST.get('fecha_entrega_real')
		reqs.calidad_input = ReqCalidadInput.objects.get(pk=2)
		reqs.estimacion_alto_nivel = ReqEstimAltoNivel.objects.get(pk=1)
		reqs.prioridad =ReqPrioridad.objects.get(pk=self.request.POST.get('prioridad'))
		if self.request.POST.get('estimacion_acuerdo') != '':
			reqs.estimacion_acuerdo =self.request.POST.get('estimacion_acuerdo')
		if self.request.POST.get('estimacion_fenix_h') != '':
			reqs.estimacion_fenix_h =self.request.POST.get('estimacion_fenix_h')
		if self.request.POST.get('horas_adicionales') != '':
			reqs.horas_adicionale=self.request.POST.get('horas_adicionales')

		#GRCL  -> ( Valores para actualozaciones masivas )
		#reqs.estado = PeticionEstado.objects.get(pk=1)
		reqs.estado = PeticionEstado.objects.get(pk=int(self.request.POST.get('estado')))
		reqs.responsable=AuthUser.objects.get(pk=self.request.user.pk)
		#reqs.responsable=AuthUser.objects.get(pk=int(self.request.POST.get('responsable')))

		if self.request.POST.get('horas_acuerddo_mes') != '':
			reqs.horas_acuerddo_mes = self.request.POST.get('horas_acuerddo_mes')
		reqs.seguimiento_diario = self.request.POST.get('seguimiento_diario')
		reqs.ordent = self.request.POST.get('ordent')
		reqs.programas = self.request.POST.get('programas')
		reqs.save()
		return redirect('dai_lis') 
		

	def get(self, request, *args, **kwargs):
		self.object = None
		idp = self.kwargs['pk']
		# Validar Pet no contenedora
		pet = Peticion.objects.filter(idpeticion=idp).first()
		lst_req = Requerimientos.objects.filter(peticion=pet)
		if pet.contenedora != 'on':
			if len(lst_req) >= 1:
				self.template_name  = 'peti/no-cont.html'
		return super().get(request, *args, **kwargs)


		# LogDeAccion(usuario, tabla, campo, tipo_de_modificación,  pk_de_la_entidad, mensaje_de_log):
		# TM (Tipo de modificación) Create:0		Read:1		Update:2		Delete:3
		#LogDeAccion(self.request.user.pk,'REQUERIMIENTO','-',0,reqs.pk, (str(reqs.codigo)+' : '+str(reqs.breve_descripcion)))



def CrearCodigoReq(corr):
	fh1 = datetime.datetime.now()
	mm = fh1.month
	dd = fh1.day	
	if mm <= 9:
		mm = "0"+str(mm)
	if dd <= 9:
		dd = "0"+str(dd)
	valida = True
	while valida:
		codigo1 = ""+str(fh1.year)+""+str(mm)+""+str(dd)+"_"+str(corr)
		if Requerimientos.objects.filter(codigo=codigo1).exists():
			corr+=1
		else:
			valida = False
	return codigo1




class ReqCrear(CreateView):
	model=Requerimientos
	form_class=ReqForm
	template_name='requ/crear.html'
	success_url=reverse_lazy('req_listar')

	def get_form(self, form_class=None):
		form=super(CreateView,self).get_form(form_class=self.form_class)
		form.fields["peticion"].queryset=Peticion.objects.filter(estado=1)
		return form


	def post(self,request,*args,**kwargs):

		reqs = Requerimientos()
		reqs.codigo=self.request.POST.get('codigo')
		if self.request.POST.get('requerimien_asociado') != '':
			reqs.requerimien_asociado=self.request.POST.get('requerimien_asociado')
		#reqs.requerimien_asociado=str(self.request.POST.get('requerimien_asociado'))
		reqs.modulo = ModulosSap.objects.get(pk=int(self.request.POST.get('modulo')))
		reqs.codigo_cliente = self.request.POST.get('codigo_cliente')
		reqs.breve_descripcion = self.request.POST.get('breve_descripcion')
		reqs.descripcion = self.request.POST.get('descripcion')
		reqs.peticion = Peticion.objects.get(pk=int(self.request.POST.get('peticion')))
		

		reqs.contacto=self.request.POST.get('contacto')
		reqs.fecha_estimacion= self.request.POST.get('fecha_estimacion')
		reqs.fecha_inicio_planificada= self.request.POST.get('fecha_inicio_planificada')
		if self.request.POST.get('fehca_inicio_real') != '':
			reqs.fehca_inicio_real= self.request.POST.get('fehca_inicio_real')		
		reqs.fecha_fin_planificada= self.request.POST.get('fecha_fin_planificada')
		if self.request.POST.get('fecha_entrega_real') != '':
			reqs.fecha_entrega_real= self.request.POST.get('fecha_entrega_real')
		reqs.calidad_input = ReqCalidadInput.objects.get(pk=2)
		reqs.estimacion_alto_nivel = ReqEstimAltoNivel.objects.get(pk=1)
		reqs.prioridad =ReqPrioridad.objects.get(pk=3)
		if self.request.POST.get('estimacion_acuerdo') != '':
			reqs.estimacion_acuerdo =self.request.POST.get('estimacion_acuerdo')
		if self.request.POST.get('estimacion_fenix_h') != '':
			reqs.estimacion_fenix_h =self.request.POST.get('estimacion_fenix_h')
		if self.request.POST.get('horas_adicionales') != '':
			reqs.horas_adicionale=self.request.POST.get('horas_adicionales')

		#GRCL  -> ( Valores para actualozaciones masivas )
		reqs.responsable=AuthUser.objects.get(pk=self.request.user.pk)
		#reqs.responsable=AuthUser.objects.get(pk=int(self.request.POST.get('responsable')))
		reqs.estado = PeticionEstado.objects.get(pk=1)
		#reqs.estado = PeticionEstado.objects.get(pk=int(self.request.POST.get('estado')))

		if self.request.POST.get('horas_acuerddo_mes') != '':
			reqs.horas_acuerddo_mes = self.request.POST.get('horas_acuerddo_mes')
		reqs.seguimiento_diario = self.request.POST.get('seguimiento_diario')
		reqs.zultima_modificacion = self.request.POST.get('fecha_estimacion')
		    
		reqs.save()		
		#return redirect('req_listar')
		return redirect('dai_lis')
		


class ReqEliminar(DeleteView):
	model=Requerimientos
	form_class=ReqForm
	template_name='requ/eliminar.html'
	success_url=reverse_lazy('dai_lis') # ('req_listar')

	def post(self,request,*args,**kwargs): 
		if Requerimientos.objects.filter(pk=self.kwargs['pk']).exists():
			req_d=Requerimientos.objects.get(pk=self.kwargs['pk'])
			LogDeAccion(self.request.user.pk,req_d.peticion.cliente,'REQUERIMIENTO','-','3',req_d.pk, (str(req_d.codigo)+':'+str(req_d.breve_descripcion)))
			req_d.delete()
		return redirect('dai_lis')

# LogDeAccion(usuario, tabla, campo, tipo_de_modificación,  pk_de_la_entidad, mensaje_de_log):




class ReqEditar(UpdateView):
	model=Requerimientos
	form_class=ReqEditForm
	template_name='requ/crear.html'
	success_url=reverse_lazy('dai_lis') #('req_listar') 

	def get_form(self, form_class=None):
		form = super(UpdateView,self).get_form(form_class=self.form_class)
		# Obtenemos el cliente 
		clie = ''
		if Requerimientos.objects.filter(pk=self.object.pk).exists():
			req = Requerimientos.objects.filter(pk=self.object.pk).first()
			clie = req.peticion.cliente
		else:
			clie = AuthCliente.objects.first()
		
		form.fields["peticion"].queryset=Peticion.objects.filter(Q(estado=1) & Q(cliente=clie)) 
		form.fields["responsable"].queryset= ObtLstCol(clie.pk,'','')# Colaboradores con asignación activa
		return form






class ReqListar(View):

	def get(self,request,*args,**kwargs):

		clie = self.request.GET.get('clie')
		fecha_desde = self.request.GET.get('fecha_desde')
		fecha_hasta = self.request.GET.get('fecha_hasta')
		#print(" >> "+str(clie)+" - "+str(fecha_desde)+" - "+str(fecha_hasta) )


		# Get TIPO ESTIM
		obj_tpo = PeticionTipo.objects.all()
		for otpo in obj_tpo:
			pass


		# Get TASK FASE DE ACTIVIDAD
		obj_fa = TaskFaseActividad.objects.all()
		cad = ''
		for fa in obj_fa:
			cad += '-'+str(fa.pk)
		#print("  >>"+cad)


		# Get TIPO ESTIM
		obj_zdi = Zdificultad.objects.all()
		for zd in obj_zdi:
			pass


		# Para el matcode de clientes
		obj2 = Cliente.objects.all()
		for ob in obj2:
			pass



		# Obtenemos el cliente para el filtro personalizado
		if clie == None:
			clie = MiCliente(self.request.user.pk)


		# Obtenemos el equipo asignado
		#equi = MiEquipo(clie)
		#print(" >> "+str(equi))


		if fecha_desde == None:
			fh1 = datetime.datetime.now()
			(fecha_desde,fecha_hasta) = ObtUltDiaDelMes(str(fh1.year),str(fh1.month))
			fecha_desde = "'"+fecha_desde+"'"
			fecha_hasta = "'"+fecha_hasta+"'"
		#print(" >.> fd: "+str(fecha_desde)+"    ff: "+str(fecha_hasta))



		# Colaboradores con asignación activa
		lst_usrs = ObtLstCol(clie,'','')
		for it in lst_usrs:
			pass#print("   "+str(it))



		#from django.db import connection, transaction
		object_list = []		
		cursor = connection.cursor()
		if clie == '0':
			cursor.execute("CALL sp_req_x_fecha ("+str(fecha_desde)+","+str(fecha_hasta)+")")
		else:
			cursor.execute("CALL sp_req_x_fecha_1 ("+str(fecha_desde)+","+str(fecha_hasta)+","+str(clie)+")")
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
			#print(" >>"+str(dic['etc']))
		cursor.close()

		# Bluid mensaje
		msj ="Reporte de requerimientos entre el "+fecha_desde+" hasta "+fecha_hasta
		if clie != '0':
			for x in (x for x in obj2 if x.idcliente == int(clie)):
				msj = msj + " en "+x.cliente


		# Build response
		dicc = { 
			'object_list':object_list,
			'lst_cliente': obj2,
			'obj_tpo': obj_tpo,
			'obj_zdi': obj_zdi,
			'msj': msj,
			'obj_fa': obj_fa,
			'lst_usrs': lst_usrs
		}
		return render(request,'requ/listar.html',dicc)




class ReqFilt(View): 

	def get(self,request,*args,**kwargs):

		filt = self.request.GET.get('filt')

		# Get TIPO ESTIM
		obj_tpo = PeticionTipo.objects.all()
		for otpo in obj_tpo:
			pass


		# Get TASK FASE DE ACTIVIDAD
		obj_fa = TaskFaseActividad.objects.all()
		cad = ''
		for fa in obj_fa:
			cad += '-'+str(fa.pk)
		#print("  >>"+cad)


		# Get TIPO ESTIM
		obj_zdi = Zdificultad.objects.all()
		for zd in obj_zdi:
			pass


		# Para el matcode de clientes
		obj2 = Cliente.objects.all()
		for ob in obj2:
			pass
		
		# Obtenemos el cliente para el filtro personalizado
		clie = MiCliente(self.request.user.pk)
		
		# Obtenemos el equipo asignado 
		equi = MiEquipo(clie)

		
		# Colaboradores con asignación activa
		lst_usrs = ObtLstCol(clie,'','')
		for it in lst_usrs:
			pass#print("   "+str(it))



		#from django.db import connection, transaction
		object_list = []		
		cursor = connection.cursor()
		cursor.execute("CALL sp_001_req_filt ("+str(equi.pk)+",'%"+str(filt)+"%')")
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic) #print(" >>"+str(dic['etc']))
		cursor.close()

		# Bluid mensaje
		msj ="Reporte de requerimientos para el filtro '"+filt+"'"
		if clie != '0':
			for x in (x for x in obj2 if x.idcliente == int(clie)):
				msj = msj + " en "+x.cliente


		# Build response
		dicc = { 
			'object_list':object_list,
			'lst_cliente': obj2,
			'obj_tpo': obj_tpo,
			'obj_zdi': obj_zdi,
			'msj': msj,
			'obj_fa': obj_fa,
			'lst_usrs': lst_usrs
		}
		return render(request,'requ/listar.html',dicc)








class ReqPorPet(View):

	def get(self,request,*args,**kwargs):
		idp = self.request.GET.get('idp')
		pet = Peticion.objects.get(pk=int(idp))


		# Para el matcode de clientes
		obj2 = Cliente.objects.all()
		for ob in obj2:
			pass


		# Get TASK FASE DE ACTIVIDAD
		obj_fa = TaskFaseActividad.objects.all()
		for fa in obj_fa:
			pass


		# Obtenemos el cliente para el filtro personalizado
		clie = MiCliente(self.request.user.pk)

		
		# Colaboradores con asignación activa
		lst_usrs = ObtLstCol(clie,'','')
		for it in lst_usrs:
			pass#print("   "+str(it))



		# Consulta de sp_
		#from django.db import connection, transaction
		object_list = []		
		cursor = connection.cursor()
		cursor.execute("CALL sp_req_x_pet ("+str(idp)+")")
		#cursor.execute("CALL sp_req_x_pet ("+str(idp)+")")
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
		cursor.close()

		dicc = { 
			'object_list':object_list,
			'obj_fa': obj_fa,
			'lst_usrs': lst_usrs,
			'msj': "Reporte de requerimientos por Petición ["+pet.nombre+"]",
			'lst_cliente': obj2
		}
		return render(request,'requ/listar.html',dicc)








class ReqAgrComn(View):
	def get(self, request, *args, **kwargs):
		idr = self.request.GET.get('idreq')
		campo = self.request.GET.get('campo')
		valor = self.request.GET.get('valor')

		print("   -> val: "+valor + "    ~id: "+str(idr) )

		rpta = '9'
		if Requerimientos.objects.filter(idrequerimiento =int(idr)).exists():
			reque=Requerimientos.objects.get(idrequerimiento =int(idr))
				
			if campo == 'comentario':
				reque.seguimiento_diario = valor
				reque.save()
				rpta = '1'
		return HttpResponse(rpta)




#  Agregar la bitácora del requerimiento.
class ReqBita(UpdateView):
	model=Requerimientos
	form_class=ReqBitaForm
	template_name='requ/bita.html'
	success_url=reverse_lazy('panel') 


# grcl4
# Actualiza la bitácora, OT y Programas_modificados por POST
class ReqUpdBit(View):
	def get(self, request, *args, **kwargs):
		print("  >> Get")
		return HttpResponse('Ok')

	def post(self,request,*args,**kwargs):
		rpta = 'Ok'
		req = Requerimientos.objects.get(pk=int(self.kwargs['pk']))
		if ValidaCliente(self.request.user.pk,req.peticion.cliente.pk):
			req.ordent = self.request.POST.get('ordent')
			req.seguimiento_diario = self.request.POST.get('seguimiento_diario')
			req.programas = self.request.POST.get('programas')
			req.save()
		else:
			rpta = 'NEq'
		return HttpResponse(rpta)



# Crea una copia del req.
class ReqDuplic(UpdateView):
	model=Requerimientos
	form_class=ReqDupForm
	template_name='requ/crear.html'
	success_url=reverse_lazy('dai_lis') # ('req_listar')

	def get_form(self, form_class=None):
		# Obtenemos el cliente 
		clie = ''
		if Requerimientos.objects.filter(pk=self.object.pk).exists():
			req = Requerimientos.objects.get(pk=self.object.pk)
			clie = req.peticion.cliente
		else:
			clie = AuthCliente.objects.all()
		form=super(UpdateView,self).get_form(form_class=self.form_class)
		form.fields["peticion"].queryset=Peticion.objects.filter( Q(estado=1) & Q(cliente=clie) )
		form.fields["responsable"].queryset= ObtLstCol(clie.pk,'','')# Colaboradores con asignación activa
		return form

	def post(self,request,*args,**kwargs):
		reqs = Requerimientos()
		reqs.codigo = self.request.POST.get('codigo')
		if self.request.POST.get('requerimien_asociado') != '':
			reqs.requerimien_asociado=self.request.POST.get('requerimien_asociado')
		reqs.modulo = ModulosSap.objects.get(pk=int(self.request.POST.get('modulo')))
		if self.request.POST.get('codigo_cliente') != '':
			reqs.codigo_cliente=self.request.POST.get('codigo_cliente')
		reqs.peticion = Peticion.objects.get(pk=int(self.request.POST.get('peticion')))
		reqs.responsable=AuthUser.objects.get(pk=int(self.request.POST.get('responsable')))
		reqs.breve_descripcion = self.request.POST.get('breve_descripcion')
		reqs.descripcion = self.request.POST.get('descripcion')
		reqs.contacto=self.request.POST.get('contacto')
		reqs.fecha_estimacion = datetime.datetime.now()
		#dte = self.request.POST.get('fecha_estimacion')#print("   ->"+dte+'-'+dte[6:10]+'-'+dte[3:5]+'-'+dte[0:2]+'')
		#reqs.fecha_estimacion = ''+dte[6:10]+'-'+dte[3:5]+'-'+dte[0:2]+''
		#dte = self.request.POST.get('fecha_inicio_planificada')
		#reqs.fecha_inicio_planificada = ''+dte[6:10]+'-'+dte[3:5]+'-'+dte[0:2]+''
		reqs.fecha_inicio_planificada = self.request.POST.get('fecha_inicio_planificada')

		#dte = self.request.POST.get('fecha_fin_planificada')
		#reqs.fecha_fin_planificada = ''+dte[6:10]+'-'+dte[3:5]+'-'+dte[0:2]+''
		reqs.fecha_fin_planificada = self.request.POST.get('fecha_fin_planificada')

		#if self.request.POST.get('fehca_inicio_real') != '':
		#	reqs.fehca_inicio_real= self.request.POST.get('fehca_inicio_real')
		#if self.request.POST.get('fecha_entrega_real') != '':
		#	reqs.fecha_entrega_real= self.request.POST.get('fecha_entrega_real')
		reqs.responsable=AuthUser.objects.get(pk=int(self.request.POST.get('responsable')))
		if self.request.POST.get('estado') != '':
			reqs.estado = PeticionEstado.objects.get(pk=int(self.request.POST.get('estado')))
		else:
			reqs.estado = PeticionEstado.objects.get(pk=1)
		if self.request.POST.get('calidad_input') != '':
			reqs.calidad_input = ReqCalidadInput.objects.get(pk=int(self.request.POST.get('calidad_input')))
		else:
			reqs.calidad_input = ReqCalidadInput.objects.get(pk=1)
		if self.request.POST.get('estimacion_alto_nivel') != '':
			reqs.estimacion_alto_nivel = ReqEstimAltoNivel.objects.get(pk=int(self.request.POST.get('estimacion_alto_nivel')))
		else:
			reqs.estimacion_alto_nivel = ReqEstimAltoNivel.objects.get(pk=1)
		if self.request.POST.get('prioridad') != '':
			reqs.prioridad = ReqPrioridad.objects.get(pk=int(self.request.POST.get('prioridad')))
		else:
			reqs.prioridad = ReqPrioridad.objects.get(pk=10)
		if self.request.POST.get('estimacion_acuerdo') != '':
			reqs.estimacion_acuerdo =self.request.POST.get('estimacion_acuerdo')
		if self.request.POST.get('estimacion_fenix_h') != '':
			reqs.estimacion_fenix_h =self.request.POST.get('estimacion_fenix_h')
		if self.request.POST.get('horas_adicionales') != '':
			reqs.horas_adicionale=self.request.POST.get('horas_adicionales')
		if self.request.POST.get('horas_acuerddo_mes') != '':
			reqs.horas_acuerddo_mes = self.request.POST.get('horas_acuerddo_mes')
		reqs.seguimiento_diario = self.request.POST.get('seguimiento_diario')
		reqs.ordent = self.request.POST.get('ordent')
		reqs.programas = self.request.POST.get('programas')
		reqs.save()
		return redirect('dai_lis')




