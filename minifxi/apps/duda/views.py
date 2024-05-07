from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from apps.gestion.models import Dudas, Requerimientos
from apps.duda.forms import *

import datetime
import calendar
from django.db.models import Q




# ============ D U D A S 

class DudCreRef(CreateView):
	model=Dudas
	form_class=DudasForm
	template_name='duda/cre.html'
	success_url=reverse_lazy('dud_lis')

	def get_form(self, form_class=None):
		form=super(CreateView,self).get_form(form_class=self.form_class)
		form.fields["task"].queryset=Task.objects.filter(idtask=self.kwargs['pk'])
		form.fields["rep_consulta"].queryset=AuthUser.objects.filter(id=self.request.user.pk)
		return form



class DudLis(ListView):
	model=DudasRelalivaA
	template_name='duda/lis.html'

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
			if AuthCliente.objects.filter(idauth = userpk ).exists():
				asig01 = AuthCliente.objects.filter( idauth = userpk ).first()
				clie = asig01.idcliente.pk
			else:
				clie = '0'
		
		#	Buils date
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
			cursor.execute("CALL sp_dud_x_fecha ("+str(fecha_desde)+","+str(fecha_hasta)+",1)")
		else:
			cursor.execute("CALL sp_dud_x_fecha_1 ("+str(fecha_desde)+","+str(fecha_hasta)+","+str(clie)+",1)")
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
		cursor.close()

		# Bluid mensaje
		msj = "Reporte de dudas entre el "+fecha_desde+" hasta "+fecha_hasta
		if clie != '0':
			for x in (x for x in obj2 if x.idcliente == int(clie)):
				msj = msj + " en "+x.cliente

		#	Build response
		dicc = { 
			'object_list':object_list,
			'msj': msj,
			'obj2' : obj2
		}
		return render(request,'duda/lis.html',dicc)





#	Listado de dudas por reqrimiento
class DudXReq(View):

	def get(self,request,*args,**kwargs):

		idr = self.request.GET.get('idr')

		# Para el matcode de clientes
		obj2 = Cliente.objects.all()
		for ob in obj2:
			pass

		from django.db import connection, transaction
		object_list = []		
		cursor = connection.cursor()
		cursor.execute("CALL sp_dud_x_req ("+str(idr)+",1)")
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
		cursor.close()

		#	Build response 
		dicc = { 
			'object_list': object_list,
			'msj': "Reporte de dudas por requerimiento",
			'obj2' : obj2
		}
		return render(request,'duda/lis.html',dicc)
		


#	Listado de dudas por petición
class DudXPet(View):

	def get(self,request,*args,**kwargs):

		idp = self.request.GET.get('idp')

		# Para el matcode de clientes
		obj2 = Cliente.objects.all()
		for ob in obj2:
			pass

		from django.db import connection, transaction
		object_list = []		
		cursor = connection.cursor()
		cursor.execute("CALL sp_dud_x_pet ("+str(idp)+",1)")
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
		cursor.close()

		#	Build response 
		dicc = { 
			'object_list' : object_list,
			'msj' : "Reporte de dudas por peticion",
			'obj2' : obj2
		}
		return render(request,'duda/lis.html',dicc)





class DudEdi(UpdateView):
	model=Dudas
	form_class=DudasEdiForm
	template_name='duda/cre.html'
	success_url=reverse_lazy('dud_lis') 

	def get_form(self, form_class=None):
		form=super(UpdateView,self).get_form(form_class=self.form_class)
		dud = Dudas.objects.get(pk=self.kwargs['pk'])
		tks = Task.objects.filter(requerimiento=dud.task.requerimiento)
		form.fields["task"].queryset= tks
		return form




class DudEli(DeleteView):
	model=Dudas
	form_class=DudasForm
	template_name='duda/eli.html'
	success_url=reverse_lazy('dud_lis')

#grcl1
class DudExp(View):

	def get(self,request,*args,**kwargs):
		cod_col = self.request.GET.get('cod_col')
		id_cli = self.request.GET.get('id_cli')

		cad = ''

		if cod_col:
			# Consulta por Colaborador y Cliente
			cad ="CALL sp_duc_exp01 ("+str(id_cli)+","+str(cod_col)+")"
		else:
			#	Consulta solo por Cliente y responsable.
			cad = "CALL sp_duc_exp02 ("+str(id_cli)+")"

		from django.db import connection, transaction

		object_list = []		
		cursor = connection.cursor()
		cursor.execute(cad)
		resultado = cursor.fetchall()

		if resultado:
			for row in resultado:
				dic = dict(zip([col[0] for col in cursor.description], row))
				object_list.append(dic)
		cursor.close()

		dicc = { 'object_list':object_list,
				 'msj': "No se encontró data para exportar." }


		return render(request,'duda/exp.html',dicc)




