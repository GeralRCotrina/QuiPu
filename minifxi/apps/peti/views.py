
from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, View
from apps.peti.forms import *
from apps.gestion.gv_view import *

from django.db.models import Q

import datetime
import calendar


"""  ==================================== PETICION ============================ """
class PetCrear(CreateView):
	model=Peticion
	form_class=PetForm
	template_name='peti/crear.html'
	success_url=reverse_lazy('pet_listar')

	def get_form(self, form_class=None):
		# Values
		form=super(CreateView,self).get_form(form_class=self.form_class)
		# Get Client
		form.fields["cliente"].queryset=Cliente.objects.filter(authcliente__idauth=self.request.user.pk)
		form.fields["cliente"].initial=Cliente.objects.filter(authcliente__idauth=self.request.user.pk).first()
		# Get asign
		clie = ''
		if AuthCliente.objects.filter(idauth=self.request.user.pk).exists():
			clie = AuthCliente.objects.filter(idauth=self.request.user.pk).first().idcliente
		else:
			clie = Cliente.objects.all().first()
		form.fields["creador"].queryset=AuthUser.objects.filter(authcliente__idcliente=clie)
		form.fields["creador"].initial=AuthUser.objects.get(pk=self.request.user.pk)
		return form



	def post(self,request,*args,**kwargs):

		pet = Peticion()
		pet.id_pet_fenix=self.request.POST.get('id_pet_fenix')
		pet.id_ot_fenix=self.request.POST.get('id_ot_fenix')
		pet.nombre=self.request.POST.get('nombre')
		pet.contenedora=self.request.POST.get('contenedora')
		pet.tipo = PeticionTipo.objects.get(pk=int(self.request.POST.get('tipo')))
		pet.cliente = Cliente.objects.get(pk=int(self.request.POST.get('cliente')))
		pet.gestion = PeticionGestion.objects.get(pk=int(self.request.POST.get('gestion')))
		pet.estado = PeticionEstado.objects.get(pk=int(self.request.POST.get('estado')))	
		pet.input_final = PeticionInputFinal.objects.get(pk=int(self.request.POST.get('input_final')))		
		if self.request.POST.get('fecha_solicitud') != '':
			pet.fecha_solicitud= self.request.POST.get('fecha_solicitud')		
		if self.request.POST.get('fecha_fin_acuerdo') != '':
			pet.fecha_fin_acuerdo= self.request.POST.get('fecha_fin_acuerdo')		
		if self.request.POST.get('fecha_real_entrega') != '':
			pet.fecha_real_entrega= self.request.POST.get('fecha_real_entrega')
		#if self.request.POST.get('horas_acuerdo') != '':
		#	pet.horas_acuerdo= self.request.POST.get('horas_acuerdo')
		if self.request.POST.get('horas_estimadas') != '':
			pet.horas_estimadas= self.request.POST.get('horas_estimadas')
		#pet.comentario = self.request.POST.get('comentario')
		pet.creador=AuthUser.objects.get(pk=self.request.user.pk)
		pet.zultima_modificacion = self.request.POST.get('fecha_estimacion')
		#grcl13
		pet.color = self.request.POST.get('color')
		pet.save()
		LogDeAccion(self.request.user.pk,pet.cliente,'PETICIÓN','-',0,pet.pk, (str(pet.id_pet_fenix)+' : '+str(pet.nombre)))
		return redirect('pet_listar')
 
# LogDeAccion(usuario, tabla, campo, tipo_de_modificación,  pk_de_la_entidad, mensaje_de_log):
# TM (Tipo de modificación) Create:0		Read:1		Update:2		Delete:3




class PetEliminar(DeleteView):
	model=Peticion
	form_class=PetForm
	template_name='peti/eliminar.html'
	success_url=reverse_lazy('pet_listar')	#grcl4

	def post(self,request,*args,**kwargs):
		pet_lst = Requerimientos.objects.filter(peticion=str(self.kwargs['pk']))
		if len(pet_lst) == 0:
			pet_d=Peticion.objects.get(pk=self.kwargs['pk'])
			LogDeAccion(self.request.user.pk,pet_d.cliente,'PETICIÓN','-','3',pet_d.pk, (str(pet_d.id_pet_fenix)+' : '+str(pet_d.nombre)))
			pet_d.delete()
		return redirect('pet_listar')



class PetEditar(UpdateView):
	model=Peticion
	form_class=PetEditForm
	template_name='peti/crear.html'
	success_url=reverse_lazy('pet_listar') #grcl4

	def get_form(self, form_class=None):
		form=super(UpdateView,self).get_form(form_class=self.form_class)
		# Get Clients
		form.fields["cliente"].queryset=Cliente.objects.filter(authcliente__idauth=self.request.user.pk)
		# Get user
		clie = ''
		if Peticion.objects.filter(pk=self.object.pk).exists():
			pet_e = Peticion.objects.get(pk=self.object.pk)
			clie = pet_e.cliente
		else:
			clie = AuthCliente.objects.all()
		form.fields["creador"].queryset=AuthUser.objects.filter(authcliente__idcliente=clie) #grcl4
		return form





 
class PetListar(View): 

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
		

		if fecha_desde == None:
			fh1 = datetime.datetime.now()
			fecha_desde = "'"+str(fh1.year)+"-"+str(fh1.month)+"-01'"
		if fecha_hasta == None:
			fh = datetime.datetime.now()
			cant_dias = calendar.monthrange(fh.year,fh.month)
			fecha_hasta = "'"+str(fh.year)+"-"+str(fh.month)+"-"+str(cant_dias[1])+"'"



		from django.db import connection, transaction
		object_list = []		
		cursor = connection.cursor()
		if clie == '0':
			#print("  >> 1")
			cursor.execute("CALL sp_pet_x_fecha ("+str(fecha_desde)+","+str(fecha_hasta)+")")
		else:
			str_qry = "CALL sp_pet_x_fecha_1 ("+str(fecha_desde)+","+str(fecha_hasta)+","+str(clie)+")"
			#print("  >>  "+str_qry)
			cursor.execute(str_qry)
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)


		cursor.close()

		# Bluid mensaje
		msj = "Reporte de peticiones entre el "+fecha_desde+" hasta "+fecha_hasta
		if clie != '0':
			for x in (x for x in obj2 if x.idcliente == int(clie)):
				msj = msj + " en "+x.cliente

		dicc = { 
			'object_list':object_list,
			'lst_cliente': obj2,
			'msj': msj
		}
		return render(request,'peti/listar.html',dicc)

"""
tsk_tot_pla 
tsk_tot_inc
gnt_tot_inc
etc
horas_adicionales



		rs_hc = 0.0 # tsk_tot_pla 
		rs_tp = 0.0 # tsk_tot_pla 
		rs_tp = 0.0 # tsk_tot_pla 
		rs_ti = 0.0 # tsk_tot_inc
		rs_ig = 0.0 # gnt_tot_inc
		rs_et = 0.0 # etc
		rs_ha = 0.0 # horas_adicionales

,

			if dic['horas_acuerdo'] != None:
				rs_hc = float(rs_hc) + float(dic['horas_acuerdo'])

			if dic['tsk_tot_pla'] != None:
				rs_tp = float(rs_tp) + float(dic['tsk_tot_pla'])

			if dic['tsk_tot_inc'] != None:
				rs_ti = float(rs_ti) + float(dic['tsk_tot_inc'])

			if dic['gnt_tot_inc'] != None:
				rs_ig = float(rs_ig) + float(dic['gnt_tot_inc'])

			if dic['etc'] != None:
				rs_et = float(rs_et) + float(dic['etc'])

			if dic['horas_adicionales'] != None:
				rs_ha = float(rs_ha) + float(dic['horas_adicionales'])

				
			'rs_hc': rs_hc,
			'rs_tp': rs_tp,
			'rs_ti': rs_ti,
			'rs_ig': rs_ig,
			'rs_et': rs_et,
			'rs_ha': rs_ha
"""








